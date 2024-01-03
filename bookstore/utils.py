from .models import Book


def get_highlighted_book():
    # .order_by('?'): This part is using Django's order_by() function with '?', which instructs the database to return results in a random order. It shuffles the query set randomly.
    highlighted_book = Book.objects.filter(avg_rating__gte=4.5).order_by("?").first()
    return highlighted_book
