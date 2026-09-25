from django.contrib import admin

from .models import (
    Category,
    FoodItem,
    Order,
    OrderItem,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "order",
    )

    list_editable = (
        "order",
    )

    search_fields = (
        "name",
    )


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "is_available",
        "is_spicy",
        "is_vegetarian",
        "updated_at",
    )

    list_editable = (
        "price",
        "is_available",
    )

    list_filter = (
        "category",
        "is_available",
        "is_spicy",
        "is_vegetarian",
    )

    search_fields = (
        "name",
        "description",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "category",
                    "description",
                    "image",
                )
            },
        ),
        (
            "Ціна та статус",
            {
                "fields": (
                    "price",
                    "is_available",
                    "is_spicy",
                    "is_vegetarian",
                )
            },
        ),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "food",
        "quantity",
        "price",
        "total",
    )

    fields = (
        "food",
        "quantity",
        "price",
        "total",
    )

    def total(self, obj):
        return obj.total_price

    total.short_description = "Сума"


@admin.action(description="Позначити вибрані замовлення як готові")
def mark_orders_ready(modeladmin, request, queryset):
    queryset.update(
        status=Order.STATUS_READY
    )


@admin.action(description="Прийняти вибрані замовлення")
def mark_orders_accepted(modeladmin, request, queryset):
    queryset.update(
        status=Order.STATUS_ACCEPTED
    )


@admin.action(description="Передати вибрані замовлення на кухню")
def mark_orders_cooking(modeladmin, request, queryset):
    queryset.update(
        status=Order.STATUS_COOKING
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "status",
        "total",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "admin_response",
        "comment",
    )

    list_editable = (
        "status",
    )

    readonly_fields = (
        "user",
        "created_at",
        "updated_at",
        "total",
    )

    fieldsets = (
        (
            "Замовлення",
            {
                "fields": (
                    "user",
                    "status",
                    "total",
                    "created_at",
                    "updated_at",
                )
            },
        ),
        (
            "Повідомлення",
            {
                "fields": (
                    "comment",
                    "admin_response",
                )
            },
        ),
    )

    inlines = [
        OrderItemInline,
    ]

    actions = [
        mark_orders_accepted,
        mark_orders_cooking,
        mark_orders_ready,
    ]

    def total(self, obj):
        return obj.total_price

    total.short_description = "Загальна сума"