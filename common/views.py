import string
import secrets
from django.http import HttpResponse
from django.shortcuts import redirect
from common.models import ShortenedURL
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from urlshortner.settings import PROJECT_BASE_URL
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK


def response(status=HTTP_400_BAD_REQUEST, message=None, data=None):
    body = {
        'status': status,
        'message': message,
        'data': data
    }
    return Response(status=HTTP_200_OK, data=body, headers={'Cache-Control': 'no-cache'})


def generate_unique_short_url():
    # Define the characters you want to use for the short URL
    characters = string.ascii_letters + string.digits

    while True:
        # Generate a random 10-character short URL
        short_url = ''.join(secrets.choice(characters) for _ in range(10))

        # Check if the short URL is already in use
        if not ShortenedURL.objects.filter(short_url=short_url).exists():
            return short_url



class UrlShortnerViewSet(ViewSet):

    def create(self, request):
        original_url = request.data.get("url")
        short_url = generate_unique_short_url()

        db_url = ShortenedURL.objects.filter(original_url = original_url).values("short_url")
        if not db_url:
            ShortenedURL.objects.create(
                original_url=original_url,
                short_url=short_url
            )
        else:
            short_url = db_url[0]["short_url"]
        return response(201, "Success", {"short_url": PROJECT_BASE_URL + "/common/url?shrt_url=" + short_url})


    def list(self, request):
        payload = request.GET.dict()
        short_url = payload.get("shrt_url")
        db_url = ShortenedURL.objects.filter(short_url = short_url).values("original_url")
        if not db_url:
            return HttpResponse("<html><body><p>Wrong URL, URL Does not exist's.</p></body></html")
        return redirect(db_url[0]["original_url"])