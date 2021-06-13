import unittest
import datetime
from task import conv_endian, conv_num, my_datetime


class TestCase(unittest.TestCase):

    # Test basic bad input with regular arguments
    def testEndian1(self):
        self.assertEqual(conv_endian(0, 'bogus'), None)

    # Test basic bad input with named arguments
    def testEndian2(self):
        self.assertEqual(conv_endian(num=0, endian='bogus'), None)

    # Begin implementing big endian function
    def testEndian3(self):
        self.assertEqual(conv_endian(954786, 'big'), '0E 91 A2')

    # Same input with different argument structure
    def testEndian4(self):
        self.assertEqual(conv_endian(954786, 'big'), '0E 91 A2')

    # Testing big-endian with negative input
    def testEndian5(self):
        self.assertEqual(conv_endian(-954786, 'big'), '-0E 91 A2')

    # Testing little endian
    def testEndian6(self):
        self.assertEqual(conv_endian(954786, 'little'), 'A2 91 0E')

    # Testing little endian with negative integers
    def testEndian7(self):
        self.assertEqual(conv_endian(-954786, 'little'), '-A2 91 0E')

    # Testing named variables with little endian / negative number
    def testEndian8(self):
        self.assertEqual(conv_endian(
                         num=-954786, endian='little'), '-A2 91 0E')

    # Now adding new tests for rubustness/confidence
    def testEndian9(self):
        self.assertEqual(conv_endian(num=50, endian='big'), '32')

    def testEndian10(self):
        self.assertEqual(conv_endian(num=50, endian='little'), '32')

    # Single byte ints
    def testEndian11(self):
        self.assertEqual(conv_endian(num=10, endian='big'), '0A')

    def testEndian12(self):
        self.assertEqual(conv_endian(num=10, endian='little'), '0A')

    # Zero?
    def testEndian13(self):
        self.assertEqual(conv_endian(0, endian='big'), '00')

    def testEndian14(self):
        self.assertEqual(conv_endian(0, endian='little'), '00')

    # More single byte ints
    def testEndian15(self):
        self.assertEqual(conv_endian(num=-10, endian='big'), '-0A')

    def testEndian16(self):
        self.assertEqual(conv_endian(num=-10, endian='little'), '-0A')

    def testEndian17(self):
        self.assertEqual(conv_endian(num=255, endian='big'), 'FF')

    def testEndian18(self):
        self.assertEqual(conv_endian(num=255, endian='little'), 'FF')

    def testEndian19(self):
        self.assertEqual(conv_endian(num=-255, endian='big'), '-FF')

    def testEndian20(self):
        self.assertEqual(conv_endian(num=-255, endian='little'), '-FF')

    # Thinking bigger
    def testEndian21(self):
        self.assertEqual(conv_endian(123456789), '07 5B CD 15')

    def testEndian22(self):
        self.assertEqual(conv_endian(123456789, 'big'), '07 5B CD 15')

    def testEndian23(self):
        self.assertEqual(conv_endian(123456789, 'little'), '15 CD 5B 07')

    def testEndian24(self):
        self.assertEqual(conv_endian(-123456789, 'big'), '-07 5B CD 15')

    def testEndian25(self):
        self.assertEqual(conv_endian(
                         num=-123456789, endian='little'), '-15 CD 5B 07')

    # Just going to add a few more..
    def testEndian26(self):
        self.assertEqual(conv_endian(9999999999), '02 54 0B E3 FF')

    def testEndian27(self):
        self.assertEqual(conv_endian(-9999999999), '-02 54 0B E3 FF')

    def testEndian28(self):
        self.assertEqual(conv_endian(-9999999999, 'little'), '-FF E3 0B 54 02')

    def testEndian29(self):
        self.assertEqual(conv_endian(
                         -9999999999999, 'little'), '-FF 9F 72 4E 18 09')

    def testEndian30(self):
        self.assertEqual(conv_endian(-0, 'little'), '00')

    def testEndian31(self):
        self.assertEqual(conv_endian(-1, endian='little'), '-01')

    # valid pos int
    def test_cn_1(self):
        val = conv_num('12345')
        # print(val, type(val))
        # uncomment any of test_cn prints to verify type equality
        self.assertEqual(val, 12345)

    # valid neg int
    def test_cn_1_1(self):
        val = conv_num('-2341')
        self.assertEqual(val, -2341)

    # valid neg float
    def test_cn_2(self):
        val = conv_num('-123.45')
        # print(val, type(val))
        self.assertEqual(val, -123.45)

    # valid pos float
    def test_cn_2_1(self):
        val = conv_num('123.45')
        self.assertEqual(val, 123.45)

    # valid pos float < 1
    def test_cn_3(self):
        val = conv_num('.45')
        # print(val, type(val))
        self.assertEqual(val, 0.45)

    # valid neg float > -1
    def test_cn_3_1(self):
        val = conv_num('-.45')
        self.assertEqual(val, -.45)

    # valid pos whole num float
    def test_cn_4(self):
        val = conv_num('123.')
        # print(val, type(val))
        self.assertEqual(val, 123.0)

    # valid neg whole num float
    def test_cn_4_1(self):
        val = conv_num('-123.')
        self.assertEqual(val, -123.0)

    # valid pos hex
    def test_cn_5(self):
        val = conv_num('0xAD4')
        self.assertEqual(val, 2772)

    # valid neg hex
    def test_cn_5_1(self):
        val = conv_num('-0xAD4')
        self.assertEqual(val, -2772)

    # invalid hex char
    def test_cn_6(self):
        val = conv_num('0xAZ4')
        self.assertEqual(val, None)

    # invalid hex char fp
    def test_cn_6_1(self):
        val = conv_num('0xA.4')
        self.assertEqual(val, None)

    # invalid int with hex alpha char
    def test_cn_7(self):
        val = conv_num('12345A')
        self.assertEqual(val, None)

    # > 1 floating point
    def test_cn_8(self):
        val = conv_num('12.3.45')
        self.assertEqual(val, None)

    # int zero
    def test_cn_9(self):
        val = conv_num('0')
        self.assertEqual(val, 0)

    # float zero
    def test_cn_10(self):
        val = conv_num('0.0')
        # print(type(val))
        self.assertEqual(val, 0.0)

    # negative at end
    def test_cn_11(self):
        val = conv_num('293-')
        self.assertEqual(val, None)

    # negative in middle
    def test_cn_12(self):
        val = conv_num('4234-23423')
        self.assertEqual(val, None)

    # wrong int arg type
    def test_cn_13(self):
        val = conv_num(1238423)
        self.assertEqual(val, None)

    # wrong list arg type
    def test_cn_14(self):
        val = conv_num([1, 2, 3, 4])
        self.assertEqual(val, None)

    # First Test Present Time
    def test_date_1(self):
        timestamp = datetime.datetime.utcfromtimestamp(1622479133)
        timestamp = timestamp.strftime('%m-%d-%Y')
        dt = my_datetime(1622479133)
        self.assertEqual(timestamp, dt)

    # Test Future Time
    def test_date_2(self):
        timestamp = datetime.datetime.utcfromtimestamp(190932620400)
        timestamp = timestamp.strftime('%m-%d-%Y')
        dt = my_datetime(190932620400)
        self.assertEqual(timestamp, dt)

    # Test Past Time
    def test_date_3(self):
        timestamp = datetime.datetime.utcfromtimestamp(1670400)
        timestamp = timestamp.strftime('%m-%d-%Y')
        dt = my_datetime(1670400)
        self.assertEqual(timestamp, dt)

    # Test 9999 Max Year Time
    def test_date_4(self):
        timestamp = datetime.datetime.utcfromtimestamp(253372435200)
        timestamp = timestamp.strftime('%m-%d-%Y')
        dt = my_datetime(253372435200)
        self.assertEqual(timestamp, dt)


if __name__ == '__main__':
    unittest.main()
