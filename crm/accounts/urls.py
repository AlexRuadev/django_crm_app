from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    # Using a name for our path gives us better routing in our html
    path('', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),
    path('products/', views.products, name='products'),
    # Dynamic routing, pk_customer is the parameter we put in our views, customer
    path('customer/<str:pk_customer>', views.customer, name="customer"),
    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
]
