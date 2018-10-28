from django.test import TestCase


class TestLocalSettings(TestCase):

    def test_settings(self):
        from core.settings.local import DEBUG

        self.assertTrue(DEBUG)


class TestProductionSettings(TestCase):

    def test_settings(self):
        from core.settings.production import DEBUG, INSTALLED_APPS

        self.assertFalse(DEBUG)
        self.assertIn('gunicorn', INSTALLED_APPS)
