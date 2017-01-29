from django.test import TestCase
from django.urls import reverse


class HomeTest(TestCase):
    fixtures = ['auth', 'items']

    def test_home(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, 'Singapore', 2, 200)
        self.assertTemplateUsed(response, 'app/index.html')
        self.assertEqual(response.context['published_items'], 2)
        self.assertEqual(response.context['fb_profile_clicks'], 0)
        self.assertFalse('searched' in response.context)
        table = response.context['table']
        self.assertEqual(len(table.data), 2)
