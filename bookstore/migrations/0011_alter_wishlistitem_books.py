# Generated by Django 5.0 on 2024-01-02 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0010_remove_wishlist_books_wishlistitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistitem',
            name='books',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bookstore.book'),
        ),
    ]
