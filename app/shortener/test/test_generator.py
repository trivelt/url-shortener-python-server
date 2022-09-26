from django.test import TestCase
from app.shortener.generator import Base62Converter, generate_short_url, get_index_from_shortcut
from app.shortener.exceptions import InvalidShortcut


class TestBase62Converter(TestCase):
    def test_encode(self):
        encode = Base62Converter.encode
        self.assertEqual('0', encode(0))
        self.assertEqual('2Bi', encode(10_000))
        self.assertEqual('37y', encode(12_000))
        self.assertEqual('7NS', encode(30_000))

    def test_decode(self):
        decode = Base62Converter.decode
        self.assertEqual(0, decode('0'))
        self.assertEqual(10_001, decode('2Bj'))
        self.assertEqual(12_000, decode('37y'))
        self.assertEqual(20_000, decode('5cA'))
        self.assertEqual(30_000, decode('7NS'))
        with self.assertRaises(InvalidShortcut):
            decode("!invalidParameter")


class TestShortURLGenerator(TestCase):
    def test_generate_short_url(self):
        short_url = generate_short_url("https://short.polydev.pl", next_element_index=1)
        self.assertEqual('https://short.polydev.pl/2Bj', short_url)

        short_url = generate_short_url("http://localhost", next_element_index=2000)
        self.assertEqual('http://localhost/37y', short_url)

        short_url = generate_short_url("http://localhost:8000", next_element_index=10_000)
        self.assertEqual('http://localhost:8000/5cA', short_url)

        short_url = generate_short_url("http://localhost", next_element_index=20_000)
        self.assertEqual('http://localhost/7NS', short_url)

    def test_get_index_from_shortcut(self):
        self.assertEqual(1, get_index_from_shortcut("2Bj"))
        self.assertEqual(2000, get_index_from_shortcut("37y"))
        self.assertEqual(10_000, get_index_from_shortcut("5cA"))
        self.assertEqual(20_000, get_index_from_shortcut("7NS"))
