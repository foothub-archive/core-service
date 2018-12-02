from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from profiles.serializers import ProfileSerializer
from profiles.models import Profile

from .models import FriendshipInvitation, Friendship


class ReceivedFriendshipInvitationSerializer(serializers.ModelSerializer):
    friend = ProfileSerializer(many=False, read_only=True, source='inviting')

    class Meta:
        model = FriendshipInvitation
        fields = ('id', 'friend')


class CreatedFriendshipInvitationSerializer(serializers.ModelSerializer):
    friend = ProfileSerializer(many=False, read_only=True, source='invited')
    friend_uuid = serializers.UUIDField(write_only=True, format='hex')

    def validate(self, data):
        try:
            invited = Profile.objects.get(external_uuid=data['friend_uuid'].hex)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Unable to find Invited Profile.")

        inviting = self.context['request'].user

        return {
            'inviting': inviting,
            'invited': invited,
        }

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)

    class Meta:
        model = FriendshipInvitation
        fields = ('id', 'friend', 'friend_uuid')


class FriendshipSerializer(serializers.ModelSerializer):
    friend = ProfileSerializer(many=False, read_only=True, source='target')

    class Meta:
        model = Friendship
        fields = ('id', 'friend')
