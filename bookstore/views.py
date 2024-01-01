from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Book, Cart, CartItem


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


class CartView(ListView):
    model = CartItem
    template_name = "cart.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        user_cart = Cart.objects.get(user=self.request.user)
        print(user_cart)
        return CartItem.objects.filter(cart=user_cart)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_queryset()
        total_items = cart_items.count()
        total_price = sum(item.books.price * item.quantity for item in cart_items)

        context["total_items"] = total_items
        context["total_price"] = total_price

        return context
