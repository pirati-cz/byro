import re
import time
import datetime
from dateutil.relativedelta import relativedelta


class Utils:

    @staticmethod
    def define_interval(month='last', year=2015):
        """
        :param month:
        :type month: string
        :return: tuple with date strings
        """
        if month == 'this':
            monthNum = datetime.date.today().month
        elif month == 'last':
            delta = relativedelta(months=-1)
            monthNum = datetime.date.today().month - 1
            # todo year break
        elif isinstance(month, int):
            monthNum = month
        else:
            dt = Utils.month_and_year_to_datetime(month, year)
            monthNum = dt.month
        delta = relativedelta(months=1,days=-1)
        first = datetime.date(year, monthNum, 1)
        last = first + delta
        return (first, last, first.strftime("%B"))

    @staticmethod
    def month_and_year_to_datetime(month, year):
        """
        :param month: month
        :type month: string
        :param year:
        :type year: int
        :return: datetime
        """
        try:
            tstruct = time.strptime("{0} {1}".format(month, year), "%B %Y")
        except ValueError as e:
            # todo: add locale
            raise e
        tstamp = time.mktime(tstruct)
        return datetime.datetime.fromtimestamp(tstamp)

    @staticmethod
    def pick_time(comment):
        """
        In comment find time entry

        :param comment: text
        :type comment: string
        :return: (string, string)
        """
        pattern = '\b*(\d\d:\d\d-\d\d:\d\d)[ *]+(.*)'
        try:
            res = re.search(pattern, comment).groups()
        except:
            res = ('?', comment)
        return res

    @staticmethod
    def split_filename(filename):
        pattern = '(.*)(\.[a-zA-Z]{2,3})'
        return re.search(pattern, filename).groups()