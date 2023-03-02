from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from trombei_api.filters import LoggedUserFilter
from trombei_api.events.models import Event, EventSerializer


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by("-created_at")
    serializer_class = EventSerializer
    filter_backends = [LoggedUserFilter, DjangoFilterBackend]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all().order_by("id")
    serializer_class = EventSerializer
    filter_backends = [LoggedUserFilter, DjangoFilterBackend]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
