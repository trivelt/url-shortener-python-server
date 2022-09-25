from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import URL
from .serializers import URLSerializer, FullURLSerializer
from .generator import generate_short_url

class URLApiView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', 'post']
    serializer_class = URLSerializer

    def get(self, request, *args, **kwargs):
        short_link = request.query_params.get("short")
        print("GET CALLED, short link=", short_link)
        if short_link is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # return Response(status=status.HTTP_200_OK)
        url = URL.objects.filter(short=short_link).first()
        print("WE HAVE URL: ", url)
        serializer = FullURLSerializer(url, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        print("POST CALLED")
        long_url = request.data.get('long')
        data = {
            'long': long_url,
            'short': generate_short_url(long_url)
        }
        serializer = FullURLSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
