from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

import urllib.parse


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.SOCIALACCOUNT_PROVIDERS["google"]["CALLBACK_URL"]
    client_class = OAuth2Client


@api_view(["GET"])
def CodeView(request):
    if request.method == "GET":
        code = urllib.parse.unquote(request.query_params["code"])
        return Response({"code": code})
