from django.urls import path
from .views import *

urlpatterns = [
    path("", BookListView.as_view(), name="index"),
    path("<int:pk>", BookDetailView.as_view(), name="book_detail"),
    path("cart", CartView.as_view(), name="cart_item"),
    path("order", CreateOrder.as_view(), name="create_order"),
    path("wishlist", WishlistView.as_view(), name="wishlist"),
    path("otp", OTPConfirmation.as_view(), name="otp_confirmation"),
]
