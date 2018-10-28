from django.urls import path

from core.views import status_view

urlpatterns = [
    path('', status_view),
]
