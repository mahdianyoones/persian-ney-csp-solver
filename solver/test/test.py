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
import test_mac
import test_lendec_lower
import test_solver
import test_jump

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
	test_stock,
	test_mac,
	test_lendec_lower,
	test_solver,
	test_jump
]

if __name__ == "__main__":
	runner = unittest.TextTestRunner()
	for case in cases:
		suite = unittest.loader.findTestCases(case)
		runner.run(suite)