from django.contrib import admin
from .models import *


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = (CartItemInline,)


class WishlistInLine(admin.TabularInline):
    model = WishlistItem
    extra = 1


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    inlines = (WishlistInLine,)


class OrderInLine(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderInLine,)
    list_display = ["user", "total_price", "created_at"]


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ["book", "user", "rating"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "avg_rating"]


# @admin.register(BookPDF):
# class BookPDFAdmin(admin.ModelAdmin):
#     list_display =

admin.site.register(BookPDF)
