# Generated by Django 5.0 on 2024-01-02 10:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0011_alter_wishlistitem_books'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistitem',
            name='books',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookstore.book'),
        ),
    ]