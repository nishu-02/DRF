from django.urls import path
from . import views

urlpatterns = [
    # path('produdcts/', views.product_list),
    # path('products/', views.ProductListAPIView.as_view()),
    path('products/', views.ProductListCreateAPIView.as_view()), # the rest_framework convention is to have single end point for both the methods

    # path('products/create/', view.ProductCreateAPIView.as_view()), 

    # path('products/<int:pk>/', views.product_detail),
    path('products/<int:pk>/', views.ProductDeatilAPIView.as_view()),
    
    # path('orders/', views.Order_list),
    path('orders', views.OrderListAPIView.as_view()),
    
    path('user-orders', views.UserOrderListAPIView.as_view(), name='user-orders'),
    
    # path('product/info/', views.product_info),
    path('product/info/', views.ProductInfoAPIView.as_view())
]