from django.contrib import admin
from .models import Invoice, Item, InvoiceEdit, ItemEdit

admin.site.register(Invoice)
admin.site.register(Item)
admin.site.register(InvoiceEdit)
admin.site.register(ItemEdit)

