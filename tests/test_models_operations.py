import unittest

from mmmusic.models.operations import combinable


class TestCombinableOperation(unittest.TestCase):
    def test_chained_operation(self):
        @combinable
        def is_odd(numbers: list[int]) -> list[int]:
            return [number for number in numbers if number % 2 == 1]

        @combinable
        def squared(numbers: list[int]) -> list[int]:
            return [number**2 for number in numbers]

        squared_odds = is_odd & squared

        sorted_squared_odds = squared_odds & combinable(sorted)

        sample = [5, 4, 6, 3, 7, 2, 8, 1, 9, 0]

        self.assertEqual(squared_odds(sample), [25, 9, 49, 1, 81])

        self.assertEqual(sorted_squared_odds(sample), [1, 9, 25, 49, 81])

    def test_union(self):
        @combinable
        def lowercase(words: list[str]) -> list[str]:
            return [word for word in words if word.islower()]

        @combinable
        def uppercase(words: list[str]) -> list[str]:
            return [word for word in words if word.isupper()]

        uppercase_or_lowercase_words = uppercase | lowercase

        sorted_uppercase_or_lowercase_words = uppercase_or_lowercase_words & combinable(
            sorted
        )

        sample = ["words", "woRDS", "WORDS", "puNCH", "LINE"]

        self.assertEqual(
            set(uppercase_or_lowercase_words(sample)), {"words", "WORDS", "LINE"}
        )

        self.assertEqual(
            sorted_uppercase_or_lowercase_words(sample), ["LINE", "WORDS", "words"]
        )
