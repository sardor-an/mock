from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import ProductSerializer, ProductMaterialSerializer, MaterialSerializer, WareHouseSerializer, UserRequestSerializer
from .models import Product, ProductMaterial, Material, WareHouse

class RetriveUpdateDestroyProductApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
class CreateProductApiView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
class RetriveUpdateDestroyMaterialApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()
class CreateMaterialApiView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = MaterialSerializer
class RetriveUpdateDestroyProducttMaterialApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductMaterialSerializer
    queryset = ProductMaterial.objects.all()
class CreateProductMaterialApiView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductMaterialSerializer
class RetriveUpdateDestroyWareHouseApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = WareHouseSerializer
    queryset = WareHouse.objects.all()
class CreateWareHouseApiView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = WareHouseSerializer




class UserRequestApiView(APIView):
    permission_classes = [AllowAny]
        
    def post(self, request: Request, *args, **kwargs):
        
        result = []
        state = []

        for data in request.data:
            serializer = UserRequestSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            product = Product.objects.get(product_code=serializer.validated_data['product_code'])
            result.append({
                'product_name': product.product_name,
                'quantity': serializer.validated_data['quantity'],
                'materials': []
            })

            materials = ProductMaterial.objects.filter(product=product)

            for material in materials:
                quantity = float(material.quantity) * float(serializer.validated_data['quantity'])
                we_need = quantity
                warehouses = WareHouseSerializer(
                    instance = WareHouse.objects.filter(material=material.material), # be careful here
                    many=True
                )
                for warehouse in warehouses.data:

                    if state:
                        for data in state:
                            if warehouse['id'] == data['warehouse_id'] and warehouse['material'] == data['material']:
                                warehouse['remainder'] = data['left']
                                break
                    
                    if we_need == 0:
                        break

                    if warehouse['remainder'] == 0:
                        continue
                    
                    elif warehouse['remainder'] < we_need:
                        initial_remainder = warehouse['remainder']
                        we_need -= warehouse['remainder']
                        
                        result[-1]['materials'].append({
                            'warehouse_id': warehouse['id'],
                            'material': warehouse['material'],
                            'quantity': warehouse['remainder'],
                            'price': warehouse['price']
                        })

                        warehouse['remainder'] = 0

                        state.append({
                            'status': 'LESS',
                            'we_needed': quantity,
                            'we_need_now': we_need,
                            'had_left': initial_remainder,
                            'taken': initial_remainder,
                            'warehouse_id': warehouse['id'],
                            'left': warehouse['remainder'],
                            'material': warehouse['material']
                        })
                    
                    elif warehouse['remainder'] > we_need:
                        initial_remainder = warehouse['remainder']
                        warehouse['remainder'] -= we_need
                        
                        result[-1]['materials'].append({
                            'warehouse_id': warehouse['id'],
                            'material': warehouse['material'],
                            'quantity': we_need,
                            'price': warehouse['price']
                        })
                        state.append({
                            'status': 'MORE',
                            'we_needed': quantity,
                            'we_need_now': we_need,
                            'had_left': initial_remainder,
                            'taken': we_need,
                            'warehouse_id': warehouse['id'],
                            'left': warehouse['remainder'],
                            'material': warehouse['material']
                        })
                        we_need = 0

                    elif warehouse['remainder'] == we_need:
                        initial_remainder = warehouse['remainder']
                        warehouse['remainder'] = 0
                        
                        result[-1]['materials'].append({
                            'warehouse_id': warehouse['id'],
                            'material': warehouse['material'],
                            'quantity': we_need,
                            'price': warehouse['price']
                        })
                        state.append({
                            'status': 'EQUAL',
                            'we_needed': quantity,
                            'we_need_now': we_need,
                            'had_left': initial_remainder,
                            'taken': we_need,
                            'warehouse_id': warehouse['id'],
                            'left': warehouse['remainder'],
                            'material': warehouse['material']
                        })
                        we_need = 0

            
                if we_need > 0:
                    result[-1]['materials'].append({
                            'warehouse_id': None,
                            'material': warehouse['material'],
                            'quantity': we_need,
                            'price': None
                        })

        return Response({
            'result': result
        })
