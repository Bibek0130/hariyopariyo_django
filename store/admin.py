from django.contrib import admin

# Register your models here.
from .models import * #here .models means models is in same directory. and * means we want to import all 

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
