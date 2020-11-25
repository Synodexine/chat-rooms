from django.db import models
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save

from .enums import PermissionLevels


class Client(models.Model):
    user = models.OneToOneField(User, related_name='client', on_delete=models.CASCADE)
    permission_level = models.IntegerField(choices=PermissionLevels, default=1)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_client(instance, created, **kwargs):
    if created:
        Client.objects.create(user=instance)
