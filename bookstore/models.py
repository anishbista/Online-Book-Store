from django.urls import reverse
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
    avg_rating = models.DecimalField(
        default=0.0,
        max_digits=3,
        decimal_places=2,
        help_text="Average rating gor the book",
    )

    def update_avg_rating(self):
        total_rating = sum(review.rating for review in self.reviews.all())
        num_reviews = self.reviews.count()

        if num_reviews > 0:
            self.avg_rating = total_rating / num_reviews
        else:
            self.avg_rating = 0.0

        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    books = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.books.title} in Cart ({self.quantity})"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Book, through="OrderItem")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("order", "book")


class Wishlist(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    books = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        # Adding unique constraint to prevent duplicate entries for a book in a wishlist
        unique_together = ("wishlist", "books")

    def __str__(self):
        return ""


class BookReview(models.Model):
    RATING_CHOICES = [
        (1, "One star"),
        (2, "Two star"),
        (3, "Three star"),
        (4, "Four star"),
        (5, "Five star"),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    review_text = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.book.update_avg_rating()

    def __str__(self):
        return self.book.title
