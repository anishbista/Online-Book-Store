from django.urls import path
from .views import *

urlpatterns = [
    path("", BookListView.as_view(), name="index"),
    path("<int:pk>", BookDetailView.as_view(), name="book_detail"),
    path("review/<int:pk>", BookReviewView.as_view(), name="book_review"),
    path("cart", CartView.as_view(), name="cart_item"),
    path("order", CreateOrder.as_view(), name="create_order"),
    path("wishlist", WishlistView.as_view(), name="wishlist"),
    path("otp", OTPConfirmation.as_view(), name="otp_confirmation"),
    path("read_book", ReadBookPDFView.as_view(), name="read_book"),
]
