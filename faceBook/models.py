from __future__ import unicode_literals

from django.db import models


class Face(models.Model):
    face = models.ImageField(upload_to="faceBook", blank=True, default=None, null=True)
    face_id = models.CharField(max_length=255, default="", blank=True)
    age = models.FloatField(default="18", blank=True)
    emotion = models.CharField(max_length=50, default="Undetected emotion")

class FaceTempPhoto(models.Model):
    photo = models.ImageField(upload_to="faceTempPhoto")

class Tempfaces(models.Model):
    face_list = models.ManyToManyField(Face, related_name="tempfaces")
    temp_photo = models.ForeignKey(FaceTempPhoto)

# Create your models here.
