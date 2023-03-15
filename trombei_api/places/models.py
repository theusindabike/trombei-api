import uuid

from django.db import models

from django.conf import settings
from rest_framework import serializers


class Place(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="Places", on_delete=models.CASCADE
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
        Place, related_name="direction_urls", on_delete=models.CASCADE
    )
    type = models.CharField("type", max_length=32, choices=DirectionType.choices)
    url = models.URLField("url", max_length=512)
    unique_together = ["place", "type"]


class DirectionUrlSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, write_only=False)

    class Meta:
        model = DirectionUrl
        fields = ["id", "type", "url"]


class PlaceUserReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ["first_name", "email"]


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
            for d in direction_urls:
                DirectionUrl.objects.create(place=place, **d)
        return place

    def update(self, instance, validated_data):
        direction_urls = validated_data.pop("direction_urls")

        instance.name = validated_data.get("name", instance.name)
        instance.full_address = validated_data.get(
            "full_address", instance.full_address
        )
        instance.image = validated_data.get("image", instance.image)
        instance.save()

        remove_items = {item.id: item for item in instance.direction_urls.all()}

        for item in remove_items.values():
            item.delete()

        for d in direction_urls:
            DirectionUrl.objects.create(place=instance, **d)

        return instance
