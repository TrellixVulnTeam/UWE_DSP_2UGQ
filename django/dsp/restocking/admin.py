"""
Links the models to the administration page.
"""

from django.contrib import admin
from .models import Product, Order, OrderItem, User, Transaction, TransactionItem, RestockingList, RestockingListItem

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name', 'size', 'fitting', 'colour')

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(TransactionItem)
admin.site.register(RestockingList)
admin.site.register(RestockingListItem)

