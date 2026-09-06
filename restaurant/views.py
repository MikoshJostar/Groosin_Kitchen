import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from .models import FoodItem, Category


def home(request):
    categories = Category.objects.prefetch_related("items").all()
    uncategorized = FoodItem.objects.filter(category__isnull=True)

    # Дані для помічника: рекомендуємо тільки страви, що є в наявності
    available_items = FoodItem.objects.filter(is_available=True)
    dishes_for_assistant = [
        {
            "name": item.name,
            "description": item.description[:120],
            "price": str(item.price),
        }
        for item in available_items
    ]

    context = {
        "categories": categories,
        "uncategorized": uncategorized,
        "dishes_json": json.dumps(dishes_for_assistant, cls=DjangoJSONEncoder, ensure_ascii=False),
        "total_items": FoodItem.objects.count(),
    }
    return render(request, "restaurant/home.html", context)
