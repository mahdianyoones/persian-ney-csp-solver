import unittest
import test_initdomains
import test_hole1A
import test_hole1B
import test_hole2
import test_hole3
import test_hole4
import test_hole5
import test_hole6
import test_len

cases = [
	test_initdomains, 
	test_hole1A,
	test_hole1B,
	test_hole2,
	test_hole3,
	test_hole4,
	test_hole5,
	test_hole6,
	test_len
]

if __name__ == "__main__":
	runner = unittest.TextTestRunner()
	for case in cases:
		suite = unittest.loader.findTestCases(case)
		runner.run(suite)
