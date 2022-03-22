from django.contrib import admin
from django.utils.html import format_html  # для отображения фото в админке

from .models import Apartment, Image, Task, Profile


class InlineImage(admin.TabularInline):
    fk_name = "apartment"
    model = Image


@admin.register(Apartment)
class AprtmentAdmin(admin.ModelAdmin):
    list_display = ["id", "address", "rooms", "price", "desc", "floor", "owner"]
    inlines = [
        InlineImage,
    ]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["created", "url"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html(
            f'<img src="{obj.avatar.url}" style="width: 50px; height: 50px;"/>'
        )

    image_tag.short_description = "изображение"
    list_display = [
        "user",
        "phone_1",
        "phone_2",
        "image_tag",
        "first_name",
        "last_name",
        "email",
    ]
