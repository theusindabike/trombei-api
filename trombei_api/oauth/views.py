from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

import urllib.parse


class GoogleLoginView(SocialLoginView):
    class GoogleAdapter(GoogleOAuth2Adapter):
        access_token_url = "https://oauth2.googleapis.com/token"
        authorize_url = "https://accounts.google.com/o/oauth2/v2/auth"
        profile_url = "https://www.googleapis.com/oauth2/v2/userinfo"

    adapter_class = GoogleAdapter
    # adapter_class = GoogleOAuth2Adapter
    # callback_url = settings.SOCIALACCOUNT_PROVIDERS["google"]["CALLBACK_URL"]
    callback_url = "http://localhost/api/v1/oauth/code/"
    client_class = OAuth2Client


@api_view(["GET"])
def CodeView(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == "GET":
        code = urllib.parse.unquote(request.query_params["code"])
        return Response({"code": code})
