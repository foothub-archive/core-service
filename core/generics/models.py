from django.db import models, IntegrityError


class Base(models.Model):

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-updated_at',)


class Invitation(Base):
    inviting = models.ForeignKey(to='profiles.Profile', on_delete=models.CASCADE, null=False,
                                 related_name='%(app_label)s_%(class)s_inviting')

    invited = models.ForeignKey(to='profiles.Profile', on_delete=models.CASCADE, null=False,
                                related_name='%(app_label)s_%(class)s_invited')

    def save(self, *args, **kwargs):
        # No self invitations!
        if self.inviting == self.invited:
            raise IntegrityError('inviting and invited can not be the same')
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ('-updated_at',)
        unique_together = ('inviting', 'invited')

    def accept(self):
        raise NotImplementedError('Invitations must implement resolve method')
