# notas/tests/test_periods.py
from django.test import TestCase
from rest_framework import status
from .helpers import create_user, create_staff, auth_client, create_period

class PeriodPermissionTests(TestCase):
    def setUp(self):
        self.user   = create_user('julian')
        self.staff  = create_staff()
        self.period = create_period()

    def test_authenticated_user_can_list(self):
        resp = auth_client(self.user).get('/api/periods/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_regular_user_cannot_create(self):
        resp = auth_client(self.user).post('/api/periods/', {
            'name': '2026-B', 'start_date': '2026-09-01', 'end_date': '2027-02-01'
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_create(self):
        resp = auth_client(self.staff).post('/api/periods/', {
            'name': '2026-B', 'start_date': '2026-09-01', 'end_date': '2027-02-01'
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)