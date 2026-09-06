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
