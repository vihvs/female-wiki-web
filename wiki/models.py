from django.db import models


class Tag(models.Model):
    text = models.CharField(max_length=250)


class Page(models.Model):
    name = models.CharField(max_length=250)
    link = models.URLField()
    summary = models.TextField()
    tags = models.ManyToManyField(Tag)
