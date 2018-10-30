import uuid
import json

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
    CONTENT_TYPE = 'application/json'

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
            [{'name': profile.name} for profile in [self.chi_profile, self.joao_profile, self.vasco_profile]]
        )

    def test_list_200_search(self):
        pattern = 'Valverde'
        response = self.client.get(
            f'{self.URL}?search={pattern}', content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(
            response.data['results'],
            [{'name': profile.name} for profile in [self.joao_profile, self.vasco_profile]]
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

    def test_create_405(self):
        response = self.client.post(self.URL, content_type=self.CONTENT_TYPE)
        self.assertEqual(response.status_code, 401)

        response = self.client.post(self.URL, content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 405)

    def test_update_401(self):
        response = self.client.put(
            self.instance_url(self.joao_profile), data={}, content_type=self.CONTENT_TYPE)
        self.assertEqual(response.status_code, 401)

        response = self.client.put(
            self.instance_url(self.vasco_profile), data={}, content_type=self.CONTENT_TYPE)
        self.assertEqual(response.status_code, 401)

    def test_update_403(self):
        response = self.client.put(
            self.instance_url(self.vasco_profile),
            data=json.dumps({}),
            content_type=self.CONTENT_TYPE,
            **self.http_auth)
        self.assertEqual(response.status_code, 403)

    def test_update_200(self):
        response = self.client.put(
            self.instance_url(self.joao_profile),
            data=json.dumps({'name': 'Joao Acciaioli'}),
            content_type=self.CONTENT_TYPE,
            **self.http_auth)
        self.assertEqual(response.status_code, 200)
        self.joao_profile.refresh_from_db()
        self.assertEqual(self.joao_profile.name, 'Joao Acciaioli')

    def test_delete_405(self):
        response = self.client.delete(
            self.instance_url(self.joao_profile), data={}, content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 405)

    def test_me_401(self):
        response = self.client.get(
            f'{self.URL}/me', content_type=self.CONTENT_TYPE)
        self.assertEqual(response.status_code, 401)

    def test_me_200(self):
        response = self.client.get(
            f'{self.URL}/me', content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], USER_JOAO['name'])
