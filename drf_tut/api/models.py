from django.db import models
from django.contrib.auth.models import AbstractUser


import uuid

# Create your models here.
class User(AbstractUser):
    pass

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def in_stock(self):
        return self.stock > 0


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending'
        COMPLETED = 'Completed'
        CANCELLED = 'Cancelled'

    order_id  = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')


    def __str__(self):
        return f"Order ID: {self.order_id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quatity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quatity

    def __str__(self):
        return f"{self.product.name} - {self.quatity} in oder {self.order.order_id}"    
    