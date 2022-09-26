from django.test import TestCase
from app.shortener.models import URL


class TestURL(TestCase):
    def test_from_shortcut(self):
        new_urls = [URL(long=f"http://long-url-{i}.com", short=f"http://localhost/shrt{i}") for i in range(1, 2001)]
        URL.objects.bulk_create(new_urls)

        url = URL.from_shortcut('2Bj')
        self.assertEqual('http://long-url-1.com', url.long)

        url = URL.from_shortcut('37y')
        self.assertEqual('http://long-url-2000.com', url.long)

        url = URL.from_shortcut("notExisting")
        self.assertIsNone(url)

        url = URL.from_shortcut('!invalid')
        self.assertIsNone(url)

    def test_next_index(self):
        self.assertEqual(1, URL.next_index())

        URL.objects.create()
        self.assertEqual(2, URL.next_index())

        URL.objects.bulk_create([URL() for _ in range(300)])
        self.assertEqual(302, URL.next_index())
