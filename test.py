import unittest
from constraints import *
from consistency import *
from csp import init_csp

def value(th = 0, r = 0, d = 0, l = 0, no = 0):
	return (no, l, th, r, d)

class TestConstraints(unittest.TestCase):

	def test_nodes_similar(self):
		asmnt = [
			("A", value(th=2.0,r=0.0)),
			("B1", value(th=2.0,r=0.0)),
			("C1", value(th=2.0,r=0.0)),
			("D1", value(th=2.0,r=0.0)),
			("E1", value(th=2.0,r=0.0)),
			("F1", value(th=2.0,r=0.0)),
			("G", value(th=2.0,r=0.0))
		]
		res = satisfies("nodes_similar", asmnt)
		self.assertTrue(res[0])
		
		asmnt = [
			("A", value(th=2.0,r=0.0)),
			("B1", value(th=2.0,r=0.0)),
			("C1", value(th=2.0,r=0.0)),
			("D1", value(th=2.0,r=0.0)),
			("E1", value(th=2.0,r=1.0)),
			("F1", value(th=2.0,r=0.0)),
			("G", value(th=2.0,r=0.0))
		]
		res = satisfies("nodes_similar", asmnt)
		self.assertFalse(res[0])
		
		asmnt = [
			("A", value(th=2.0,r=0.0)),
			("B1", value(th=2.0,r=0.0)),
			("D1", value(th=2.0,r=0.0)),
			("E1", value(th=2.0,r=0.0)),
		]
		res = satisfies("nodes_similar", asmnt)
		self.assertTrue(res[0])

		asmnt = [
			("A", value(th=2.1,r=0.0)),
			("B1", value(th=2.0,r=0.0)),
			("D1", value(th=2.0,r=0.0)),
			("E1", value(th=2.0,r=0.0)),
		]
		res = satisfies("nodes_similar", asmnt)
		self.assertFalse(res[0])
		
	def test_diam_diff(self):
		asmnt = [
			("A", value(d=17.5)),
			("B1", value(d=18.0))
		]
		self.assertEqual(satisfies("diam_diff", asmnt), (False, {"A", "B1"}))
		
		asmnt = [
			("A", value(d=18.0)),
			("B1", value(d=18.0))
		]
		self.assertEqual(satisfies("diam_diff", asmnt), (False, {"A", "B1"}))
		
		asmnt = [
			("A", value(d=18.5)),
			("B1", value(d=18.0))
		]
		self.assertEqual(satisfies("diam_diff", asmnt), (True, None))
		
		asmnt = [
			("B1", value(d=18.0)),
			("A", value(d=18.5)),
			("C1", value(d=17.5))
		]
		self.assertEqual(satisfies("diam_diff", asmnt), (True, None))
		
		asmnt = [
			("A", value(d=18.5)),
			("B1", value(d=18.0)),
			("C1", value(d=18.0))
		]
		self.assertEqual(satisfies("diam_diff", asmnt), (False, {"B1", "C1"}))
		
		asmnt = [
			("B1", value(d=18.0))
		]
		self.assertEqual(satisfies("diam_diff", asmnt), (True, None))
		
		asmnt = [
			("B1", value(d=18.0)),
			("D1", value(d=17.5)),
		]
		self.assertEqual(satisfies("diam_diff", asmnt), (True, None))
		
		asmnt = [
			("F1", value(d=18.0)),
			("G", value(d=17.5)),
		]
		self.assertEqual(satisfies("diam_diff", asmnt), (True, None))
		
		asmnt = [
			("F1", value(d=18.0)),
			("G", value(d=17.5)),
		]
		self.assertEqual(satisfies("diam_diff", asmnt), (True, None))
		
		asmnt = [
			('A', value(no='175',l=27,th=2.5,r=0.0,d=18.0)),
			('B1', value(no='478',l=20,th=2.5,r=0.0,d=19.0))
		]
		self.assertEqual(satisfies("diam_diff", asmnt), (False, {"A", "B1"}))


class TestConsistency(unittest.TestCase):

	def test_is_conistent(self):
		csp = init_csp()
		make_A_consistent(csp)
		self.assertEqual(len(csp["D"]["A"]), 666)
		
		asmnt = [
			('A', value(no='10',l=10,th=2.0,r=0.0,d=18.0)),
		]
		val = value(no='10',l=10,th=2.5,r=1.0,d=18.0)
		self.assertEqual(is_consistent(csp, asmnt, "B1", val), (False, {"A", "B1"}))
		
if __name__ == '__main__':
	unittest.main()
