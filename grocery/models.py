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