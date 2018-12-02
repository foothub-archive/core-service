from django.db import models

from generics.models import Base
from .managers import ProfileManager


class Profile(Base):

    UUID_LEN = 32

    # "foreign key" to the auth service User Model
    external_uuid = models.CharField(
        max_length=UUID_LEN,
        editable=False,
        null=False,
        blank=False,
        unique=True,
    )

    @property
    def uuid(self):
        return self.external_uuid

    name = models.CharField(max_length=128)

    # django-rest-framework-jwt expects the user object to have this property
    # for now, from profiles are always active
    is_active = True

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    class Meta:
        ordering = ['-id']
