from django.urls import path, include

from core.views import status_view

urlpatterns = [
    path('', status_view),
    path('', include('profiles.urls')),
    path('', include('friendships.urls')),
    path('', include('friend_profiles.urls')),
]
