import unittest
from constraints import *
from consistency import *
from csp import init_csp

class TestConstraints(unittest.TestCase):

	def test_nodes_similar(self):
		asmnt = {
			"A": {"TH": 2.0, "R": 0},
			"B1": {"TH": 2.0, "R": 0},
			"C1": {"TH": 2.0, "R": 0},
			"D1": {"TH": 2.0, "R": 0},
			"E1": {"TH": 2.0, "R": 0},
			"F1": {"TH": 2.0, "R": 0},
			"G1": {"TH": 2.0, "R": 0}
		}
		self.assertTrue(nodes_similar(asmnt))
		asmnt = {
			"A": {"TH": 2.0, "R": 0},
			"B1": {"TH": 2.0, "R": 0},
			"C1": {"TH": 2.0, "R": 0},
			"D1": {"TH": 2.0, "R": 0},
			"E1": {"TH": 2.0, "R": 1},
			"F1": {"TH": 2.0, "R": 0},
			"G1": {"TH": 2.0, "R": 0}
		}
		self.assertFalse(nodes_similar(asmnt))
		asmnt = {
			"A": {"TH": 2.0, "R": 0},
			"B1": {"TH": 2.0, "R": 0},
			"D1": {"TH": 2.0, "R": 0},
			"E1": {"TH": 2.0, "R": 0},
		}
		self.assertTrue(nodes_similar(asmnt))
		asmnt = {
			"A": {"TH": 2.1, "R": 0},
			"B1": {"TH": 2.0, "R": 0},
			"D1": {"TH": 2.0, "R": 0},
			"E1": {"TH": 2.0, "R": 0},
		}
		self.assertFalse(nodes_similar(asmnt))
		
	def test_diam_diff(self):
		asmnt = {
			"B1": {"D": 18},
			"A": {"D": 17.5}
		}
		self.assertFalse(diam_diff(asmnt))
		
		asmnt = {
			"B1": {"D": 18},
			"A": {"D": 18}
		}
		self.assertFalse(diam_diff(asmnt))
		
		asmnt = {
			"B1": {"D": 18},
			"A": {"D": 18.5}
		}
		self.assertTrue(diam_diff(asmnt))
		
		asmnt = {
			"B1": {"D": 18},
			"A": {"D": 18.5},
			"C1": {"D": 17.5}
		}
		self.assertTrue(diam_diff(asmnt))
		
		asmnt = {
			"B1": {"D": 18},
			"A": {"D": 18.5},
			"C1": {"D": 18}
		}
		self.assertFalse(diam_diff(asmnt))
		
		asmnt = {
			"B1": {"D": 18}
		}
		self.assertTrue(diam_diff(asmnt))
		
		asmnt = {
			"B1": {"D": 18},
			"D1": {"D": 17.5},
		}
		self.assertTrue(diam_diff(asmnt))
		
		asmnt = {
			"F1": {"D": 18},
			"G": {"D": 17.5},
		}
		self.assertTrue(diam_diff(asmnt))	
		
		asmnt = {
			"F1": {"D": 18},
			"G": {"D": 17.5},
		}
		self.assertTrue(diam_diff(asmnt))
		
		asmnt = {
			'A': {'NO': '175', 'L': 27, 'TH': 2.5, 'R': 0.0, 'D': 18.0},
			'B1': {'NO': '478', 'L': 20, 'TH': 2.5, 'R': 0.0, 'D': 19.0}
		}
		self.assertFalse(diam_diff(asmnt))


class TestConsistency(unittest.TestCase):

	def test_is_conistent(self):
		csp = init_csp()
		make_A_consistent(csp)
		self.assertEqual(len(csp["D"]["A"]), 666)
		asmnt = {
			"A": {"NO": 10, "L": 10, "D": 18.0, "R": 0, "TH": 2.0}
		}
		value = {"NO": 10, "L": 10, "D": 18.0, "R": 1.0, "TH": 2.5}
		self.assertFalse(is_consistent(csp, asmnt, "B1", value))
		
if __name__ == '__main__':
	unittest.main()
