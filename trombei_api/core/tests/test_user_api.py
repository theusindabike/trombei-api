from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


USER_ME_URL = reverse("users:user-detail", kwargs={"version": "v1"})


class PlaceAPITest(APITestCase):
    fixtures = ["users.json", "places.json"]

    def setUp(self):
        self.user_1 = User.objects.get(pk=1)
        self.user_2 = User.objects.get(pk=2)
        self.admin_user = User.objects.get(pk=3)
        self.client = APIClient()

    def tearDown(self):
        self.client.force_authenticate(user=None)

    def test_get(self):
        """
        Ensure we can get a place object.
        """
        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(USER_ME_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
