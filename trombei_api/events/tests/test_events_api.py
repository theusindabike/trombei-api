from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from trombei_api.events.models import Event

EVENT_CREATE_AND_LIST_URL = reverse("events:event-list", kwargs={"version": "v1"})


class EventAPITest(APITestCase):
    fixtures = ["users.json", "places.json", "events.json"]

    def setUp(self):
        self.user_1 = User.objects.get(pk=1)
        self.user_2 = User.objects.get(pk=2)
        self.client = APIClient()

    def tearDown(self):
        self.client.force_authenticate(user=None)

    def test_get(self):
        """
        Ensure we can get a event object.
        """
        event = Event.objects.get(id=1)

        self.client.force_authenticate(user=self.user_1)

        url = reverse("events:event-detail", kwargs={"version": "v1", "pk": event.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get("id"), "00000000-0000-0000-0000-000000000001"
        )
        self.assertEqual(response.data.get("title"), "event title 1")
        self.assertEqual(response.data.get("owner").get("username"), "user_1")
        self.assertEqual(response.data.get("place").get("name"), "Tábuas Bar")
        self.assertEqual(
            response.data.get("place").get("full_address"),
            "Av. Santa Isabel, 57 - Barão Geraldo, Campinas - SP, 13084-012",
        )

    def test_list(self):
        """
        Ensure we can list all logged user events
        """
        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(EVENT_CREATE_AND_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 9)

    def test_create(self):
        """
        Ensure we can create a Event
        """
        self.client.force_authenticate(user=self.user_1)

        data = {
            "title": "event title",
            "content": "event content",
            "place_id": "00000000-0000-0000-0000-000000000001",
            "date": datetime(2022, 4, 1),
            "status": Event.EventStatus.DRAFT,
        }

        response = self.client.post(EVENT_CREATE_AND_LIST_URL, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("title"), data["title"])
