from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import SearchFilter
from rest_framework.decorators import list_route
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileSerializer
from .permissions import ProfilePermissions


class ProfileViewSet(RetrieveModelMixin,
                     UpdateModelMixin,
                     ListModelMixin,
                     GenericViewSet):

    model_class = Profile
    serializer_class = ProfileSerializer
    permission_classes = (ProfilePermissions,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        return self.model_class.objects.all()

    @list_route(methods=['get'])
    def me(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
