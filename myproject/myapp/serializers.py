from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Restaurant, Category, Testimonial, Gallery, Menu
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'role', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        # Validar contraseñas
        if self.context['request'].method == 'POST':
            if 'password' in attrs and 'confirm_password' in attrs:
                if attrs['password'] != attrs['confirm_password']:
                    raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
            # Validar si el correo ya está registrado
            if User.objects.filter(email=attrs['email']).exists():
                raise serializers.ValidationError({"email": "Este correo electrónico ya está registrado."})
        return attrs

    def create(self, validated_data):
        # Eliminar confirm_password y cifrar la contraseña antes de crear el usuario
        validated_data.pop('confirm_password', None)
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Cifrar la nueva contraseña si se proporciona
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Añadir el campo 'role' al token
        token['role'] = user.role
        return token