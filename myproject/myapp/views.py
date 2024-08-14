from rest_framework import viewsets, status
from .models import User, Restaurant, Category, Testimonial, Gallery, Menu
from .serializers import UserSerializer, RestaurantSerializer, CategorySerializer, TestimonialSerializer, GallerySerializer, MenuSerializer, MyTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters import rest_framework as filters

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # Si el serializer no es válido, devolver la respuesta con errores
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

class RestaurantFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='category__id')

    class Meta:
        model = Restaurant
        fields = ['category']

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RestaurantFilter

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        if 'is_active' in data:
            instance.is_active = data['is_active']
        return super().partial_update(request, *args, **kwargs)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        if 'is_active' in data:
            instance.is_active = data['is_active']
        return super().partial_update(request, *args, **kwargs)

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        if 'is_active' in data:
            instance.is_active = data['is_active']
        return super().partial_update(request, *args, **kwargs)

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        if 'is_active' in data:
            instance.is_active = data['is_active']
        return super().partial_update(request, *args, **kwargs)

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        if 'is_active' in data:
            instance.is_active = data['is_active']
        return super().partial_update(request, *args, **kwargs)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer