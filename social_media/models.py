import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


def get_image_file_name(instance, filename):
    _, extension = os.path.splitext(filename)
    new_name_image_file = (
        f"{slugify(instance.title)}-{uuid.uuid4()}.{extension}"
    )
    return os.path.join("uploads/movies/", new_name_image_file)


class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile_number = models.SmallIntegerField()
    photo_image = models.ImageField(null=True, upload_to=get_image_file_name)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)