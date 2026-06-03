# notas/views/__init__.py
from .health import health_check
from .auth import RegisterView, LogoutView
from .user import UserViewSet
from .period import AcademicPeriodViewSet
from .course import CourseViewSet
from .student import StudentViewSet
from .enrollment import EnrollmentViewSet
from .grade import GradeViewSet