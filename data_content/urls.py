
from django.urls import path
from .import views

urlpatterns = [
    path("", views.home, name="home"),
    path("edit-stock/<pk>", views.update_stock, name="editStock"),
    path("delete-stock/<pk>", views.delete_stock, name="deleteStock"),

]
