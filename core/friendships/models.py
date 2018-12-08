from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError
from generics.models import Base, Invitation


class FriendshipInvitation(Invitation):

    def accept(self) -> None:
        """
        creates a Friendships for both profiles the invite (invting and invited)
        deletes invite and reverse invite if exists

        """
        Friendship.objects.get_or_create(source=self.inviting, target=self.invited)
        Friendship.objects.get_or_create(source=self.invited, target=self.inviting)
        try:
            reverse_invite = FriendshipInvitation.objects.get(inviting=self.invited, invited=self.inviting)
            reverse_invite.delete()
        except ObjectDoesNotExist:
            pass
        self.delete()


class Friendship(Base):
    source = models.ForeignKey(to='profiles.Profile', on_delete=models.CASCADE, null=False,
                               related_name='friend_source')

    target = models.ForeignKey(to='profiles.Profile', on_delete=models.CASCADE, null=False,
                               related_name='friend_target')

    def save(self, *args, **kwargs):
        # No self friendships!
        if self.source == self.target:
            raise IntegrityError('inviting and invited can not be the same')
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-updated_at',)
        unique_together = ('source', 'target')
