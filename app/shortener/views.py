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
from .generator import generate_short_url, get_index_from_short_url


class MessageParam:
    SHORT_URL = "short"
    LONG_URL = "long"
    ERROR = "error"


class URLApiView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', 'post']
    serializer_class = LongURLSerializer

    def get(self, request, *args, **kwargs):
        short_link = request.query_params.get(MessageParam.SHORT_URL)
        if short_link is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # TODO: Add validation https://docs.djangoproject.com/en/4.1/ref/validators/
        # TODO: Add extensive tests of this API

        url = URL.objects.filter(id=get_index_from_short_url(short_link)).first()
        if not url:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = URLSerializer(url, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        long_url = request.data.get(MessageParam.LONG_URL)
        try:
            URLValidator()(long_url)
        except ValidationError as e:
            return Response(data={MessageParam.ERROR: e.message}, status=status.HTTP_400_BAD_REQUEST)

        url = URL.objects.create(long=long_url, short=generate_short_url(URL.next_index()))
        return Response(URLSerializer(url).data, status=status.HTTP_201_CREATED)


class ShortURLRedirectView(View):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        short_link = request.path[1:]
        url = URL.objects.filter(id=get_index_from_short_url(short_link)).first()
        if not url:
            return render(request, "shortener/404.html", status=status.HTTP_404_NOT_FOUND)

        return redirect(url.long)
