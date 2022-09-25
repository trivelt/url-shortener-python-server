from django.db import models


class URL(models.Model):
    id = models.AutoField(primary_key=True)
    long = models.CharField(max_length=1024)
    short = models.CharField(max_length=128)
