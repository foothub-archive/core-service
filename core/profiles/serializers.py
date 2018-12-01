from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from jwt import ExpiredSignature, DecodeError

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True, source='external_uuid')

    class Meta:
        model = Profile
        fields = ['uuid', 'name']


class CreateProfileSerializer(serializers.ModelSerializer):
    token = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        try:
            payload = api_settings.JWT_DECODE_HANDLER(data['token'])
        except (ExpiredSignature, DecodeError):
            raise serializers.ValidationError("Invalid Token field.")

        if 'uuid' not in payload:
            raise serializers.ValidationError("Invalid payload (no uuid).")

        if len(payload['uuid']) != self.Meta.model.UUID_LEN:
            raise serializers.ValidationError("Invalid payload (bad uuid).")

        if self.Meta.model.objects.filter(external_uuid=payload['uuid']).exists():
            raise serializers.ValidationError("Invalid payload (existing uuid).")

        data['uuid'] = payload['uuid']
        data['name'] = payload.get('username', '')  # use username to initialize profile.name
        return data

    def create(self, validated_data):
        return self.Meta.model.objects.create(
            external_uuid=validated_data['uuid'],
            name=validated_data['name'],
        )

    class Meta:
        model = Profile
        fields = ['token']
