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


    @staticmethod
    def core(data, new=[]): 
        serializer = UserRequestSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        requested_product = Product.objects.get(product_code=serializer.validated_data['product_code'])
        requested_materials = ProductMaterial.objects.filter(product=requested_product)

        state = []
        result = []

        for material in requested_materials:
            required_quantity = float(material.quantity) * float(serializer.validated_data['quantity'])

            we_need = required_quantity    


            warehouses = WareHouseSerializer(instance=WareHouse.objects.filter(material=material, remainder__gte=0), many=True)

            for warehouse in warehouses.data:

                if warehouse['remainder'] == 0:
                    continue

                if warehouse['remainder'] < we_need:
                    we_need = we_need - warehouse['remainder']

                    warehouse['remainder'] = 0


                    state.append({
                        'warehouse_id': warehouse['id']
                    })
                
                elif warehouse['remainder'] > we_need:
                    we_need = 0
                    warehouse['remainder'] -= we_need
                
                elif warehouse['remainder'] == we_need:
                    we_need = 0
                    warehouse['remainder'] = 0
                else:
                    print('VALUES SUCKS')

        

    def post(self, request, *args, **kwargs):
        self.core(request.data)
        return Response({'msg':'Maintain'})
