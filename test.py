import unittest

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def run_unit_tests():
	print(f"{bcolors.OKBLUE}\nRunning unit tests\n{bcolors.ENDC}")
	loader = unittest.TestLoader()
	suite = loader.discover("solver/blackbox_tests/unit")
	runner = unittest.TextTestRunner()
	runner.run(suite)
	
def run_integration_tests():
	print(f"{bcolors.OKBLUE}\nRunning integration tests\n{bcolors.ENDC}")
	loader = unittest.TestLoader()
	suite = loader.discover("solver/blackbox_tests/integrated")
	runner = unittest.TextTestRunner()
	runner.run(suite)

def run_system_tests():
	print(f"{bcolors.OKBLUE}\nRunning system tests\n{bcolors.ENDC}")
	loader = unittest.TestLoader()
	suite = loader.discover("solver/blackbox_tests/system")
	runner = unittest.TextTestRunner()
	runner.run(suite)

if __name__ == "__main__":
	run_unit_tests()
	run_integration_tests()
	run_system_tests()