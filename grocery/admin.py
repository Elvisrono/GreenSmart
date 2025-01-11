from django.contrib import admin

from grocery.models import ContactMessage, Seedling, CartItem

# Register your models here.
admin.site.register(ContactMessage)
admin.site.register(Seedling)
admin.site.register(CartItem)
