# notas/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from notas.views.health    import health_check
from notas.views.auth      import RegisterView, LogoutView
from notas.views.user      import UserViewSet
from notas.views.category  import CategoryViewSet
from notas.views.product   import ProductViewSet
from notas.views.order     import OrderViewSet
from notas.serializers.auth import CustomTokenView

router = DefaultRouter()
router.register('users',      UserViewSet,     basename='user')
router.register('categories', CategoryViewSet, basename='category')
router.register('products',   ProductViewSet,  basename='product')
router.register('orders',     OrderViewSet,    basename='order')

urlpatterns = [
    path('health/',             health_check),
    path('auth/register/',      RegisterView.as_view()),
    path('auth/login/',         CustomTokenView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/token/verify/',  TokenVerifyView.as_view()),
    path('auth/logout/',        LogoutView.as_view()),
    path('', include(router.urls)),
]