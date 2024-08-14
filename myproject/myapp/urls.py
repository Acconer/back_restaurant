from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RestaurantViewSet, CategoryViewSet, TestimonialViewSet, GalleryViewSet, MenuViewSet, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'testimonials', TestimonialViewSet)
router.register(r'galleries', GalleryViewSet)
router.register(r'menus', MenuViewSet)  # Asegúrate de que el nombre de la ruta sea coherente

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
