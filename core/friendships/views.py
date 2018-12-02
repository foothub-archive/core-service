from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from generics.permissions import IsAuthenticated
from .models import FriendshipInvitation, Friendship
from .serializers import (
    ReceivedFriendshipInvitationSerializer,
    CreatedFriendshipInvitationSerializer,
    FriendshipSerializer
)


class ReceivedFriendshipInvitationViewSet(RetrieveModelMixin, DestroyModelMixin,
                                          ListModelMixin, GenericViewSet):

    model_class = FriendshipInvitation
    serializer_class = ReceivedFriendshipInvitationSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('inviting__name',)

    def get_queryset(self):
        user = self.request.user
        return self.model_class.objects.filter(invited=user)

    @action(methods=('post',), detail=True)
    def accept(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.accept()
        return Response(status=HTTP_204_NO_CONTENT)


class CreatedFriendshipInvitationViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin,
                                         ListModelMixin, GenericViewSet):

    model_class = FriendshipInvitation
    serializer_class = CreatedFriendshipInvitationSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('invited__name',)

    def get_queryset(self):
        user = self.request.user
        return self.model_class.objects.filter(inviting=user)


class FriendshipViewSet(RetrieveModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):

    model_class = Friendship
    serializer_class = FriendshipSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('target__name',)

    def get_queryset(self):
        user = self.request.user
        return self.model_class.objects.filter(source=user)

    def perform_destroy(self, instance):
        try:
            reverse_instance = self.model_class.objects.get(source=instance.target, target=instance.source)
            reverse_instance.delete()
        except ObjectDoesNotExist:
            pass  # no longer exists, its ok..

        instance.delete()
