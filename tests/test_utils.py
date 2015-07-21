import unittest
import datetime
import locale
from urllib.request import urlopen

from byro.utils import Utils


class IntervalCzech(unittest.TestCase):

    def setUp(self):
        locale.setlocale(locale.LC_ALL, "cs_CZ.utf8")

    def tearDown(self):
        pass

    def test_leden(self):
        real = Utils.define_interval('leden', 2015)
        firstJan = datetime.date(2015, 1, 1)
        lastJan = datetime.date(2015, 1, 31)
        expect = (firstJan, lastJan, "leden")
        self.assertEqual(real, expect)

    def test_duben(self):
        real = Utils.define_interval('duben', 2015)
        firstJan = datetime.date(2015, 4, 1)
        lastJan = datetime.date(2015, 4, 30)
        expect = (firstJan, lastJan, "duben")
        self.assertEqual(real, expect)


class IntervalEnglish(unittest.TestCase):

    def setUp(self):
        locale.setlocale(locale.LC_ALL, "en_US.utf8")

    def tearDown(self):
        pass

    def test_january(self):
        real = Utils.define_interval('January', 2015)
        firstJan = datetime.date(2015, 1, 1)
        lastJan = datetime.date(2015, 1, 31)
        expect = (firstJan, lastJan, "January")
        self.assertEqual(real, expect)

    def test_april(self):
        real = Utils.define_interval('April', 2015)
        firstJan = datetime.date(2015, 4, 1)
        lastJan = datetime.date(2015, 4, 30)
        expect = (firstJan, lastJan, "April")
        self.assertEqual(real, expect)


class PickTime(unittest.TestCase):

    def setUp(self):
        self.time = "10:00-11:00"
        self.rawtext = "INF department meeting"

    def test_ok1(self):
        text = self.time + " " + self.rawtext
        real = Utils.pick_time(text)
        expect = (self.time, self.rawtext)
        self.assertEqual(real, expect)

    def test_ok2(self):
        text = " " + self.time + "   " + self.rawtext
        real = Utils.pick_time(text)
        expect = (self.time, self.rawtext)
        self.assertEqual(real, expect)

    def test_ok3(self):
        text = self.time + "* " + self.rawtext
        real = Utils.pick_time(text)
        expect = (self.time, self.rawtext)
        self.assertEqual(real, expect)

    def test_bad(self):
        real = Utils.pick_time(self.rawtext)
        expect = ("?", self.rawtext)
        self.assertEqual(real, expect)


class SplitFilename(unittest.TestCase):

    def setUp(self):
        pass

    def test1(self):
        res = Utils.split_filename("file.md")
        self.assertEqual(res[0], "file")
        self.assertEqual(res[1], ".md")

    def test2(self):
        res = Utils.split_filename("file.tex")
        self.assertEqual(res[0], "file")
        self.assertEqual(res[1], ".tex")

    def test3(self):
        res = Utils.split_filename("file.md.pdf")
        self.assertEqual(res[0], "file.md")
        self.assertEqual(res[1], ".pdf")

    def test4(self):
        res = Utils.split_filename("file-with_extra.symbols.txt")
        self.assertEqual(res[0], "file-with_extra.symbols")
        self.assertEqual(res[1], ".txt")



def offline():
    try:
        response = urlopen('http://74.125.228.100', timeout=1)
        return False
    except:
        return True


@unittest.skipIf(offline(), "Internet connection is required for this test case")
class RedmineOnline(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_user(self):
        pass

    def test_get_data(self):
        pass
        #rm = Red
        #data = rm.get_data()