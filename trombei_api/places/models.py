import uuid

from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers


class Place(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        "auth.User", related_name="Places", on_delete=models.CASCADE
    )
    name = models.CharField("name", max_length=128)
    full_address = models.CharField("full_address", max_length=255)
    image = models.ImageField(upload_to="places", blank=True, null=True)
    created_at = models.DateTimeField("created_at", auto_now_add=True)

    def __str__(self):
        return self.name


class DirectionUrl(models.Model):
    class DirectionType(models.TextChoices):
        GOOGLE_MAPS = "GOOGLE-MAPS"
        UBER = "UBER"

    place = models.ForeignKey(
        "places.Place", on_delete=models.CASCADE, related_name="direction_urls"
    )
    type = models.CharField("type", max_length=32, choices=DirectionType.choices)
    url = models.URLField("url", max_length=512)
    unique_together = ["place", "type"]


class DirectionUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectionUrl
        fields = ["type", "url"]
        # fields = "__all__"


class PlaceUserReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class PlaceSerializer(serializers.ModelSerializer):
    owner = PlaceUserReadOnlySerializer(many=False, read_only=True)
    direction_urls = DirectionUrlSerializer(many=True, required=False)

    class Meta:
        model = Place
        fields = [
            "id",
            "name",
            "full_address",
            "image",
            "owner",
            "direction_urls",
            "created_at",
        ]

    def create(self, validated_data):
        direction_urls = validated_data.pop("direction_urls", None)
        place = Place.objects.create(**validated_data)

        if direction_urls is not None:
            for url in direction_urls:
                DirectionUrl.objects.create(place=place, **url)
        return place
