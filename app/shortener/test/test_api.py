from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from app.shortener.models import URL


class TestAPI(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_link(self):
        response = self.client.get('/api/v1/link', {'short': 'not-existing'}, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

        URL.objects.create(long='http://some-long-link.com', short='http://localhost/2Bj')
        response = self.client.get('/api/v1/link', {'short': '2Bj'}, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('http://some-long-link.com', response.data.get('long'))

    def test_post_link(self):
        response = self.client.post('/api/v1/link', {'long': 'invalid-url'})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Enter a valid URL.', response.data.get('error'))

        response = self.client.post('/api/v1/link', {'long': 'https://polydev.pl'})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('https://polydev.pl', response.data.get('long'))
        self.assertEqual('http://testserver/2Bj', response.data.get('short'))

        response = self.client.post('/api/v1/link', {'long': 'https://polydev.pl'})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('https://polydev.pl', response.data.get('long'))
        self.assertEqual('http://testserver/2Bk', response.data.get('short'))

    def test_post_and_get(self):
        response = self.client.post('/api/v1/link', {'long': 'https://polydev.pl'})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        response = self.client.get('/api/v1/link', {'short': '2Bj'}, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('https://polydev.pl', response.data.get('long'))

    def test_redirect(self):
        response = self.client.get('/nonexisting')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

        response = self.client.post('/api/v1/link', {'long': 'https://polydev.pl'})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        response = self.client.get('/2Bj')
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
        self.assertEqual('https://polydev.pl', response.url)
