from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "food/<int:pk>/",
        views.food_detail,
        name="food_detail",
    ),

    path(
        "register/",
        views.register_view,
        name="register",
    ),

    path(
        "login/",
        views.login_view,
        name="login",
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),

    path(
        "food/<int:pk>/order/",
        views.create_order,
        name="create_order",
    ),

    path(
        "orders/",
        views.my_orders,
        name="my_orders",
    ),
]