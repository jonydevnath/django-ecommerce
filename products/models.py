from enum import unique
from django.db import models
from django.db.models import Q, F
from django.db.models import Count

# Create your models here.
class ProductManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)
    def low_stock(self):
        return self.filter(Q(stock__lt=10) | Q(price__gt=F('stock')))
    def in_stock(self):
        return self.filter(stock__gt=0)

class CategoryManager(models.Manager):
    def with_product_count(self):
        return self.annotate(product_count=Count('products'))

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.URLField(blank=True)
    description = models.TextField(blank=True)
    objects = CategoryManager()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.URLField(blank=True)  # Store image URL for now
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')
    objects = ProductManager()

    @property
    def effective_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price

    def __str__(self):
        return self.name