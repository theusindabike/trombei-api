from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from trombei_api.filters import LoggedUserFilter  # , EventFilter
from trombei_api.places.models import Place, PlaceSerializer


class PlaceList(generics.ListCreateAPIView):
    queryset = Place.objects.all().order_by("id")
    serializer_class = PlaceSerializer
    filter_backends = [LoggedUserFilter, DjangoFilterBackend]
    # filterset_class = PlaceFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all().order_by("id")
    serializer_class = PlaceSerializer
    filter_backends = [LoggedUserFilter, DjangoFilterBackend]
    # filterset_class = PlaceFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
