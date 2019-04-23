import timeit
from unittest import TestCase

from parser.parser import Parser


class ParseTimingTest(TestCase):

    def test_parse_timing(self):
        test_sent = 'ومن وقتاش رجعت تحكي معاه المدير؟'
        start_time = timeit.default_timer()
        p = Parser(test_sent)
        p.parse()
        print('Runtime: ',timeit.default_timer() - start_time)
        return