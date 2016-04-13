import os

from django.test import TestCase


class SanityTests(TestCase):
    def test_sanity(self):
        self.assertIn(os.environ['DJANGO_SETTINGS_MODULE'],['django_simplestore.settings','django_simplestore.tests.test_settings'])
    def test_sanity0(self):
        self.assertEqual(1+1,2)