import unittest

if __name__ == "__main__":
	loader = unittest.TestLoader()
	suite = loader.discover("solver/blackbox_tests")
	runner = unittest.TextTestRunner()
	runner.run(suite)