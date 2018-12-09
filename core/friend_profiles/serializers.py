from rest_framework import serializers

from profiles.serializers import ProfileSerializer
from profiles.models import Profile
from friendships.models import Friendship


class ProfileIsFriendSerializer(ProfileSerializer):
    is_friend = serializers.SerializerMethodField()

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
        fields = ProfileSerializer.Meta.fields + ('is_friend',)
