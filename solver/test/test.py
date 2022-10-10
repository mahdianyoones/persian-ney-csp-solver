import unittest
import test_hole1
import test_hole3
import test_hole6
import test_len
import test_sameround
import test_samethick
import test_half
import test_diamdec
import test_lendec
import test_pickup
import test_stock

cases = [
	test_hole1,
	test_hole3,
	test_hole6,
	test_len,
	test_sameround,
	test_samethick,
	test_half,
	test_diamdec,
	test_lendec,
	test_pickup,
	test_stock
]

if __name__ == "__main__":
	runner = unittest.TextTestRunner()
	for case in cases:
		suite = unittest.loader.findTestCases(case)
		runner.run(suite)
