from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from allauth.socialaccount.models import SocialAccount


class UserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        data = SocialAccount.objects.get(user=request.user).extra_data
        return JsonResponse(data)
