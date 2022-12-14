from app.shortener.exceptions import InvalidShortcut

INDEX_OFFSET = 10_000  # to generate short URLs with min. length of 3 characters


def generate_short_url(url_base: str, next_element_index: int) -> str:
    shortcut = Base62Converter.encode(next_element_index + INDEX_OFFSET)
    return f"{url_base}/{shortcut}"


def get_index_from_shortcut(url: str) -> int:
    return Base62Converter.decode(url) - INDEX_OFFSET


class Base62Converter:
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ALPHABET_MAP = {character: index for index, character in enumerate(ALPHABET)}
    BASE = len(ALPHABET)

    @staticmethod
    def encode(number: int) -> str:
        if number == 0:
            return Base62Converter.ALPHABET[0]

        result = ""
        while number:
            result = Base62Converter.ALPHABET[number % Base62Converter.BASE] + result
            number //= Base62Converter.BASE

        return result

    @staticmethod
    def decode(shortcut: str) -> int:
        result = 0
        index = 0

        for char in shortcut:
            power = (len(shortcut) - (index + 1))
            if char not in Base62Converter.ALPHABET_MAP:
                raise InvalidShortcut
            result += Base62Converter.ALPHABET_MAP[char] * (Base62Converter.BASE ** power)
            index += 1

        return result
