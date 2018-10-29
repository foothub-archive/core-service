from django.db import models


class ProfileManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, username):

        return self.get(external_uuid=username)
