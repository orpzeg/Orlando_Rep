import unittest
import xmlrunner

def first_longest_common(string_one, string_two):
    longest_substring = []

    for ind, elem in enumerate(string_one):
        for j in [i for i, x in enumerate(string_two) if x == elem]:
            substring = []
            temp_ind = ind
            while temp_ind < len(string_one) and j < len(string_two) and string_one[temp_ind] == string_two[j]:
                substring.append(string_one[temp_ind])
                temp_ind += 1
                j += 1

            if len(substring) > len(longest_substring):
                longest_substring = substring

    return ''.join(longest_substring)


class TestFirstLongestCommon(unittest.TestCase):

    # Basic Test Cases
    def test_basic_cases(self):
        self.assertEqual(first_longest_common("hello", "yellow"), 'ello')
        self.assertEqual(first_longest_common("abcdef", "ghijkl"), '')
        self.assertEqual(first_longest_common("ABCD", "BCDA"), 'BCD')
        self.assertEqual(first_longest_common("xyz", "abcxyz"), 'xyz')

    # Edge Test Cases
    def test_edge_cases(self):
        self.assertEqual(first_longest_common("", ""), '')
        self.assertEqual(first_longest_common("A", "A"), 'A')
        self.assertEqual(first_longest_common("A", "B"), '')
        self.assertEqual(first_longest_common("A", ""), '')

    # Additional Test Cases
    def test_advanced_cases(self):
        self.assertEqual(first_longest_common("ABABAB", "BABA"), 'BABA')
        self.assertEqual(first_longest_common("appleorangebanana", "orangeapplegrape"), 'orange')
        self.assertEqual(first_longest_common("ABCDEF", "ACDFEB"), 'CD')
        self.assertEqual(first_longest_common("@hello@", "@world@hello@"), '@hello@')
        self.assertEqual(first_longest_common("123hello456", "hello123"), 'hello')
        self.assertEqual(first_longest_common("Hello", "hello"), 'ello')

        s1 = "a" * 7000 + "hello" + "b" * 5000
        s2 = "c" * 5000 + "hello" + "d" * 2000
        self.assertEqual(first_longest_common(s1, s2), 'hello')


if __name__ == '__main__':
    with open('Practice_xml_output.xml', 'w') as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output))
