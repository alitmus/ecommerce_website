from django.contrib import admin
from .models import Category,Product ,Review ,Image ,Order ,OrderItem,Subscriber

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Image)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Subscriber)