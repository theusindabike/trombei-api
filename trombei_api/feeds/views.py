from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import AllowAny
from trombei_api.filters import FeedFilter
from trombei_api.events.models import Event, EventSerializer


from datetime import datetime, timedelta
import pytz

SETTINGS_TZ = pytz.timezone(settings.TIME_ZONE)


class FeedList(generics.ListAPIView):
    today = datetime.now(tz=SETTINGS_TZ)

    queryset = (
        Event.objects.prefetch_related("place")
        .filter(
            status=Event.EventStatus.PUBLISHED,
            date__gt=today + timedelta(hours=-12),
        )
        .order_by("date")
    )
    serializer_class = EventSerializer
    filterset_class = FeedFilter
    permission_classes = [AllowAny]


class PastFeedList(generics.ListAPIView):
    queryset = (
        Event.objects.prefetch_related("place")
        .filter(
            status=Event.EventStatus.PUBLISHED,
        )
        .order_by("date")
    )
    serializer_class = EventSerializer
    filterset_class = FeedFilter
    permission_classes = [AllowAny]


class FeedRetrieve(generics.RetrieveAPIView):
    queryset = (
        Event.objects.prefetch_related("place")
        .filter(status=Event.EventStatus.PUBLISHED)
        .order_by("date")
    )
    serializer_class = EventSerializer
    filterset_class = FeedFilter
    permission_classes = [AllowAny]
