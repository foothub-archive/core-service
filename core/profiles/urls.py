from rest_framework import routers
from .views import ProfileViewSet


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'profiles', ProfileViewSet, 'profiles')

urlpatterns = router.urls
