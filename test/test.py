import unittest
import init_thdr

test_modules = [init_thdr]

if __name__ == "__main__":
	suite = unittest.loader.findTestCases(init_thdr)
	runner = unittest.TextTestRunner()
	runner.run(suite)
