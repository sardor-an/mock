from django.db import models
from django.core.validators import MinValueValidator
from shared.models import BaseModel
from shared.utility import generate_product_code

class Product(BaseModel):
    product_name = models.CharField(max_length=150, unique=True)
    product_code = models.CharField(max_length=6, unique=True, blank=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f'{self.product_name}'
    


    def save(self, *args, **kwargs):
        
        code = generate_product_code()

        while Product.objects.filter(product_code=code).exists():
            code = generate_product_code()
        
        self.product_code = code
        super().save(*args, **kwargs)

class Material(BaseModel):
    material_name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return f'{self.material_name}'

class ProductMaterial(BaseModel):
    product = models.ForeignKey(to=Product, related_name='product_materials', on_delete=models.CASCADE)
    material = models.ForeignKey(to=Material, related_name='product_materials', on_delete=models.CASCADE)
    quantity = models.FloatField(validators=[MinValueValidator(limit_value=0, message='Quantity must be greater than 1')])

    def __str__(self):
        return f'for product {self.product.product_name}, material {self.material.material_name}, quantity {self.quantity}'


class WareHouse(models.Model):
    material = models.ForeignKey(to=Material, related_name='ware_houses', on_delete=models.CASCADE)
    remainder = models.IntegerField(validators=[MinValueValidator(limit_value=0, message='Quantity must be greater than 0')])
    price = models.IntegerField(validators=[MinValueValidator(limit_value=1, message='Quantity must be greater than 0')])

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'WH {self.pk}, material: {self.material.material_name} remains {self.remainder} | price {self.price}'