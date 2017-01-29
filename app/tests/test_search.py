from django.test import TestCase
from django.urls import reverse

from app.models import Item, Search, FoundItem


class SearchTest(TestCase):
    fixtures = ['auth', 'items']

    def test_with_unpublished(self):
        for i in Item.objects.all():
            i.is_published = False
            i.save()

        response = self.client.get(reverse('home'))

        self.assertNotContains(response, 'Singapore')
        self.assertNotIn('table', response.context)

    def test_with_published(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, 'Singapore', 2)
        table = response.context['table']
        self.assertEqual(len(table.data), 2)

    def test_search_what(self):
        response = self.client.get(reverse('home'), dict(what='first item'))

        self.assertContains(response, 'Singapore', 1)
        table = response.context['table']
        self.assertEqual(len(table.data), 1)

    def test_filter_by_category(self):
        response = self.client.get(reverse('home'), dict(category=1))

        self.assertContains(response, 'Singapore', 1)
        table = response.context['table']
        self.assertEqual(len(table.data), 1)

    def test_set_location(self):
        response = self.client.get(reverse('home'), dict(place='Singapore', location='1.3553794,103.86774439999999'))

        table = response.context['table']
        self.assertEqual(len(table.data), 2)
        self.assertAlmostEqual(table.data.data[0].distance, 4.27, places=2)
        self.assertAlmostEqual(table.data.data[1].distance, 4.94, places=2)

    def test_search_is_saved(self):
        self.client.get(reverse('home'), dict(what='first item'))

        self.assertEqual(len(Search.objects.all()), 1)
        self.assertEqual(list(Search.objects.all())[0].what, 'first item')

    def test_search_found_items_are_saved(self):
        self.client.get(reverse('home'), dict(place='Singapore', location='1.3553794,103.86774439999999'))

        self.assertEqual(len(FoundItem.objects.all()), 2)
