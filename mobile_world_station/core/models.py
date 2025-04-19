from django.db import models

from django.contrib.auth.models import User

# Create your models here.

ITEM_TYPES = [
    ('personal_computer', 'Personal Computer'),
    ('laptop', 'Laptop'),
    ('phone', 'Phone'),
    ('tablet', 'Tablet'),
    ('watch', 'Watch'),
    ('headphones', 'Headphones'),
    ('accessory', 'Accessory'),
]

BRAND_CHOICES = [
    ('apple', 'Apple'),
    ('samsung', 'Samsung'),
    ('dell', 'Dell'),
    ('hp', 'HP'),
    ('lenovo', 'Lenovo'),
    ('xiomi', 'Xiomi'),
    ('microsoft', 'Microsoft'),
]

SERVICE_CHOICES = [
    ('screen_replacement', 'Screen Replacement'),
    ('battery_replacement', 'Battery Replacement'),
    ('water_damage_repair', 'Water Damage Repair'),
    ('software_issue', 'Software Issue'),
    ('other', 'Other'),
]

SUBJECT_CHOICES = [
    ('inquiry', 'General Inquiry'),
    ('feedback', 'Feedback/Suggestions'),
    ('technical_support', 'Technical Support'),
    ('repair_status', 'Repair Status'),
    ('business_inquiry', 'Business Inquiry'),
    ('other', 'Other'),
]


class Item(models.Model):
    item_name = models.CharField(max_length=100)  # short name/title
    item_price = models.DecimalField(max_digits=6, decimal_places=2)  # for currency values
    item_description = models.TextField(blank=True, null=True)  # long optional text
    item_image = models.URLField(blank=True, null=True)    
    item_brand = models.CharField(max_length=20, choices=BRAND_CHOICES, blank=True, null=True)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES, blank=True, null=True)
    item_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name

class AppointmentEmail(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)  # flexible for formatting
    service_needed = models.CharField(max_length=30, choices=SERVICE_CHOICES)
    preferred_date = models.DateField()
    device_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.service_needed}"
    
class ContactUsEmail(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    subject = models.CharField(max_length=30, choices=SUBJECT_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.subject}"
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    # total_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.user} - {self.product}"
    
    @property
    def product_price(self):
        """Calculate total price for this cart item (quantity * price)"""
        return round(self.quantity * self.product.item_price, 2)

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicate items


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.item_name}"