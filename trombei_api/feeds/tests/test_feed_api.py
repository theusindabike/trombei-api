from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from trombei_api.events.models import Event
from trombei_api.places.models import Place

from datetime import datetime, timedelta
import pytz

FEED_LIST_URL = reverse("feeds:feed-list", kwargs={"version": "v1"})
PAST_FEED_LIST_URL = reverse("feeds:past-feed-list", kwargs={"version": "v1"})

SETTINGS_TZ = pytz.timezone(settings.TIME_ZONE)


class EventAPITest(APITestCase):
    fixtures = ["users.json", "places.json", "events.json"]

    def setUp(self):
        self.user_1 = User.objects.get(pk=1)
        self.user_2 = User.objects.get(pk=2)
        self.client = APIClient()

        self.place_1 = Place.objects.get(pk=1)

        today = datetime.now(tz=SETTINGS_TZ)

        self.event_1 = Event.objects.create(
            owner=self.user_1,
            title="Next Cool Event 1",
            place=self.place_1,
            date=today + timedelta(days=3),
            status=Event.EventStatus.PUBLISHED,
        )

        self.event_2 = Event.objects.create(
            owner=self.user_1,
            title="Next Cool Event 2",
            place=self.place_1,
            date=today + timedelta(days=5),
            status=Event.EventStatus.PUBLISHED,
        )

    def tearDown(self):
        self.client.force_authenticate(user=None)

    def test_feed_list(self):
        """
        Ensure we can get a feed item
        """

        response = self.client.get(FEED_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 2)
        self.assertEqual(
            response.data.get("results")[0].get("title"), self.event_1.title
        )
        self.assertEqual(
            response.data.get("results")[1].get("title"), self.event_2.title
        )

    def test_feed_detail(self):
        """
        Ensure we can list Events in a feed
        """

        event = Event.objects.get(id=8)

        url = reverse("feeds:feed-detail", kwargs={"version": "v1", "pk": event.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_feed_filtered_by_title(self):
        """
        Ensure we can filter Events by title
        """

        response = self.client.get(FEED_LIST_URL, {"title": "Next Cool Event 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 1)

    def test_feed_filtered_by_place(self):
        """
        Ensure we can filter Events by title
        """

        response = self.client.get(FEED_LIST_URL, {"place": self.place_1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 2)
