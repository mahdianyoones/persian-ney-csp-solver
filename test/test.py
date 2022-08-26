import unittest
import initdomains

cases = [initdomains]

if __name__ == "__main__":
	runner = unittest.TextTestRunner()
	for case in cases:
		suite = unittest.loader.findTestCases(initdomains)
		runner.run(suite)
