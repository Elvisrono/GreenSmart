from django.db import models

# Create your models here.

class ContactMessage(models.Model):
    email = models.EmailField(max_length=20)
    subject = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Seedling(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='seedlings/', null=True, blank=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    seedling = models.ForeignKey(Seedling, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seedling.name} ({self.quantity})"

