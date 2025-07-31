from rest_framework import serializers
from .models import Product, ProductMaterial, Material, WareHouse


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 
            'product_name',
            'product_code',
        )

        extra_kwargs = {
            'product_code': {'required': False}
        }


class MaterialSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Material
        fields = (
            'id', 
            'material_name'
        )

class ProductMaterialSerializer(serializers.ModelSerializer):
    product = serializers.CharField(required=True)
    material = serializers.UUIDField(required=True)
    

    class Meta:
        model = ProductMaterial
        fields = (
            'product', # actually we return id, and check if serializer transforms it
            'material',
            'quantity'
        )

    # def validate(self, attrs):
    #     attrs['quantity'] = None
    #     return super().validate(attrs)

    def create(self, validated_data):
        code = validated_data['product']

        product = Product.objects.filter(product_code=code)
        
        if not product.exists():
            raise serializers.ValidationError({
                'success': False,
                'message': 'Product not found with this code'
            })
        
        validated_data['product'] = product.first()

        return super().create(validated_data)

class WareHouseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    material = serializers.UUIDField(required=True)
    class Meta:
        model = WareHouse
        fields = (
            'id', 
            'material',
            'remainder',
            'price'
        )
    
    # def validate(self, attrs):
    #     material = 
    #     return super().validate(attrs)

    

class UserRequestSerializer(serializers.Serializer):
    product_code = serializers.CharField(required=True, write_only=True)
    quantity = serializers.CharField(required=True, write_only=True)


    def validate(self, data):
        product_code = data.get('product_code', None)
        quantity = data.get('quantity', None)

        product = Product.objects.filter(product_code=product_code)
        if not product.exists():
            raise serializers.ValidationError({
                'success': True,
                'message': 'Product has not been found with this code'
            })
        
        if int(quantity) < 1:
            raise serializers.ValidationError({
                'success': False,
                'message': 'Quantity must be 1 at least'
            })
        
        return data