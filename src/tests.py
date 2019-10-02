import unittest
from src import Generator


class TestCases(unittest.TestCase):
    generator = Generator()
    valid_chars = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

    # test Generate a Random Integer
    def test_generate_number(self):
        generated_number = self.generator.generate_number(type='integer', )
        self.assertEqual(type(generated_number), int)

    # test Generate a Random Integer less than a given number
    def test_generate_number_higher_range(self):
        higher_range = 1000
        generated_number = self.generator.generate_number(type='integer',
                                                          range=True,
                                                          range_end=higher_range)
        self.assertEqual(type(generated_number), int)
        self.assertLessEqual(generated_number, higher_range)

    # test Generate a Random Integer more than a given number
    def test_generate_number_lower_range(self):
        lower_range = 1000
        generated_number = self.generator.generate_number(type='integer',
                                                          range=True,
                                                          range_start=lower_range)
        self.assertEqual(type(generated_number), int)
        self.assertGreaterEqual(generated_number, lower_range)

    # test Generate a Random Integer between 2 given numbers
    def test_generate_number_full_range(self):
        lower_range = 10
        higher_range = 100
        generated_number = self.generator.generate_number(type='integer',
                                                          range=True,
                                                          range_start=lower_range,
                                                          range_end=higher_range)
        self.assertEqual(type(generated_number), int)
        self.assertGreaterEqual(generated_number, lower_range)
        self.assertLessEqual(generated_number, higher_range)

    # test Generate a Random Character (alphanumeric)
    def test_generate_character(self):
        generated_character = self.generator.generate_string(type='string',
                                                             length=1)
        self.assertEqual(type(generated_character), str)
        self.assertIn(generated_character, self.valid_chars)

    # test Generate a Random Character from a given set of characters
    def test_generate_character_from_given_set(self):
        valid_set = ('1', '2', '3', '4', '5', 'a', 'b', 'c', 'd', 'e')
        generated_character = self.generator.generate_string(type='string',
                                                             length=1,
                                                             choices=valid_set,
                                                             choice_invert=False)
        self.assertEqual(type(generated_character), str)
        self.assertIn(generated_character, valid_set)

    # test Generate 10 Random Characters
    def test_generate_10_random_characters(self):
        generated_set = self.generator.generate_string(type='string',
                                                             length=10)
        self.assertEqual(type(generated_set), str)
        for letter in generated_set:
            self.assertIn(letter, self.valid_chars)


if __name__ == '__main__':
    unittest.main()
