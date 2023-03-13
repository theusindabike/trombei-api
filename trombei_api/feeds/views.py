from rest_framework import generics
from rest_framework.permissions import AllowAny
from trombei_api.filters import FeedFilter
from trombei_api.events.models import Event, EventSerializer


class FeedList(generics.ListAPIView):
    queryset = (
        Event.objects.prefetch_related("place")
        .filter(status=Event.EventStatus.PUBLISHED)
        .order_by("-date")
    )
    serializer_class = EventSerializer
    filterset_class = FeedFilter
    permission_classes = [AllowAny]


class FeedRetrieve(generics.RetrieveAPIView):
    queryset = (
        Event.objects.prefetch_related("place")
        .filter(status=Event.EventStatus.PUBLISHED)
        .order_by("-date")
    )
    serializer_class = EventSerializer
    filterset_class = FeedFilter
    permission_classes = [AllowAny]
