from django.contrib import admin
from django.utils.html import format_html
from .models import Category, FoodItem, Order, OrderItem


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
        (None, {"fields": ("name", "category", "description", "image")}),
        ("Ціна та статус", {"fields": ("price", "is_available", "is_spicy", "is_vegetarian")}),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("food", "name", "price", "quantity")
    can_delete = False
    has_add_permission = lambda self, request, obj=None: False


STATUS_COLORS = {"new": "#d32f2f", "processing": "#f9a825", "done": "#2e7d32", "cancelled": "#757575"}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "name", "phone", "items_summary", "total", "colored_status")
    list_filter = ("status", "created_at")
    search_fields = ("name", "phone")
    readonly_fields = ("total", "created_at")
    inlines = [OrderItemInline]
    actions = ["accept_orders", "mark_done", "cancel_orders"]
    date_hierarchy = "created_at"

    @admin.display(description="Страви")
    def items_summary(self, obj):
        return ", ".join(f"{i.name} ×{i.quantity}" for i in obj.items.all())

    @admin.display(description="Статус", ordering="status")
    def colored_status(self, obj):
        return format_html('<b style="color:{}">{}</b>',
                           STATUS_COLORS.get(obj.status, "#000"), obj.get_status_display())

    @admin.action(description="✅ Прийняти обрані замовлення (в обробку)")
    def accept_orders(self, request, qs):
        n = qs.filter(status="new").update(status="processing")
        self.message_user(request, f"Прийнято замовлень: {n}")

    @admin.action(description="🍽 Позначити як виконані")
    def mark_done(self, request, qs):
        self.message_user(request, f"Виконано: {qs.update(status='done')}")

    @admin.action(description="❌ Скасувати обрані")
    def cancel_orders(self, request, qs):
        self.message_user(request, f"Скасовано: {qs.update(status='cancelled')}")
