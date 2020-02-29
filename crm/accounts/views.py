from django.shortcuts import render, redirect
from django.http import HttpResponse
# allow us to create multiple forms from only one form
from django.forms import inlineformset_factory

from .models import *
from .forms import OrderForm
from .filters import OrderFilter

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


def customer(request, pk_customer):
    customer = Customer.objects.get(id=pk_customer)

    orders = customer.order_set.all()
    order_count = orders.count()

    # we query the orders, throw them in the filter, make a request to filter down
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer,
               'orders': orders, 'order_count': order_count, 'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


def createOrder(request, pk):
    # Create the instance of our FormSet, We need to pass first the parent Model, and then the child Model, and which fields for the child object
    # Extra allows us to choose how many fields we want
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=3)

    customer = Customer.objects.get(id=pk)
    # The query set allows us to hide the firsts few fields which are pre-filled
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    # order_form = OrderForm(initial={'customer': customer})
    # we sending our form with POST
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    order_form = OrderForm(instance=order)

    if request.method == 'POST':
        # putting that instance will allow us to change the order and not creating a new one
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'order_form': order_form}
    return render(request, 'accounts/order_form.html', context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
