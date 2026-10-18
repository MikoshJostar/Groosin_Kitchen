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


from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("food", "name", "price", "quantity")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "total", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "created_at")
    search_fields = ("name", "phone")
    readonly_fields = ("total", "created_at")
    inlines = [OrderItemInline]
