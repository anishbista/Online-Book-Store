from celery import shared_task
from django.core.mail import send_mail
from .models import Book
from accounts.models import CustomUser
from .utils import get_highlighted_book


@shared_task
def send_highlighted_book_notification():
    highlighted_book = get_highlighted_book()

    if highlighted_book:
        all_users = CustomUser.objects.all()
        recipients = [user.email for user in all_users]
        print(recipients)
        subject = "Check out out highlighted book of the week!"
        message = f"Don't miss out this book: {highlighted_book.title} by {highlighted_book.author}"

        send_mail(subject, message, "anishbista9237@gmail.com", recipients)
