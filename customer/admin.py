from django.contrib import admin
from .models import MenuItem, Category, OrderModel, Allergy

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)
admin.site.register(Allergy)