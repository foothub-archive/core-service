from django.db import models


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

    class Meta:
        abstract = True
        ordering = ('-updated_at',)

    def accept(self):
        raise NotImplementedError('Invitations must implement resolve method')
