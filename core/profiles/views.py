from rest_framework import viewsets
# from rest_framework import filters


from .models import Profile
from .serializers import ProfileSerializer
from .permissions import ProfilePermissions


class ProfileViewSet(viewsets.ModelViewSet):
    model_class = Profile
    serializer_class = ProfileSerializer
    permission_classes = (ProfilePermissions, )
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('target_user__username',)

    def get_queryset(self):
        return self.model_class.objects.all()
