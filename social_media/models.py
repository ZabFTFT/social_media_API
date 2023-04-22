import os
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify



def get_image_file_name(instance, filename):
    _, extension = os.path.splitext(filename)
    new_name_image_file = (
        f"{slugify(instance.first_name)}-{slugify(instance.last_name)}-{uuid.uuid4()}.{extension}"
    )
    return os.path.join("uploads/movies/", new_name_image_file)


class UserProfile(models.Model):
    username = models.CharField(max_length=20, default="")
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    mobile_number = models.SmallIntegerField(null=True)
    photo_image = models.ImageField(null=True, upload_to=get_image_file_name, default="")



class Relationship(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')




