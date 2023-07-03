from django.test import TestCase
from django.shortcuts import reverse
from pprint import pprint


class LandingPageTest(TestCase):

    def test_get(self):
        """Test"""
        response = self.client.get(reverse('landing-page'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing.html")

        pprint(response.status_code)