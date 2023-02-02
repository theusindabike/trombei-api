from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from trombei_api.places.models import Place

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
        Ensure we can add mutiples directions urls
        """

        self.client.force_authenticate(user=self.user_1)

        data = {
            "name": "Casa theus e bia",
            "full_address": "Rua de casa",
            "direction_urls": [
                {
                    "type": "GOOGLE-MAPS",
                    "url": "https://www.google.com/maps/dir//tabuas+bar+barao+geraldo/data=!4m6!4m5!1m1!4e2!1m2!1m1!1s0x94c8c6c80e5e0b9d:0xd339581ddbdc8fe5?sa=X&ved=2ahUKEwjMnYfl-_D8AhVIrpUCHc7YAt0Q9Rd6BAhhEAU",
                },
                {
                    "type": "UBER",
                    "url": "https://m.uber.com/ul/?client_id=123&action=setPickup&pickup[latitude]=37.775818&pickup[longitude]=-122.418028&pickup[nickname]=UberHQ&pickup[formatted_address]=1455%20Market%20St%2C%20San%20Francisco%2C%20CA%2094103&dropoff[latitude]=37.802374&dropoff[longitude]=-122.405818&dropoff[nickname]=Coit%20Tower&dropoff[formatted_address]=1%20Telegraph%20Hill%20Blvd%2C%20San%20Francisco%2C%20CA%2094133&product_id=a1111c8c-c720-46c3-8534-2fcdd730040d",
                },
            ],
        }
        response = self.client.post(PLACE_CREATE_AND_LIST_URL, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("direction_urls"), data["direction_urls"])
