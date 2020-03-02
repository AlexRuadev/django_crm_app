from django.shortcuts import render, redirect
from django.http import HttpResponse
# allow us to create multiple forms from only one form
from django.forms import inlineformset_factory
# To use django user authentication form
from django.contrib.auth.forms import UserCreationForm
# Import flash messages
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# To manage permissions and access to pages when user isn't logged in
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.


@unauthenticated_user
def registerPage(request):
    # If user is authenticated, redicrect to home when try to access registerPage

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Get the username and store in user variable
            username = form.cleaned_data.get('username')

            # When a customer signup , we add it to the group customer
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    # if POST method, we get username and password
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
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


def userPage(request):
    context = {}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    # Check our database and query all products
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'my_product_list': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
