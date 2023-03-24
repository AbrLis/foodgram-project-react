from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        # "role",
        "first_name",
        "last_name",
    )
    search_fields = (
        "username",
        "email",
    )
    list_filter = ("username", "email")
    empty_value_display = "-пусто-"
    sortable_by = (
        "id",
        "username",
        "email",
        # "role",
    )


admin.site.register(User, UserAdmin)
