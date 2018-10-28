import uuid

from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from .models import Profile


USER_VASCO = {
    'name': 'Vasco Valverde',
    'external_uuid': uuid.uuid4().hex

}

USER_JOAO = {
    'name': 'Joao Valverde',
    'external_uuid': uuid.uuid4().hex

}

USER_CHI = {
    'name': 'Chi Dominguez',
    'external_uuid': uuid.uuid4().hex
}


class TestProfilesApi(APITestCase):
    URL = '/profiles'
    CONTENT_TYPE = 'json'

    @classmethod
    def instance_url(cls, profile: Profile):
        return f'{cls.URL}/{profile.id}'

    def setUp(self):
        self.vasco_profile = Profile.objects.create(**USER_VASCO)
        self.joao_profile = Profile.objects.create(**USER_JOAO)
        self.chi_profile = Profile.objects.create(**USER_CHI)

        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = {'uuid': USER_JOAO['external_uuid']}
        token = jwt_encode_handler(payload)

        self.http_auth = {
            'HTTP_AUTHORIZATION': f'JWT {token}',
        }

    def test_list_200_401(self):
        response = self.client.get(self.URL, content_type=self.CONTENT_TYPE)
        self.assertEqual(response.status_code, 401)

    def test_list_200_200(self):
        response = self.client.get(self.URL, content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(
            response.data['results'],
            [{'name': profile.name} for profile in Profile.objects.all()]
        )

    def test_retrieve_401(self):
        response = self.client.get(
            self.instance_url(self.joao_profile), content_type=self.CONTENT_TYPE)
        self.assertEqual(response.status_code, 401)

    def test_retrieve_200(self):
        response = self.client.get(
            self.instance_url(self.joao_profile), content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], USER_JOAO['name'])

        response = self.client.get(
            self.instance_url(self.vasco_profile), content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], USER_VASCO['name'])
