from django.test import TestCase
from app.shortener.models import URL
from app.shortener.generator import Base62Converter, generate_short_url, get_index_from_shortcut


class TestShortURLGenerator(TestCase):
    def test_all(self):
        r = Base62Converter.encode(0)
        self.assertEqual(r, '0')

        r = Base62Converter.encode(30000)
        self.assertEqual(r, '7NS')

        r = generate_short_url("http://localhost", next_element_index=1)
        self.assertEqual(r, 'http://localhost/2Bj')

    def test_al2l2(self):
        r = Base62Converter.encode(0)
        self.assertEqual(r, '0')

        r = Base62Converter.encode(30000)
        self.assertEqual(r, '7NS')

        # new_urls = [URL(long=f"XDD{i}", short=f"XD{i}") for i in range(2000)]
        # URL.objects.bulk_create(new_urls)

        r = generate_short_url("http://localhost", next_element_index=2000)
        self.assertEqual(r, 'http://localhost/37y')

    def test_al3(self):
        r = Base62Converter.decode("7NS")
        self.assertEqual(r, 30000)

        r = Base62Converter.decode('0')
        self.assertEqual(r, 0)

        r = Base62Converter.decode('2Bi')
        self.assertEqual(r, 10000)

        r = Base62Converter.decode('37y')
        self.assertEqual(r, 12000)

        r = get_index_from_shortcut("37y")
        self.assertEqual(r, 2000)
