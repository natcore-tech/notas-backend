# notas/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from notas.views.health     import health_check
from notas.views.auth       import RegisterView, LogoutView
from notas.views.user       import UserViewSet
from notas.views.period     import AcademicPeriodViewSet
from notas.views.course     import CourseViewSet
from notas.views.student    import StudentViewSet
from notas.views.enrollment import EnrollmentViewSet
from notas.views.grade      import GradeViewSet
from notas.serializers.auth import CustomTokenView

# Configuración del Router para los ViewSets (CRUD automáticos)
router = DefaultRouter()
router.register('users',       UserViewSet,           basename='user')
router.register('periods',     AcademicPeriodViewSet, basename='period')
router.register('courses',     CourseViewSet,         basename='course')
router.register('students',    StudentViewSet,        basename='student')
router.register('enrollments', EnrollmentViewSet,     basename='enrollment')
router.register('grades',      GradeViewSet,          basename='grade')

urlpatterns = [
    # Verificación de estado del servidor
    path('health/',             health_check),
    
    # Endpoints de Autenticación (JWT)
    path('auth/register/',      RegisterView.as_view()),
    path('auth/login/',         CustomTokenView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/token/verify/',  TokenVerifyView.as_view()),
    path('auth/logout/',        LogoutView.as_view()),
    
    # Inclusión de todas las rutas del router
    path('', include(router.urls)),
]