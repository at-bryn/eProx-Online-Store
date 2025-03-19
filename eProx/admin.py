from django.contrib import admin
from .models import *
from order.models import *



admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Business)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(ShippingAddress)
admin.site.register(Profile)
admin.site.register(Checkout)
admin.site.register(OrderedProducts)

