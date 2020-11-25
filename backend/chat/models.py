from django.db import models

from client_app.enums import PermissionLevels
from client_app.models import Client


class Room(models.Model):
    name = models.CharField(max_length=32)
    capacity = models.PositiveIntegerField(default=32)
    permission_level = models.IntegerField(choices=PermissionLevels, default=1)
    users_online = models.ManyToManyField(
        Client,
        blank=True,
        related_name='rooms_user_in'
    )

    def __str__(self):
        return self.name
