from django.urls import include, re_path, path
from rest_framework.routers import DefaultRouter
from common.views import UrlShortnerViewSet

route = DefaultRouter(trailing_slash=False)

route.register(r'url', UrlShortnerViewSet, basename ='url')


urlpatterns = [
    re_path(r'^', include(route.urls))
    ] 