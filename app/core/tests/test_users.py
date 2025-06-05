from django.conf import settings
from django.urls import reverse
from rest_framework.test import APITestCase


class UserViewSetTests(APITestCase):

    fixtures = settings.FIXTURE_DIRS

    def setUp(self):
        self.url_list = reverse("user-list")

    def test_user_create(self):
        data = {
            "first_name": "user",
            "last_name": "test",
            "username": "user@test.com",
            "email": "user@test.com",
            "password": "usertest123",
        }
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_user_list_unauthorized(self):
        response = self.client.get(self.url_list, format="json")
        self.assertEqual(response.status_code, 401)

    def test_user_list(self):
        self.client.login(username="test@user.com", password="admin")
        response = self.client.get(self.url_list, format="json")
        self.assertEqual(response.status_code, 200)

    def test_user_retrieve(self):
        url = reverse("user-detail", kwargs={"pk": 1})
        self.client.login(username="test@user.com", password="admin")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
