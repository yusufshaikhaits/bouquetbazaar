from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone', 'delivery_preference', 'total_amount', 'created_at')
    list_filter = ('delivery_preference', 'created_at')
    search_fields = ('customer_name', 'phone', 'address')
    readonly_fields = ('created_at',)
