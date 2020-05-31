from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Link(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    url = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    image_url = models.CharField(max_length=500)
    tags = TaggableManager()

    def __str__(self):
        return self.title
