
import unittest


class ProssTestCase(unittest.TestCase):

    def setUp(self):
        self.fout0 = open("out_mem0.txt", 'r')
        self.fout1 = open("out_mem1.txt", 'r')
        self.fout2 = open("out_mem2.txt", 'r')
        self.fout3 = open("out_mem3.txt", 'r')

        self.fespe0 = open("esperado0.txt", 'r')
        self.fespe1 = open("esperado1.txt", 'r')
        self.fespe2 = open("esperado2.txt", 'r')
        self.fespe3 = open("esperado3.txt", 'r')

    def test_conv0(self):
        for i in range(437):
            self.assertEqual(self.fout0.readline(), self.fespe0.readline(), msg="line "+str(i))

    def test_conv1(self):
        for i in range(437):
            self.assertEqual(self.fout1.readline(), self.fespe1.readline(), msg="line "+str(i))

    def test_conv2(self):
        for i in range(438):
            self.assertEqual(self.fout2.readline(), self.fespe2.readline())

    def test_conv3(self):
        for i in range(437):
            self.assertEqual(self.fout3.readline(), self.fespe3.readline())

    def tearDown(self):
        self.fout0.close()
        self.fout1.close()
        self.fout2.close()
        self.fout3.close()
        self.fespe0.close()
        self.fespe1.close()
        self.fespe2.close()
        self.fespe3.close()