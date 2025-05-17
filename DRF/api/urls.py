from django.urls import path
from . import views

urlpatterns = [
    # path('produdcts/', views.product_list),
    path('products/', views.ProductListAPIView.as_view()),
    # path('products/<int:pk>/', views.product_detail),
    path('products/<int:pk>/', views.ProductDeatilAPIView.as_view()),
    # path('orders/', views.Order_list),
    path('orders', views.OrderListAPIView.as_view()),
    path('product/info/', views.product_info),
]