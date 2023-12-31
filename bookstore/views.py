from django.views.generic import ListView
from django.db.models import Q
from .models import Book


class BookListView(ListView):
    model = Book
    template_name = "index.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        genre = self.request.GET.get("genre")
        title = self.request.GET.get("title")
        if genre:
            queryset = queryset.filter(genre=genre)
        if title:
            queryset = queryset.filter(Q(title__icontains=title))
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        context["genres"] = Book.GENRE_CHOICES
        return context
