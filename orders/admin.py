from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Payment

# Register your models here.

# --- Inlines ---
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0  # Don't show empty extra rows
    readonly_fields = ['subtotal']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal']

# --- ModelAdmins ---
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'created_at']
    inlines = [CartItemInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at']
    list_filter = ['status']
    search_fields = ['user__username']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at']
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'method', 'status', 'amount', 'created_at']
    list_filter = ['status', 'method']
    search_fields = ['transaction_id']