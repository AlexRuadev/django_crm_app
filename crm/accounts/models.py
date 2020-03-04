from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    # Create a 1 to 1 relationship with the User(customer can have only one user and vice versa). CASCADE means when user is deleted, so is the relationship
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)

    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(
        default="serveimage1.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    # to show the name instead of "object" in our database
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door'),
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    # We had blank so the field isn't a required field
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    # Create a relation between this model (Products and Tag)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    # creating status tuples
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    # everytime we delete an order from a customer, the order will stay in database with a value of null
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL)

    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return self.product.name
