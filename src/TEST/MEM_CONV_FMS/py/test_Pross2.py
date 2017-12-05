
import unittest


class ProssTestCase(unittest.TestCase):

    def setUp(self):
        self.fout = open("output.txt", 'r')
        self.fespe= open("esperado.txt", 'r')

    def test_conv(self):
        for i in range(438):
            self.assertEqual(self.fout.readline(), self.fespe.readline())

    def tearDown(self):
        self.fout.close()
        self.fespe.close()