from django import forms
from .models import BookReview


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ["rating", "review_text"]
        widgets = {
            "review_text": forms.Textarea(attrs={"rows": 3}),
        }
