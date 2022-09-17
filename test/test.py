import unittest
import test_initdomains
import test_hole1A
import test_hole1B

cases = [
	test_initdomains, 
	test_hole1A,
	test_hole1B
]

if __name__ == "__main__":
	runner = unittest.TextTestRunner()
	for case in cases:
		suite = unittest.loader.findTestCases(case)
		runner.run(suite)
