from django.contrib import admin
from .models import Category, FoodItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    search_fields = ("name",)


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = (
        "name", "category", "price", "is_available",
        "is_spicy", "is_vegetarian", "updated_at",
    )
    list_editable = ("price", "is_available")
    list_filter = ("category", "is_available", "is_spicy", "is_vegetarian")
    search_fields = ("name", "description")
    fieldsets = (
        (None, {
            "fields": ("name", "category", "description", "image")
        }),
        ("Ціна та статус", {
            "fields": ("price", "is_available", "is_spicy", "is_vegetarian")
        }),
    )
