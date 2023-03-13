from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from trombei_api.filters import LoggedUserFilter
from trombei_api.events.models import Event, EventSerializer


class EventList(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    filter_backends = [LoggedUserFilter, DjangoFilterBackend]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Event.objects.all().order_by("-date").filter(owner=self.request.user)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.all().order_by("-date").filter(owner=self.request.user)
