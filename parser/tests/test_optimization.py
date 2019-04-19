import timeit
from django.test import TestCase

from aeb_parser.parser import parser


class ParseTimingTest(TestCase):

    def test_parse_timing(self):
        test_sent = 'ومن وقتاش رجعت تحكي معاه المدير؟'
        start_time = timeit.default_timer()
        parser(test_sent)
        print('Runtime: ',timeit.default_timer() - start_time)
        return