import os

from django.test import TestCase


class SanityTests(TestCase):
    def test_sanity(self):
        self.assertEqual(os.environ['DJANGO_SETTINGS_MODULE'],'django_simplestore.settings')
    def test_sanity0(self):
        self.assertEqual(1+1,2)