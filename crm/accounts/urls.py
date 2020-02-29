from django.urls import path
from . import views


urlpatterns = [
    # Using a name for our path gives us better routing in our html
    path('', views.home, name="home"),
    path('products/', views.products, name='products'),
    # Dynamic routing, pk_customer is the parameter we put in our views, customer
    path('customer/<str:pk_customer>', views.customer, name='customer'),
    path('create_order/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
]
