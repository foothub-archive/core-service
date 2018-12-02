import uuid
from collections import namedtuple

from rest_framework_jwt.settings import api_settings as jwt_settings

from profiles.models import Profile


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

ProfilesSetUp = namedtuple('ProfilesSetUp', ['profiles', 'http_auth'])


def set_up() -> ProfilesSetUp:
    vasco_profile = Profile.objects.create(**USER_VASCO)
    chi_profile = Profile.objects.create(**USER_CHI)
    joao_profile = Profile.objects.create(**USER_JOAO)

    jwt_encode_handler = jwt_settings.JWT_ENCODE_HANDLER
    payload = {'uuid': USER_JOAO['external_uuid']}
    token = jwt_encode_handler(payload)

    http_auth = {
        'HTTP_AUTHORIZATION': f'JWT {token}',
    }

    return ProfilesSetUp((vasco_profile, chi_profile, joao_profile), http_auth)
