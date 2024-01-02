import random
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Book, Cart, CartItem
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail


class BookListView(ListView):
    model = Book
    template_name = "index.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        genre = self.request.GET.get("genre")
        query = self.request.GET.get("title")
        if genre:
            queryset = queryset.filter(genre=genre)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(author__icontains=query)
                | Q(genre__icontains=query)
            )
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        context["genres"] = Book.GENRE_CHOICES
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=user_cart, books=book
        )
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()

        return HttpResponseRedirect(reverse("cart_item"))


class CartView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = "cart.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        try:
            user_cart = Cart.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            user_cart = Cart.objects.create(user=self.request.user)
        return CartItem.objects.filter(cart=user_cart)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_items = self.object_list.count()
        total_price = sum(item.books.price * item.quantity for item in self.object_list)

        context["total_items"] = total_items
        context["total_price"] = total_price

        return context

    def post(self, request):
        otp = random.randint(1000, 9999)
        user_email = request.user.email
        send_mail(
            "OTP for Checkout",
            f"Your OTP for checkout is :{otp}",
            "anishbista9237@gmail.com",
            [user_email],
            fail_silently=False,
        )

        request.session["checkout_otp"] = otp
        return redirect("otp_confirmation")


class OTPConfirmation(View):
    def get(self, request):
        return render(request, "otp_entry.html")

    def post(self, request):
        submitted_otp = request.POST.get("otp")
        stored_otp = request.session.get("checkout_otp")

        if submitted_otp and stored_otp and int(submitted_otp) == stored_otp:
            del request.session["checkout_otp"]
            return render(request, "checkout_success.html")
        else:
            error_message = "Invalid OTP. Please try again."
            return render(request, "otp_entry.html", {"error_message": error_message})
