from django.db import models
from generics.models import Base, Invitation


class FriendshipInvitation(Invitation):

    def accept(self):
        Friendship.objects.create(source=self.inviting, target=self.invited)
        Friendship.objects.create(source=self.invited, target=self.inviting)


class Friendship(Base):
    source = models.ForeignKey(to='profiles.Profile', on_delete=models.CASCADE, null=False,
                               related_name='friend_source')

    target = models.ForeignKey(to='profiles.Profile', on_delete=models.CASCADE, null=False,
                               related_name='friend_target')
