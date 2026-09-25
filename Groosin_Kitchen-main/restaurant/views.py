import json

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django import forms

from .models import Category, FoodItem, Order, OrderItem


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        min_length=6,
    )

    password2 = forms.CharField(
        label="Повторіть пароль",
        widget=forms.PasswordInput,
        min_length=6,
    )

    class Meta:
        model = User
        fields = ("username", "email")

        labels = {
            "username": "Ім'я користувача",
            "email": "Email",
        }

    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(
            username__iexact=username
        ).exists():
            raise forms.ValidationError(
                "Користувач з таким іменем вже існує."
            )

        return username

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Паролі не співпадають."
            )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data["password1"]
        )

        # Звичайний користувач.
        user.is_staff = False
        user.is_superuser = False

        if commit:
            user.save()

        return user


def home(request):
    categories = Category.objects.prefetch_related(
        "items"
    ).all()

    uncategorized = FoodItem.objects.filter(
        category__isnull=True
    )

    available_items = FoodItem.objects.filter(
        is_available=True
    )

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
        "dishes_json": json.dumps(
            dishes_for_assistant,
            cls=DjangoJSONEncoder,
            ensure_ascii=False,
        ),
        "total_items": FoodItem.objects.count(),
    }

    return render(
        request,
        "restaurant/home.html",
        context,
    )


def food_detail(request, pk):
    item = get_object_or_404(
        FoodItem,
        pk=pk,
    )

    return render(
        request,
        "restaurant/food_detail.html",
        {
            "item": item,
        },
    )


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(
                request,
                user,
            )

            messages.success(
                request,
                "Реєстрація успішна! Ласкаво просимо!"
            )

            return redirect("home")

    else:
        form = RegisterForm()

    return render(
        request,
        "restaurant/register.html",
        {
            "form": form,
        },
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST,
        )

        if form.is_valid():
            login(
                request,
                form.get_user(),
            )

            return redirect("home")

    else:
        form = AuthenticationForm()

    return render(
        request,
        "restaurant/login.html",
        {
            "form": form,
        },
    )


@login_required
def logout_view(request):
    logout(request)

    return redirect("home")


@login_required
def create_order(request, pk):
    if request.method != "POST":
        return redirect(
            "food_detail",
            pk=pk,
        )

    food = get_object_or_404(
        FoodItem,
        pk=pk,
        is_available=True,
    )

    try:
        quantity = int(
            request.POST.get(
                "quantity",
                1,
            )
        )
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    if quantity > 50:
        quantity = 50

    comment = request.POST.get(
        "comment",
        "",
    ).strip()

    with transaction.atomic():

        order = Order.objects.create(
            user=request.user,
            comment=comment,
        )

        OrderItem.objects.create(
            order=order,
            food=food,
            quantity=quantity,
            price=food.price,
        )

    messages.success(
        request,
        f"Замовлення №{order.pk} успішно створено!"
    )

    return redirect(
        "my_orders"
    )


@login_required
def my_orders(request):
    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related(
            "items__food"
        )
    )

    return render(
        request,
        "restaurant/orders.html",
        {
            "orders": orders,
        },
    )