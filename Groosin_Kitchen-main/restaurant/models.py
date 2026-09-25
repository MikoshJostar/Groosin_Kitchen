from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """Категорія страви."""
    name = models.CharField("Назва категорії", max_length=100)
    order = models.PositiveIntegerField("Порядок відображення", default=0)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    """Страва грузинської кухні."""
    category = models.ForeignKey(
        Category,
        verbose_name="Категорія",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="items",
    )

    name = models.CharField("Назва страви", max_length=200)

    description = models.TextField(
        "Опис",
        blank=True
    )

    price = models.DecimalField(
        "Ціна (грн)",
        max_digits=8,
        decimal_places=2
    )

    image = models.ImageField(
        "Фото",
        upload_to="food_images/",
        blank=True,
        null=True
    )

    is_available = models.BooleanField(
        "В наявності",
        default=True
    )

    is_spicy = models.BooleanField(
        "Гостра страва",
        default=False
    )

    is_vegetarian = models.BooleanField(
        "Вегетаріанська",
        default=False
    )

    created_at = models.DateTimeField(
        "Додано",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        "Оновлено",
        auto_now=True
    )

    class Meta:
        verbose_name = "Страва"
        verbose_name_plural = "Страви"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_NEW = "new"
    STATUS_ACCEPTED = "accepted"
    STATUS_COOKING = "cooking"
    STATUS_READY = "ready"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_NEW, "Нове"),
        (STATUS_ACCEPTED, "Прийнято"),
        (STATUS_COOKING, "Готується"),
        (STATUS_READY, "Готово"),
        (STATUS_CANCELLED, "Скасовано"),
    ]

    user = models.ForeignKey(
        User,
        verbose_name="Користувач",
        on_delete=models.CASCADE,
        related_name="orders",
    )

    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )

    admin_response = models.TextField(
        "Відповідь адміністратора",
        blank=True,
    )

    comment = models.TextField(
        "Коментар користувача",
        blank=True,
    )

    created_at = models.DateTimeField(
        "Створено",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Оновлено",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Замовлення №{self.pk} — {self.user.username}"

    @property
    def total_price(self):
        return sum(
            item.total_price
            for item in self.items.all()
        )


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name="Замовлення",
        on_delete=models.CASCADE,
        related_name="items",
    )

    food = models.ForeignKey(
        FoodItem,
        verbose_name="Страва",
        on_delete=models.PROTECT,
        related_name="order_items",
    )

    quantity = models.PositiveIntegerField(
        "Кількість",
        default=1,
    )

    # Зберігаємо ціну на момент замовлення.
    # Якщо адмін потім змінить ціну страви,
    # старе замовлення не зміниться.
    price = models.DecimalField(
        "Ціна на момент замовлення",
        max_digits=8,
        decimal_places=2,
    )

    class Meta:
        verbose_name = "Позиція замовлення"
        verbose_name_plural = "Позиції замовлення"

    def __str__(self):
        return f"{self.food.name} × {self.quantity}"

    @property
    def total_price(self):
        return self.price * self.quantity