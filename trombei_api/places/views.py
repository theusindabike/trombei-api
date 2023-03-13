from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from trombei_api.places.models import Place, PlaceSerializer


class PlaceListCreate(generics.ListCreateAPIView):
    queryset = Place.objects.all().order_by("id")
    serializer_class = PlaceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_permissions(self):
        if self.request.method in ["POST"]:
            return [IsAdminUser()]
        return []

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlaceRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all().order_by("id")
    serializer_class = PlaceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAdminUser()]
        return []
