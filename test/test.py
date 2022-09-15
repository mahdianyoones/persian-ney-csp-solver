import unittest
import test_initdomains
import test_hole1A

cases = [
	test_initdomains, 
	test_hole1A
]

if __name__ == "__main__":
	runner = unittest.TextTestRunner()
	for case in cases:
		suite = unittest.loader.findTestCases(case)
		runner.run(suite)
