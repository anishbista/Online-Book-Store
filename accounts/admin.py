from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "phone_number",
        "address",
        "order_count",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "address",
                    "phone_number",
                    "order_count",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "address",
                    "phone_number",
                    "order_count",
                )
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
