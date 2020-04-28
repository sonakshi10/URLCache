from django.db import models
from taggit.managers import TaggableManager

# Create your models here.
class Link(models.Model):
	url=models.CharField(max_length=500)
	title=models.CharField(max_length=500)
	image_url=models.CharField(max_length=500)
	tags=TaggableManager()

	def __str__(self):
		return self.title
