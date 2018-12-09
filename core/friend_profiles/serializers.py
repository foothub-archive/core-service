from rest_framework import serializers

from profiles.serializers import ProfileSerializer
from profiles.models import Profile
from friendships.models import FriendshipInvitation, Friendship


class ProfileIsFriendSerializer(ProfileSerializer):
    has_friend_invitation = serializers.SerializerMethodField()
    is_friend = serializers.SerializerMethodField()

    def get_has_friend_invitation(self, profile: Profile) -> bool:
        is_friend = False
        if 'request' in self.context and self.context['request'].user is not None:
            is_friend = FriendshipInvitation.objects.filter(
                inviting=self.context['request'].user,
                invited=profile,
            ).exists()

        return is_friend

    def get_is_friend(self, profile: Profile) -> bool:
        is_friend = False
        if 'request' in self.context and self.context['request'].user is not None:
            is_friend = Friendship.objects.filter(
                source=self.context['request'].user,
                target=profile,
            ).exists()

        return is_friend

    class Meta:
        model = ProfileSerializer.Meta.model
        fields = ProfileSerializer.Meta.fields + ('has_friend_invitation', 'is_friend')
