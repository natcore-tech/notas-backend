# notas/tests/test_grades.py
from django.test import TestCase
from rest_framework import status
from .helpers import (
    create_user, create_staff, auth_client, 
    create_period, create_course, create_student, 
    create_enrollment, create_grade
)

class GradeBusinessLogicTests(TestCase):
    def setUp(self):
        self.staff    = create_staff()
        self.user     = create_user('edison')
        self.student  = create_student(self.user)
        self.course   = create_course()
        self.period   = create_period()
        self.enroll   = create_enrollment(self.student, self.course, self.period)
        self.client   = auth_client(self.staff)

    def test_cannot_create_grade_over_20(self):
        resp = self.client.post('/api/grades/', {
            'enrollment': self.enroll.id,
            'evaluation_type': 'parcial_1',
            'score': '25.00'
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('score', resp.data)

    def test_cannot_create_negative_grade(self):
        resp = self.client.post('/api/grades/', {
            'enrollment': self.enroll.id,
            'evaluation_type': 'parcial_1',
            'score': '-5.00'
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_duplicate_evaluation_type(self):
        create_grade(self.enroll, evaluation_type='parcial_1', score=15.00)
        resp = self.client.post('/api/grades/', {
            'enrollment': self.enroll.id,
            'evaluation_type': 'parcial_1',
            'score': '18.00'
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

class GradePermissionTests(TestCase):
    def setUp(self):
        self.user1    = create_user('david')
        self.student1 = create_student(self.user1, 'UTE-101')
        
        self.user2    = create_user('hacker')
        self.student2 = create_student(self.user2, 'UTE-999')
        
        self.enroll   = create_enrollment(self.student1, create_course(), create_period())
        self.grade    = create_grade(self.enroll)

    def test_student_can_see_own_grades(self):
        resp = auth_client(self.user1).get(f'/api/grades/{self.grade.id}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_student_cannot_see_others_grades(self):
        resp = auth_client(self.user2).get(f'/api/grades/{self.grade.id}/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_regular_student_cannot_create_grades(self):
        resp = auth_client(self.user1).post('/api/grades/', {
            'enrollment': self.enroll.id,
            'evaluation_type': 'parcial_2',
            'score': '20.00'
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)