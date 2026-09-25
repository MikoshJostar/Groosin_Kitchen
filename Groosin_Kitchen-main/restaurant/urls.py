from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),

    # Сторінка окремої страви
    path(
        "food/<int:pk>/",
        views.food_detail,
        name="food_detail",
    ),
]