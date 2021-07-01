from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Product, Category, Company, ProductSize, ProductSite, Comment

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Company)
admin.site.register(ProductSize)
admin.site.register(ProductSite)
admin.site.register(Comment)
