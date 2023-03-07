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

def run_all_tests():
	print(f"{bcolors.OKBLUE}\nRunning all test cases\n{bcolors.ENDC}")
	loader = unittest.TestLoader()
	suite = loader.discover("blackbox_tests")
	runner = unittest.TextTestRunner()
	runner.run(suite)

if __name__ == "__main__":
	run_all_tests()