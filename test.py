import unittest

def run_unit_tests():
	print("\nRunning unit tests\n")
	loader = unittest.TestLoader()
	suite = loader.discover("solver/blackbox_tests/unit")
	runner = unittest.TextTestRunner()
	runner.run(suite)
	
def run_integration_tests():
	print("\nRunning integration tests\n")
	loader = unittest.TestLoader()
	suite = loader.discover("solver/blackbox_tests/integrated")
	runner = unittest.TextTestRunner()
	runner.run(suite)

if __name__ == "__main__":
	run_unit_tests()
	run_integration_tests()