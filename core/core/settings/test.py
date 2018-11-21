from django.test import TestCase


class TestLocalSettings(TestCase):

    def setUp(self):
        import core.settings.local as settings
        self.settings = settings

    def test_settings(self):
        self.assertTrue(self.settings.DEBUG)
        self.assertIsNotNone(self.settings.JWT_AUTH['JWT_PRIVATE_KEY'])
        self.assertFalse(self.settings.JWT_AUTH['JWT_VERIFY_EXPIRATION'])


class TestProductionSettings(TestCase):

    def setUp(self):
        import core.settings.production as settings
        self.settings = settings

    def test_settings(self):
        self.assertFalse(self.settings.DEBUG)
        self.assertIn('gunicorn', self.settings.INSTALLED_APPS)
        self.assertIsNone(self.settings.JWT_AUTH['JWT_PRIVATE_KEY'])
        self.assertTrue(self.settings.JWT_AUTH['JWT_VERIFY_EXPIRATION'])
