from rest_framework import mixins, viewsets
from rest_framework import filters


from .models import Profile
from .serializers import ProfileSerializer
from .permissions import ProfilePermissions


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):

    model_class = Profile
    serializer_class = ProfileSerializer
    permission_classes = (ProfilePermissions,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        return self.model_class.objects.all()
