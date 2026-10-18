from django.db import models


class Category(models.Model):
    """Категорія страви, напр. Хачапурі, Хінкалі, Салати, Напої."""
    name = models.CharField("Назва категорії", max_length=100)
    order = models.PositiveIntegerField("Порядок відображення", default=0)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    """Страва грузинської кухні, яку можна замовити."""
    category = models.ForeignKey(
        Category,
        verbose_name="Категорія",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="items",
    )
    name = models.CharField("Назва страви", max_length=200)
    description = models.TextField("Опис", blank=True)
    price = models.DecimalField("Ціна (грн)", max_digits=8, decimal_places=2)
    image = models.ImageField(
        "Фото", upload_to="food_images/", blank=True, null=True
    )
    is_available = models.BooleanField("В наявності", default=True)
    is_spicy = models.BooleanField("Гостра страва", default=False)
    is_vegetarian = models.BooleanField("Вегетаріанська", default=False)
    created_at = models.DateTimeField("Додано", auto_now_add=True)
    updated_at = models.DateTimeField("Оновлено", auto_now=True)

    class Meta:
        verbose_name = "Страва"
        verbose_name_plural = "Страви"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Order(models.Model):
    """Замовлення, оформлене відвідувачем на сайті."""
    STATUS_CHOICES = [
        ("new", "Нове"),
        ("processing", "В обробці"),
        ("done", "Виконано"),
        ("cancelled", "Скасовано"),
    ]
    name = models.CharField("Ім'я", max_length=100)
    phone = models.CharField("Телефон", max_length=30)
    comment = models.TextField("Коментар", blank=True)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="new")
    total = models.DecimalField("Сума (грн)", max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Замовлення №{self.pk} — {self.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    food = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField("Страва", max_length=200)
    price = models.DecimalField("Ціна (грн)", max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField("Кількість", default=1)

    class Meta:
        verbose_name = "Позиція замовлення"
        verbose_name_plural = "Позиції замовлення"

    def __str__(self):
        return f"{self.name} × {self.quantity}"
