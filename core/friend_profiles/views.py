from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.filters import SearchFilter

from generics.permissions import IsAuthenticated
from profiles.models import Profile
from .serializers import ProfileIsFriendSerializer


class FriendProfilesViewSet(ListModelMixin, GenericViewSet):

    model_class = Profile
    serializer_class = ProfileIsFriendSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        """
        Exclude the user making the request from results
        """
        user = self.request.user
        return self.model_class.objects.exclude(id=user.id)
