from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from django.contrib.auth import get_user_model


class Profile(models.Model):
    date_birthday = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    photo = models.ImageField(upload_to="profile/%Y/%m/%d/", verbose_name="Аватарка", null=True, blank=True)
    thumbnail = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 80}
    )
    user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING, null=True, blank=True,
                                related_name="profile")

    def __str__(self):
        return self.user.username