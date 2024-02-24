from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    prouser = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.prouser.username


class Category(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    market_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title   
    
    
class Cart(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    total = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart #{self.id}==Complete== {self.completed}" 

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    price =  models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal =  models.PositiveIntegerField()

    def __str__(self):
        return f"Cart=={self.cart.id} ==CartProduct== {self.id}==Quantity== {self.quantity}"
    
ORDER_STATUS_CHOICES = [
        ('received', 'Order Received'),
        ('processing', 'Order Processing'),
        ('on_the_way', 'On the Way'),
        ('completed', 'Order Completed'),
        ('canceled', 'Order Canceled'),
    ]

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    address = models.TextField()
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    total = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='received')
    date = models.DateTimeField(auto_now_add=True)
    payment = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.get_order_status_display()}"