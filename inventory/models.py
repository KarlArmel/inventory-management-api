from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from django.contrib.auth import get_user_model

class InventoryItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, related_name='inventory_items', on_delete=models.CASCADE)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    price_per_item = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    quantity_in_stock = models.PositiveIntegerField(null=False, blank=False)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='inventory_items', on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class InventoryChange(models.Model):
    INVENTORY_CHANGE_TYPES = (
        ('restock', 'Restock'),
        ('sell', 'Sell'),
        ('adjustment', 'Adjustment'),
    )
    item = models.ForeignKey(InventoryItem, related_name="inventory_changes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="inventory_changes", on_delete=models.CASCADE)
    change_type = models.CharField(max_length=20, choices=INVENTORY_CHANGE_TYPES)
    quantity_change = models.IntegerField()  
    created_at = models.DateTimeField(default=timezone.now)    
    inventory_item = models.ForeignKey(Inventory, related_name='changes', on_delete=models.CASCADE)
    quantity_changed = models.IntegerField()
    date_changed = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, related_name='inventory_changes', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_change_type_display()} of {self.quantity_change} units on {self.item.name} by {self.user.username}"

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username


