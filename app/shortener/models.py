from django.db import models
from app.shortener.generator import get_index_from_short_url

class URL(models.Model):
    id = models.AutoField(primary_key=True)
    long = models.CharField(max_length=1024)
    short = models.CharField(max_length=128)

    @staticmethod
    def from_short_link(url: str) -> 'URL':
        return URL.objects.filter(id=get_index_from_short_url(url)).first()

    @staticmethod
    def next_index() -> int:
        return URL.objects.count() + 1  # because db indices start at 1
