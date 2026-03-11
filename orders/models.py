from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.db import transaction
from django.db.models import F

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow guest carts
    session_key = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart ({self.user or self.session_key})"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def subtotal(self):
        return self.product.effective_price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def place_order(self):
        # Confirm order: validate stock and decrease it. Uses atomic transaction - all or nothing!
        with transaction.atomic():
            for item in self.items.all():
                product = item.product
                if not product.can_order(item.quantity):
                    raise ValueError(
                        f"Not enough stock for '{product.name}'. "
                        f"Available: {product.stock}, Requested: {item.quantity}"
                    )
                # Decrease stock using F() to prevent race conditions
                product.stock = F('stock') - item.quantity
                product.save()

            self.status = 'confirmed'
            self.save()

            #  Mock payment record
            Payment.objects.create(
                order=self,
                method='card', # default, in real app user selects this 
                amount=self.total_price,
                status='completed'  # mock: assume payment succeeds
            )

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot of price at order time

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def subtotal(self):
        return self.price * self.quantity

class Payment(models.Model):
    METHOD_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('cash', 'Cash on Delivery'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)  # From payment gateway
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment #{self.id} - {self.order} ({self.status})"
    
