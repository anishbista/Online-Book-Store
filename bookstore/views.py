import random
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib import messages
from .forms import BookReviewForm
from .models import *
from accounts.models import CustomUser
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

    def get(self, request, *args, **kwargs):
        book = self.get_object()
        form = BookReviewForm()

        # review, created = BookReview.objects.get_or_create(book=book, user=request.user)
        context = {
            "object": book,
            "form": form,
            # "review": review,
        }

        return render(request, "book_detail.html", context)

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        if "add_to_cart" in request.POST:
            print(book)
            user_cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=user_cart, books=book
            )
            if not item_created:
                cart_item.quantity += 1
                cart_item.save()
            return HttpResponseRedirect(reverse("cart_item"))
        elif "add_to_wishlist" in request.POST:
            user_wishlist, created = Wishlist.objects.get_or_create(user=request.user)
            print(created)
            wishlist_item, item_created = WishlistItem.objects.get_or_create(
                wishlist=user_wishlist, books=book
            )
            return HttpResponseRedirect(reverse("wishlist"))

        return HttpResponseRedirect(reverse("book_detail", kwargs={"pk": book.pk}))


class BookReviewView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        user = request.user
        rating = request.POST.get("rating")
        review_text = request.POST.get("review_text")

        print(review_text)

        if not OrderItem.objects.filter(order__user=user, book=book).exists():
            messages.error(request, "You can only review books you have ordered. ")
        elif rating and review_text:
            BookReview.objects.create(
                book=book, user=user, rating=rating, review_text=review_text
            )
            book.update_avg_rating()
        return HttpResponseRedirect(reverse("book_detail", kwargs={"pk": book.pk}))


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

        if self.request.user.order_count == 5:
            discount_price = float(total_price) - ((25 / 100) * float(total_price))

            context["discounted_price"] = discount_price

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
            return redirect("create_order")
        else:
            error_message = "Invalid OTP. Please try again."
            return render(request, "otp_entry.html", {"error_message": error_message})


class CreateOrder(View):
    def get(self, request):
        user_cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=user_cart)
        total_price = sum(item.books.price * item.quantity for item in cart_items)
        user = get_object_or_404(CustomUser, username=request.user.username)

        discount_applied = False
        if user.order_count == 5:
            discount_price = float(total_price) - (0.25 * float(total_price))
            discount_applied = True
        else:
            discount_price = total_price

        order = Order.objects.create(user=request.user, total_price=discount_price)

        if discount_applied:
            user.order_count = 0
        else:
            user.order_count += 1
        user.save()

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.books,
                quantity=item.quantity,
                price=item.books.price * item.quantity,
            )
        user_cart.cartitem_set.all().delete()

        return render(request, "checkout_success.html")


class WishlistView(LoginRequiredMixin, ListView):
    model = WishlistItem
    template_name = "wishlist.html"
    context_object_name = "wishlist"

    def get_queryset(self):
        try:
            user_wishlist = Wishlist.objects.get(user=self.request.user)

        except ObjectDoesNotExist:
            user_wishlist = Wishlist.objects.create(user=self.request.user)

        return WishlistItem.objects.filter(wishlist=user_wishlist)
