from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model

class User(AbstractUser):
    email = models.EmailField(unique=True)
    # Agregar rol mediante grupos
    USER_ROLES = (
        (1, 'Admin'),  # Rol para gestionar restaurantes
        (2, 'User'),   # Rol para dejar opiniones
    )
    role = models.PositiveSmallIntegerField(choices=USER_ROLES, default=2)
    
    # Cambiar los nombres de los campos related_name para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  
        blank=True,
        help_text='Los grupos a los que pertenece este usuario.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Permisos específicos para este usuario.',
        verbose_name='user permissions',
    )

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    description = models.TextField()
    image = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)  # Agregar campo is_active

class Category(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # Agregar campo is_active

class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Referencia al usuario que deja la opinión
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  # Referencia al restaurante
    testimonial = models.TextField()
    rating = models.IntegerField()
    is_active = models.BooleanField(default=True)  # Agregar campo is_active

class Gallery(models.Model):
    image_url = models.URLField()
    description = models.TextField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)  # Añadido 'null=True'
    is_active = models.BooleanField(default=True)  # Agregar campo is_active


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  # Relación con el restaurante
    menu_image_url = models.URLField()  # Imagen del menú
    is_active = models.BooleanField(default=True)  # Agregar campo is_active
