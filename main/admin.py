from django.contrib import admin
from .models import Product, ProductMaterial, Material, WareHouse

admin.site.register(Product)
admin.site.register(ProductMaterial)
admin.site.register(Material)
admin.site.register(WareHouse)