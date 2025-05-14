from django.urls import path
from . import views

urlpatterns = [
    path('produdcts/', views.product_list),
    path('products/<int:pk>/', views.product_detail),
]