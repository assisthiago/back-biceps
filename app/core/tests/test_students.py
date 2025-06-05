from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.core.models import Student


class StudentViewSetTests(APITestCase):

    fixtures = settings.FIXTURE_DIRS

    def setUp(self):
        self.url_list = reverse("student-list")

    def test_student_create(self):
        data = {
            "first_name": "student",
            "last_name": "test",
            "username": "student@test.com",
            "email": "student@test.com",
            "password": "studenttest123",
        }
        self.client.post(reverse("user-list"), data, format="json")
        response = self.client.post(
            self.url_list, data={"user_email": "student@test.com"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_list_unauthorized(self):
        response = self.client.get(self.url_list, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_student_list_not_found(self):
        Student.objects.all().delete()  # Ensure no students exist
        self.client.login(username="test@user.com", password="admin")
        response = self.client.get(self.url_list, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_student_list(self):
        self.client.login(username="test@user.com", password="admin")
        response = self.client.get(self.url_list, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_retrieve_not_found(self):
        Student.objects.all().delete()  # Ensure no students exist
        url = reverse("student-detail", kwargs={"pk": 1})
        self.client.login(username="test@user.com", password="admin")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_student_retrieve(self):
        url = reverse("student-detail", kwargs={"pk": 1})
        self.client.login(username="test@user.com", password="admin")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
