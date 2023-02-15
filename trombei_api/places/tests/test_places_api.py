from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from trombei_api.places.models import Place, DirectionUrl

PLACE_CREATE_AND_LIST_URL = reverse("places:place-list", kwargs={"version": "v1"})


class PlaceAPITest(APITestCase):
    fixtures = ["users.json", "places.json"]

    def setUp(self):
        self.user_1 = User.objects.get(pk=1)
        self.user_2 = User.objects.get(pk=2)
        self.client = APIClient()

    def tearDown(self):
        self.client.force_authenticate(user=None)

    def test_get(self):
        """
        Ensure we can get a place object.
        """

        place = Place.objects.get(id="00000000-0000-0000-0000-000000000003")

        self.client.force_authenticate(user=self.user_2)

        url = reverse("places:place-detail", kwargs={"version": "v1", "pk": place.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get("id"), "00000000-0000-0000-0000-000000000003"
        )
        self.assertEqual(response.data.get("name"), "Hoppie Tap House")
        self.assertEqual(
            response.data.get("full_address"),
            "R. Waldomiro Martini, 98 - Centro, Mogi Guaçu - SP, 13840-054",
        )
        self.assertEqual(response.data.get("owner").get("username"), "user_2")

    def test_list(self):
        """
        Ensure we can list all logged user places
        """
        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(PLACE_CREATE_AND_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 2)

    def test_create(self):
        """
        Ensure we can create a Place
        """
        self.client.force_authenticate(user=self.user_1)

        data = {"name": "Casa theus e bia", "full_address": "Rua de casa"}
        response = self.client.post(PLACE_CREATE_AND_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("name"), data["name"])

    def test_delete(self):
        """
        Ensure we can delete a Place
        """
        self.client.force_authenticate(user=self.user_1)

        data = {"name": "Casa theus e bia", "full_address": "Rua de casa"}
        response = self.client.post(PLACE_CREATE_AND_LIST_URL, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("name"), data["name"])

        url = reverse(
            "places:place-detail",
            kwargs={"version": "v1", "pk": response.data.get("id")},
        )
        delete_response = self.client.delete(url)

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_direction_urls(self):
        """
        Ensure we can add mutiples direction urls
        """

        self.client.force_authenticate(user=self.user_1)

        data = {
            "name": "Casa João e Maria",
            "full_address": "Rua da casa do João e a Maria",
            "direction_urls": [
                {
                    "type": "GOOGLE-MAPS",
                    "url": "https://www.google.com/1",
                },
                {
                    "type": "UBER",
                    "url": "https://m.uber.com/ul/2",
                },
            ],
        }
        response = self.client.post(PLACE_CREATE_AND_LIST_URL, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data.get("direction_urls")), 2)

    def test_add_direction_urls_to_an_existing_place(self):
        """
        Ensure we can add directions urls to a existing place
        """

        place = Place.objects.get(id="00000000-0000-0000-0000-000000000001")

        self.client.force_authenticate(user=self.user_1)

        url = reverse("places:place-detail", kwargs={"version": "v1", "pk": place.id})

        existing_place = self.client.get(url).data

        direction_urls = [
            {
                "type": "GOOGLE-MAPS",
                "url": "https://www.google.com/3",
            },
            {
                "type": "UBER",
                "url": "https://m.uber.com/ul/4",
            },
        ]

        existing_place["direction_urls"] = direction_urls

        url = reverse("places:place-detail", kwargs={"version": "v1", "pk": place.id})

        response = self.client.put(url, data=existing_place)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), str(place.id))
        self.assertEqual(len(response.data.get("direction_urls")), 2)

    def test_update_direction_urls_and_place(self):
        """
        Ensure we can update directions urls and place
        """

        self.client.force_authenticate(user=self.user_1)

        place_with_directions = {
            "name": "Place Name 1",
            "full_address": "Full Address 1",
            "direction_urls": [
                {
                    "type": DirectionUrl.DirectionType.GOOGLE_MAPS,
                    "url": "https://www.google.com/5",
                }
            ],
        }
        response = self.client.post(
            PLACE_CREATE_AND_LIST_URL, data=place_with_directions
        )
        existing_place = response.data

        updated_place_name = "Place Name 2"
        updated_direction_urls = [
            {
                "type": DirectionUrl.DirectionType.GOOGLE_MAPS,
                "url": "https://www.google.com/6",
            },
            {
                "type": DirectionUrl.DirectionType.UBER,
                "url": "https://www.uber.com/7",
            },
        ]

        existing_place["direction_urls"] = updated_direction_urls
        existing_place["name"] = updated_place_name

        url = reverse(
            "places:place-detail",
            kwargs={"version": "v1", "pk": existing_place.get("id")},
        )

        response = self.client.put(url, data=existing_place)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), str(existing_place.get("id")))
        self.assertEqual(response.data.get("name"), updated_place_name)
        self.assertEqual(len(response.data.get("direction_urls")), 2)
