from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.contrib.auth.models import Permission

@receiver(post_save, sender=get_user_model())
def add_permission(sender, instance, created, **kwargs):
    if created:
        perm = Permission.objects.get(codename="change_psw_perm")
        instance.user_permissions.add(perm)