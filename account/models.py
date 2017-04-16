from django.db import models
from django.contrib.auth.models import AbstractUser
from faceBook.models import Face


class AccountUser(AbstractUser):
    face_book = models.ManyToManyField(Face, related_name="user_face")
    person_id = models.CharField(max_length=255, default="", blank=True)
    portrait = models.ImageField(upload_to="portrait", blank=True, default=None, null=True)

# Create your models here.
