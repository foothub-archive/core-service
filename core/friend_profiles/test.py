from django.test import TestCase
from rest_framework.test import APITestCase

from t_helpers.profiles import set_up as profiles_set_up
from profiles.models import Profile
from friendships.models import Friendship
from .serializers import ProfileIsFriendSerializer


class TestProfileIsFriendSerializer(TestCase):
    def setUp(self):
        profile_set_up = profiles_set_up()
        self.vasco, self.chi, self.joao = profile_set_up.profiles

        Friendship.objects.create(source=self.joao, target=self.vasco)

    def test_is_friend_no_context(self):
        serializer = ProfileIsFriendSerializer(self.vasco)
        self.assertFalse(serializer.data['is_friend'])


class TestProfileIsFriendApi(APITestCase):
    URL = '/friend_profiles'
    CONTENT_TYPE = 'application/json'

    @classmethod
    def instance_url(cls, instance: Profile):
        return f'{cls.URL}/{instance.id}'

    def setUp(self):
        profile_set_up = profiles_set_up()
        self.vasco, self.chi, self.joao = profile_set_up.profiles
        self.http_auth = profile_set_up.http_auth

        Friendship.objects.create(source=self.joao, target=self.vasco)

    def test_options_200(self):
        response = self.client.options(self.URL, **self.http_auth)
        self.assertEqual(response.status_code, 200)

    def test_list_401(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 401)

    def test_list_200(self):
        response = self.client.get(self.URL, **self.http_auth)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()['next'])
        self.assertIsNone(response.json()['previous'])
        self.assertEqual(Profile.objects.count(), 3)
        self.assertEqual(response.json()['count'], 2)
        self.assertEqual(response.json()['results'][0]['uuid'], self.chi.external_uuid)
        self.assertEqual(response.json()['results'][0]['is_friend'], False)
        self.assertEqual(response.json()['results'][1]['uuid'], self.vasco.external_uuid)
        self.assertEqual(response.json()['results'][1]['is_friend'], True)

    def test_list_200_search(self):
        pattern = 'vasco'
        response = self.client.get(f'{self.URL}?search={pattern}', **self.http_auth)
        self.assertEqual(response.status_code, 200)

        self.assertIsNone(response.json()['next'])
        self.assertIsNone(response.json()['previous'])
        self.assertEqual(response.json()['count'], 1)

        pattern = 'joao'
        response = self.client.get(f'{self.URL}?search={pattern}', **self.http_auth)
        self.assertEqual(response.status_code, 200)

        self.assertIsNone(response.json()['next'])
        self.assertIsNone(response.json()['previous'])
        self.assertEqual(response.json()['count'], 0)
