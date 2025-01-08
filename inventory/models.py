from django.db import models

class Inventory(models.Model)
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    price_per_item = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    quantity_in_stock = models.PositiveIntegerFieldIntegerField(null=False, blank=False)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='inventory_items', on_delete=models.CASCADE)


    def __str__(self):
        return self.name


