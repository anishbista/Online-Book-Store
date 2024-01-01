from django.urls import path
from .views import *

urlpatterns = [
    path("", BookListView.as_view(), name="index"),
    path("<int:pk>", BookDetailView.as_view(), name="book_detail"),
    path("cart", CartView.as_view(), name="cart_item"),
]
