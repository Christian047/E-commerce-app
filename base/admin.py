from django.contrib import admin
from .models import *




admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Wallet)
admin.site.register(Expenses)
admin.site.register(Category)
admin.site.register(Subscribers)



# Register your models here.
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)

