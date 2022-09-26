from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import View
from .models import URL
from .serializers import LongURLSerializer, URLSerializer
from .generator import generate_short_url

from urllib.parse import urlsplit


class MessageParam:
    SHORT_LINK = "short"
    LONG_LINK = "long"
    ERROR = "error"


class URLApiView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', 'post']
    serializer_class = LongURLSerializer

    def get(self, request, *args, **kwargs):
        shortcut = request.query_params.get(MessageParam.SHORT_LINK)
        if shortcut is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        url = URL.from_shortcut(shortcut)
        if not url:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(URLSerializer(url).data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        long_url = request.data.get(MessageParam.LONG_LINK)
        try:
            URLValidator()(long_url)
        except ValidationError as e:
            return Response(data={MessageParam.ERROR: e.message}, status=status.HTTP_400_BAD_REQUEST)

        url = URL.objects.create(long=long_url, short=generate_short_url(self._base_url(request), URL.next_index()))
        return Response(URLSerializer(url).data, status=status.HTTP_201_CREATED)

    def _base_url(self, request) -> str:
        splitted_url = urlsplit(request.build_absolute_uri())
        return f"{splitted_url.scheme}://{splitted_url.netloc}"


class ShortURLRedirectView(View):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        url = URL.from_shortcut(request.path[1:])
        if not url:
            return render(request, "shortener/404.html", status=status.HTTP_404_NOT_FOUND)

        return redirect(url.long)
