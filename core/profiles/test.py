import uuid
import json

from rest_framework.test import APITestCase
from rest_framework.settings import api_settings
from rest_framework_jwt.settings import api_settings as jwt_settings

from .models import Profile
from .serializers import ProfileSerializer


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
        return f'{cls.URL}/{profile.external_uuid}'

    def setUp(self):
        self.vasco_profile = Profile.objects.create(**USER_VASCO)
        self.joao_profile = Profile.objects.create(**USER_JOAO)
        self.chi_profile = Profile.objects.create(**USER_CHI)

        jwt_encode_handler = jwt_settings.JWT_ENCODE_HANDLER
        payload = {'uuid': USER_JOAO['external_uuid']}
        token = jwt_encode_handler(payload)

        self.http_auth = {
            'HTTP_AUTHORIZATION': f'JWT {token}',
        }

    def test_options_401(self):
        response = self.client.options(self.URL)
        self.assertEqual(response.status_code, 401)

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
        self.assertEqual(response.json()['count'], 3)
        self.assertEqual(
            response.json()['results'],
            [ProfileSerializer(profile).data
             for profile in [self.chi_profile, self.joao_profile, self.vasco_profile]]
        )

    def test_list_200_search(self):
        pattern = 'Valverde'
        response = self.client.get(
            f'{self.URL}?search={pattern}', **self.http_auth)
        self.assertEqual(response.status_code, 200)

        self.assertIsNone(response.json()['next'])
        self.assertIsNone(response.json()['previous'])
        self.assertEqual(response.json()['count'], 2)
        self.assertEqual(
            response.json()['results'],
            [ProfileSerializer(profile).data for profile in [self.joao_profile, self.vasco_profile]]
        )

    def test_list_200_paginated(self):
        number_of_dummy_profiles = int(api_settings.PAGE_SIZE * 1.5)
        for i in range(0, number_of_dummy_profiles):
            Profile.objects.create(external_uuid=str(i), name=f'dummy_{i}')

        initial_url = f'{self.URL}?search=dummy'
        response_initial = self.client.get(initial_url, **self.http_auth)
        self.assertEqual(response_initial.status_code, 200)
        self.assertIsNotNone(response_initial.json()['next'])
        next_page_url = response_initial.json()['next']
        self.assertIsNone(response_initial.json()['previous'])
        self.assertEqual(response_initial.json()['count'], api_settings.PAGE_SIZE * 1.5)

        response_next_page = self.client.get(next_page_url, **self.http_auth)
        self.assertIsNone(response_next_page.json()['next'])
        self.assertIsNotNone(response_next_page.json()['previous'])
        prev_page_url = response_next_page.json()['previous']
        self.assertEqual(response_next_page.json()['count'], api_settings.PAGE_SIZE * 1.5)

        response_prev_page = self.client.get(prev_page_url, **self.http_auth)
        self.assertEqual(response_prev_page.json(), response_initial.json())

    def test_retrieve_401(self):
        response = self.client.get(
            self.instance_url(self.joao_profile))
        self.assertEqual(response.status_code, 401)

    def test_retrieve_200(self):
        response = self.client.get(
            self.instance_url(self.joao_profile), **self.http_auth)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], USER_JOAO['name'])

        response = self.client.get(
            self.instance_url(self.vasco_profile), **self.http_auth)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], USER_VASCO['name'])

    def test_create_400_no_token(self):
        response = self.client.post(self.URL, data=json.dumps({}), content_type=self.CONTENT_TYPE)
        self.assertEqual(response.status_code, 400)
        self.assertIn('token', response.json())
        self.assertEqual(response.json()['token'], ["This field is required."])

    def test_create_400_bad_token(self):
        response = self.client.post(
            self.URL, data=json.dumps({'token': 'bad.token'}), content_type=self.CONTENT_TYPE)
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.json())
        self.assertEqual(response.json()['non_field_errors'], ["Invalid Token field."])

    def test_create_400_no_uuid(self):
        jwt_encode_handler = jwt_settings.JWT_ENCODE_HANDLER
        payload = {'no_uuid': 'new_user_uuid'}
        token = jwt_encode_handler(payload)

        response = self.client.post(
            self.URL, data=json.dumps({'token': token}), content_type=self.CONTENT_TYPE)
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.json())
        self.assertEqual(response.json()['non_field_errors'], ["Invalid payload (no uuid)."])

    def test_create_400_bad_uuid(self):
        jwt_encode_handler = jwt_settings.JWT_ENCODE_HANDLER
        payload = {'uuid': 'bad uuid'}
        token = jwt_encode_handler(payload)

        response = self.client.post(
            self.URL, data=json.dumps({'token': token}), content_type=self.CONTENT_TYPE)
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.json())
        self.assertEqual(response.json()['non_field_errors'], ["Invalid payload (bad uuid)."])

    def test_create_400_existing_uuid(self):
        jwt_encode_handler = jwt_settings.JWT_ENCODE_HANDLER
        payload = {'uuid': USER_JOAO['external_uuid']}
        token = jwt_encode_handler(payload)

        response = self.client.post(
            self.URL, data=json.dumps({'token': token}), content_type=self.CONTENT_TYPE)
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.json())
        self.assertEqual(response.json()['non_field_errors'], ["Invalid payload (existing uuid)."])

    def test_create_201(self):
        jwt_encode_handler = jwt_settings.JWT_ENCODE_HANDLER
        payload = {
            'uuid': uuid.uuid4().hex,
            'username': 'John Doe'
        }
        token = jwt_encode_handler(payload)

        response = self.client.post(
            self.URL, data=json.dumps({'token': token}), content_type=self.CONTENT_TYPE)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Profile.objects.count(), 4)
        self.assertEqual(Profile.objects.filter(external_uuid=payload['uuid']).count(), 1)
        self.assertEqual(Profile.objects.get(external_uuid=payload['uuid']).name, payload['username'])

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
        response = self.client.delete(self.instance_url(self.joao_profile), **self.http_auth)
        self.assertEqual(response.status_code, 405)

    def test_me_401(self):
        response = self.client.get(f'{self.URL}/me')
        self.assertEqual(response.status_code, 401)

    def test_me_200(self):
        response = self.client.get(f'{self.URL}/me', **self.http_auth)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], USER_JOAO['name'])
