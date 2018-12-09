from rest_framework import routers
from .views import FriendProfilesViewSet


router = routers.SimpleRouter(trailing_slash=False)
router.register(
    r'friend_profiles', FriendProfilesViewSet, 'friend_profiles')

urlpatterns = router.urls
