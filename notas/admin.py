# notas/admin.py
from django.contrib import admin
from notas.models import AcademicPeriod, Course, Student, Enrollment, Grade

@admin.register(AcademicPeriod)
class AcademicPeriodAdmin(admin.ModelAdmin):
    list_display  = ['id', 'name', 'start_date', 'end_date', 'is_active']
    list_filter   = ['is_active']
    search_fields = ['name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display  = ['id', 'name', 'credits', 'is_active']
    list_filter   = ['is_active']
    search_fields = ['name', 'description']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display  = ['id', 'user', 'enrollment_number']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'enrollment_number']

class GradeInline(admin.TabularInline):
    model  = Grade
    extra  = 0
    fields = ['evaluation_type', 'score', 'observations']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display  = ['id', 'student', 'course', 'period', 'created_at']
    list_filter   = ['period', 'course']
    search_fields = ['student__user__username', 'student__enrollment_number', 'course__name']
    inlines       = [GradeInline]

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display  = ['id', 'enrollment', 'evaluation_type', 'score', 'created_at']
    list_filter   = ['evaluation_type', 'enrollment__course']
    search_fields = ['enrollment__student__user__username', 'enrollment__student__enrollment_number']