from django.urls import path
from .views import RetriveUpdateDestroyProductApiView, CreateProductApiView, RetriveUpdateDestroyMaterialApiView, \
      CreateMaterialApiView, CreateProductMaterialApiView, RetriveUpdateDestroyProducttMaterialApiView, \
      CreateWareHouseApiView, RetriveUpdateDestroyWareHouseApiView, UserRequestApiView

urlpatterns = [
    path('product/<uuid:pk>/', RetriveUpdateDestroyProductApiView.as_view()),
    path('product/create/', CreateProductApiView.as_view()),
    path('material/<uuid:pk>/', RetriveUpdateDestroyMaterialApiView.as_view()),
    path('material/create/', CreateMaterialApiView.as_view()),
    path('product/<uuid:pk>/', RetriveUpdateDestroyProductApiView.as_view()),
    path('product/create/', CreateProductApiView.as_view()),
    path('productmaterial/<uuid:pk>/', RetriveUpdateDestroyProducttMaterialApiView.as_view()),
    path('productmaterial/create/', CreateProductMaterialApiView.as_view()),
    path('warehouse/<int:pk>/', RetriveUpdateDestroyWareHouseApiView.as_view()),
    path('warehouse/create/', CreateWareHouseApiView.as_view()),
    path('request/', UserRequestApiView.as_view())

]