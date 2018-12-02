from rest_framework import serializers

from profiles.serializers import ProfileSerializer

from .models import FriendshipInvitation


class FriendshipInvitationSerializerMeta:
    model = FriendshipInvitation
    fields = ('id', 'friend')


class ReceivedFriendshipInvitationSerializer(serializers.ModelSerializer):
    friend = ProfileSerializer(many=False, read_only=True, source='inviting')

    class Meta(FriendshipInvitationSerializerMeta):
        pass


class CreatedFriendshipInvitationSerializer(serializers.ModelSerializer):
    friend = ProfileSerializer(many=False, read_only=True, source='invited')

    class Meta(FriendshipInvitationSerializerMeta):
        pass
