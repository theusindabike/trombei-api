import uuid

from django.db import models
from rest_framework import serializers
from django.conf import settings

from trombei_api.places.models import Place, PlaceSerializer


class Event(models.Model):
    class EventStatus(models.TextChoices):
        DRAFT = "DRAFT"
        PUBLISHED = "PUBLISHED"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="Events", on_delete=models.CASCADE
    )
    title = models.CharField("title", max_length=128)
    content = models.CharField("content", max_length=255)
    place = models.ForeignKey(
        "places.Place", on_delete=models.SET_NULL, null=True, blank=True
    )
    date = models.DateTimeField("date")
    status = models.CharField("type", max_length=32, choices=EventStatus.choices)
    created_at = models.DateTimeField("created at", auto_now_add=True)

    def __str__(self):
        return self.title


class EventUserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ("first_name", "email")


class EventSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source="owner.username")
    owner = EventUserReadSerializer(many=False, read_only=True)
    place_id = serializers.PrimaryKeyRelatedField(
        queryset=Place.objects.all(), source="place", many=False
    )
    place = PlaceSerializer(many=False, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "content",
            "place_id",
            "place",
            "date",
            "status",
            "owner",
            "created_at",
        ]
