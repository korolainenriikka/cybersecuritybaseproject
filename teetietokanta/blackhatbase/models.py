from django.db import models

# Create your models here.

class Content(models.Model):
    content = models.CharField(max_length=200)
  