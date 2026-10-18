import json
import logging
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from .models import FoodItem, Category, Order, OrderItem


@ensure_csrf_cookie
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


@require_POST
def create_order(request):
    try:
        return _create_order(request)
    except Exception:
        logging.getLogger(__name__).exception("Order failed")
        return JsonResponse({"error": "Помилка сервера. Спробуйте ще раз або зателефонуйте нам."}, status=500)


def _create_order(request):
    """Приймає кошик (JSON), перераховує ціни з бази і зберігає замовлення."""
    try:
        data = json.loads(request.body)
    except ValueError:
        return JsonResponse({"error": "Некоректні дані"}, status=400)

    name = str(data.get("name", "")).strip()[:100]
    phone = str(data.get("phone", "")).strip()[:30]
    comment = str(data.get("comment", "")).strip()[:1000]
    if not name or len(phone) < 6:
        return JsonResponse({"error": "Вкажіть ім'я та телефон"}, status=400)

    lines = []
    for row in data.get("items", []):
        try:
            pk, qty = int(row["id"]), int(row["qty"])
        except (KeyError, TypeError, ValueError):
            continue
        if qty < 1:
            continue
        food = FoodItem.objects.filter(pk=pk, is_available=True).first()
        if food:
            lines.append((food, min(qty, 50)))
    if not lines:
        return JsonResponse({"error": "Кошик порожній або страви недоступні"}, status=400)

    with transaction.atomic():
        order = Order.objects.create(name=name, phone=phone, comment=comment)
        total = 0
        for food, qty in lines:
            OrderItem.objects.create(order=order, food=food, name=food.name,
                                     price=food.price, quantity=qty)
            total += food.price * qty
        order.total = total
        order.save(update_fields=["total"])
    return JsonResponse({"ok": True, "order_id": order.pk, "total": str(total)})
