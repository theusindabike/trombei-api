from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from trombei_api.filters import FeedFilter
from trombei_api.events.models import Event, EventSerializer


class FeedList(generics.ListAPIView):
    queryset = (
        Event.objects.prefetch_related("place")
        .filter(status=Event.EventStatus.PUBLISHED)
        .order_by("-created_at")
    )
    serializer_class = EventSerializer
    filterset_class = FeedFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
