from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
import uuid


class User(AbstractUser):
    email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    photo = models.ImageField(upload_to="profile/%Y/%m/%d/", blank=True, null=True, verbose_name="Аватарка")
    date_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    thumbnail = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(200, 200)],
        format='JPEG',
        options={'quality': 80}
    )
