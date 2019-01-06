from django.db import models


class Tag(models.Model):
    text = models.CharField(max_length=250)

    def __str__(self):
        return self.text


class Page(models.Model):
    name = models.CharField(max_length=250)
    link = models.URLField()
    summary = models.TextField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
