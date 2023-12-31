from django.db import models
from django.conf import settings


class Book(models.Model):
    GENRE_CHOICES = (
        ("Fiction", "Fiction"),
        ("Non-Fiction", "Non-Fiction"),
        ("Science Fiction", "Science Fiction"),
        ("Mystery", "Mystery"),
    )

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    Cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    books = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.books.title} in Cart ({self.quantity})"
