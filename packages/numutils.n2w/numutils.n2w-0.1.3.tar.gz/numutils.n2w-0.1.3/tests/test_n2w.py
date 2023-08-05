from unittest import TestCase
from numutils import n2w


class Test_n2w(TestCase):
    # 1-10
    def test_one(self):
        n = n2w(1)
        self.assertEqual(n.words(), "one")

    def test_two(self):
        n = n2w(2)
        self.assertEqual(n.words(), "two")

    def test_three(self):
        n = n2w(3)
        self.assertEqual(n.words(), "three")

    def test_four(self):
        n = n2w(4)
        self.assertEqual(n.words(), "four")

    def test_five(self):
        n = n2w(5)
        self.assertEqual(n.words(), "five")

    def test_six(self):
        n = n2w(6)
        self.assertEqual(n.words(), "six")

    def test_seven(self):
        n = n2w(7)
        self.assertEqual(n.words(), "seven")

    def test_eight(self):
        n = n2w(8)
        self.assertEqual(n.words(), "eight")

    def test_nine(self):
        n = n2w(9)
        self.assertEqual(n.words(), "nine")

    def test_ten(self):
        n = n2w(10)
        self.assertEqual(n.words(), "ten")

    # 11-19
    def test_eleven(self):
        n = n2w(11)
        self.assertEqual(n.words(), "eleven")

    def test_twelve(self):
        n = n2w(12)
        self.assertEqual(n.words(), "twelve")

    def test_thirteen(self):
        n = n2w(13)
        self.assertEqual(n.words(), "thirteen")

    def test_fourteen(self):
        n = n2w(14)
        self.assertEqual(n.words(), "fourteen")

    def test_fifteen(self):
        n = n2w(15)
        self.assertEqual(n.words(), "fifteen")

    def test_sixteen(self):
        n = n2w(16)
        self.assertEqual(n.words(), "sixteen")

    def test_seventeen(self):
        n = n2w(17)
        self.assertEqual(n.words(), "seventeen")

    def test_eighteen(self):
        n = n2w(18)
        self.assertEqual(n.words(), "eighteen")

    def test_nineteen(self):
        n = n2w(19)
        self.assertEqual(n.words(), "nineteen")

    # 20-99
    def test_twenty(self):
        n = n2w(20)
        self.assertEqual(n.words(), "twenty")

    def test_twenty_one(self):
        n = n2w(21)
        self.assertEqual(n.words(), "twenty one")

    def test_twenty_two(self):
        n = n2w(22)
        self.assertEqual(n.words(), "twenty two")

    def test_twenty_three(self):
        n = n2w(23)
        self.assertEqual(n.words(), "twenty three")

    def test_twenty_four(self):
        n = n2w(24)
        self.assertEqual(n.words(), "twenty four")

    def test_twenty_five(self):
        n = n2w(25)
        self.assertEqual(n.words(), "twenty five")

    def test_thirty(self):
        n = n2w(30)
        self.assertEqual(n.words(), "thirty")

    def test_forty(self):
        n = n2w(40)
        self.assertEqual(n.words(), "fourty")

    def test_fifty(self):
        n = n2w(50)
        self.assertEqual(n.words(), "fifty")

    def test_sixty(self):
        n = n2w(60)
        self.assertEqual(n.words(), "sixty")

    def test_seventy(self):
        n = n2w(70)
        self.assertEqual(n.words(), "seventy")

    def test_eighty(self):
        n = n2w(80)
        self.assertEqual(n.words(), "eighty")

    def test_ninety(self):
        n = n2w(90)
        self.assertEqual(n.words(), "ninety")

    # 100-999
    def test_one_hundred(self):
        n = n2w(100)
        self.assertEqual(n.words(), "one hundred")

    def test_one_hundred_and_one(self):
        n = n2w(101)
        self.assertEqual(n.words(), "one hundred and one")

    def test_one_hundred_and_twenty_three(self):
        n = n2w(123)
        self.assertEqual(n.words(), "one hundred and twenty three")

    def test_one_thousand(self):
        n = n2w(1000)
        self.assertEqual(n.words(), "one thousand")

    def test_one_thousand_and_one(self):
        n = n2w(1001)
        self.assertEqual(n.words(), "one thousand and one")

    def test_one_thousand_two_hundred_and_three(self):
        n = n2w(1203)
        self.assertEqual(n.words(), "one thousand two hundred and three")

    def test_one_thousand_two_hundred_and_thirty_four(self):
        n = n2w(1234)
        self.assertEqual(n.words(), "one thousand two hundred and thirty four")

    def test_ten_thousand(self):
        n = n2w(10000)
        self.assertEqual(n.words(), "ten thousand")

    def test_one_hundred_thousand(self):
        n = n2w(100000)
        self.assertEqual(n.words(), "one hundred thousand")

    def test_999999(self):
        n = n2w(999999)
        self.assertEqual(
            n.words(),
            "nine hundred and ninety nine thousand nine hundred and ninety nine",
        )

    def test_one_billion(self):
        n = n2w(1000000000)
        self.assertEqual(n.words(), "Only numbers < 1_000_000 dealt with at the moment")

    # def test_nonsense_input(self):
    #     self.assertEqual(n2w("nonsense"), ValueError)

    # def test_the_rest(self):
    #   start_val = 0
    #   print(start_val)
    #   with open(path.join(path.dirname(__file__), "test_results.txt"), "r") as f:
    #     for line in f:
    #       n = n2w(start_val)
    #       self.assertEqual(n.words(), line.rstrip())
    #       start_val += 1
