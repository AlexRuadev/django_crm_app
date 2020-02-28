from django.shortcuts import render
from django.http import HttpResponse

from .models import *

# Create your views here.


def home(request):
    #  Quering our orders and customers
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    # We just want orders with the status of delivered
    delivered = orders.filter(status='Delivered').count

    pending = orders.filter(status='Pending').count

    context = {'my_orders_list': orders, 'my_customers_list': customers,
               'total_orders': total_orders, 'delivered': delivered, 'pending': pending}

    return render(request, 'accounts/dashboard.html', context)


def products(request):
    # Check our database and query all products
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'my_product_list': products})


def customer(request):
    return render(request, 'accounts/customer.html')
