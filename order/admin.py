from django.contrib import admin
from  .models import Checkout, OrderedProducts

class OrderItemInline(admin.TabularInline):
    model = OrderedProducts
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]