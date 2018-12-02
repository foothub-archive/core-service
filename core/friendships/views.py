from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.filters import SearchFilter

from generics.permissions import IsAuthenticated
from .models import FriendshipInvitation
from .serializers import ReceivedFriendshipInvitationSerializer, CreatedFriendshipInvitationSerializer


class ReceivedFriendshipInvitationViewSet(RetrieveModelMixin,
                                          DestroyModelMixin,
                                          ListModelMixin,
                                          GenericViewSet):

    model_class = FriendshipInvitation
    serializer_class = ReceivedFriendshipInvitationSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('inviting__name',)

    def get_queryset(self):
        user = self.request.user
        return self.model_class.objects.filter(invited=user)


class CreatedFriendshipInvitationViewSet(CreateModelMixin,
                                         RetrieveModelMixin,
                                         DestroyModelMixin,
                                         ListModelMixin,
                                         GenericViewSet):

    model_class = FriendshipInvitation
    serializer_class = CreatedFriendshipInvitationSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('invited__name',)

    def get_queryset(self):
        user = self.request.user
        return self.model_class.objects.filter(inviting=user)
