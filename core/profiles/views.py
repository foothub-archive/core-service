
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileSerializer, CreateProfileSerializer
from .permissions import ProfilePermissions


class ProfileViewSet(CreateModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     ListModelMixin,
                     GenericViewSet):

    model_class = Profile
    serializer_class = ProfileSerializer
    create_serializer_class = CreateProfileSerializer
    permission_classes = (ProfilePermissions,)
    lookup_field = 'external_uuid'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        return self.model_class.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return self.create_serializer_class

        return self.serializer_class

    @action(methods=['get'], detail=False)
    def me(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
