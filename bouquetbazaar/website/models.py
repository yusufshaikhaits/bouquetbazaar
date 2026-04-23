from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('bouquet', 'Handmade Bouquet'),
        ('gift', 'Gift Box'),
        ('letter', 'Love Letter / Personalised Note'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='bouquet')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Order(models.Model):
    DELIVERY_CHOICES = [
        ('pickup', 'Self Pickup'),
        ('delivery', 'Online Delivery'),
    ]

    customer_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    delivery_preference = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='delivery')
    address = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    cart_items = models.JSONField()  # Stores the list of items
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} from {self.customer_name}"
