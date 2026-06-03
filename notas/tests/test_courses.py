# notas/tests/test_courses.py
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .helpers import create_user, create_staff, auth_client, create_course

class CourseTests(TestCase):
    def setUp(self):
        self.user   = create_user('diego')
        self.staff  = create_staff()
        self.course = create_course('Seguridad Informática')

    def test_regular_user_cannot_create_course(self):
        resp = auth_client(self.user).post('/api/courses/', {
            'name': 'Redes', 'credits': 3
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_create_course(self):
        resp = auth_client(self.staff).post('/api/courses/', {
            'name': 'Sistemas Operativos', 'credits': 4
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_search_course_by_name(self):
        client = auth_client(self.user)
        resp = client.get('/api/courses/?search=Seguridad')
        self.assertEqual(resp.data['count'], 1)
        self.assertEqual(resp.data['results'][0]['name'], 'Seguridad Informática')