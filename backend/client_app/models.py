from django.db import models
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save

from .enums import PermissionLevels


class Client(models.Model):
    user = models.OneToOneField(User, related_name='client', on_delete=models.CASCADE)
    permission_level = models.IntegerField(choices=PermissionLevels, default=1)
    department = models.ForeignKey(to='Department',
                                   related_name='client',
                                   related_query_name='clients',
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True)

    def __str__(self):
        return self.user.username


class Settings(models.Model):
    prefix = models.CharField(max_length=8)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE, related_name='settings')

    def __str__(self):
        return self.client.user.username


class Department(models.Model):
    name = models.CharField(max_length=128)

    @property
    def employees(self):
        return ", ".join([str(client) for client in self.client.all()])

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_client(instance, created, **kwargs):
    if created:
        client = Client.objects.create(user=instance)
        Settings.objects.create(client=client)
