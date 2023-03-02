from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from trombei_api.places.models import Place, PlaceSerializer


class PlaceCreate(generics.CreateAPIView):
    queryset = Place.objects.all().order_by("id")
    serializer_class = PlaceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlaceList(generics.ListAPIView):
    queryset = Place.objects.all().order_by("id")
    serializer_class = PlaceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class PlaceRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all().order_by("id")
    serializer_class = PlaceSerializer
    # filterset_class = PlaceFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class RetrieveDeletePlace(generics.GenericAPIView):
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = self.get_object_or_404()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        permission_classes = [IsAuthenticated, IsAdminUser]
        instance = self.get_object_or_404()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
