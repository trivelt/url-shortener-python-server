from rest_framework import serializers
from .models import URL


class LongURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ["long"]


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ["long", "short"]
