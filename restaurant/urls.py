from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("order/", views.create_order, name="create_order"),
]
