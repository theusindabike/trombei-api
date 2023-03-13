from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from trombei_api.events.models import Event

FEED_LIST_URL = reverse("feeds:feed-list", kwargs={"version": "v1"})


class EventAPITest(APITestCase):
    fixtures = ["users.json", "places.json", "events.json"]

    def setUp(self):
        self.user_1 = User.objects.get(pk=1)
        self.user_2 = User.objects.get(pk=2)
        self.client = APIClient()

    def tearDown(self):
        self.client.force_authenticate(user=None)

    def test_feed_list(self):
        """
        Ensure we can list Events in a feed
        """

        event = Event.objects.get(id=8)

        url = reverse("feeds:feed-detail", kwargs={"version": "v1", "pk": event.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_feed_item(self):
        """
        Ensure we can get a feed item
        """

        response = self.client.get(FEED_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 6)

    def test_feed_filtered_by_title(self):
        """
        Ensure we can filter Events by title
        """

        response = self.client.get(FEED_LIST_URL, {"title": "title 11"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 1)

    def test_feed_filtered_by_place(self):
        """
        Ensure we can filter Events by title
        """

        response = self.client.get(
            FEED_LIST_URL, {"place": "00000000-0000-0000-0000-000000000002"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 3)
