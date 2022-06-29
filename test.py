import unittest
from catalog import CATALOG
from constants import *
from holes import HOLES
from len import LEN
from l_dec import L_DEC
from d_dec import D_DEC
from same_thr import SAME_THR
from l1_half_l2 import L1_HALF_L2
from in_stock import IN_STOCK
from ney_spec import spec
from assignment import ASSIGNMENT
from csp import CSP

class TestCatalog(unittest.TestCase):

	def test_get_l(self):
		self.catalog = CATALOG("measures_of_drained_pieces.csv")
		er = [
			(441, {"TH": 1.0}),
			(215, {"TH": 1.0,  "R": 1.0}),
			(40, {"TH": 1.0,  "R": 1.5}),
			(120, {"TH": 1.0,  "R": 1.0,  "D": 13.5}),
			(7323, {"TH": 2.0}),
			(578, {"TH": 2.0,  "R": 1.0,  "D": 21.0}),
			(55, {"TH": 3.0,  "R": 0.5,  "D": 19.0}),
			(60, {"TH": 3.5,  "R": 1.5,  "D": 17.5}),
			(60, {"TH": 3.5,  "R": 1.5}),
			(60, {"TH": 3.5}),
			(2661, {"R": 0.0}),
			(185, {"D": 21.5}),
			(26, {"D": 23.5}),
			(47, {"D": 21.5,  "R": 0.0}),
			(138, {"D": 21.5,  "TH": 2.0,  "R": 0.5}),
			(0, {"D": 87.5,  "TH": 2.0,  "R": 0.5}),
		]
		for _er in er:
			expected = _er[0]
			filters = _er[1]
			returned = self.catalog.get_l(filters)
			self.assertEqual(expected, returned)
	
	def test_values(self):
		self.catalog = CATALOG("measures_of_drained_pieces.csv")
		er = [
			({1.0, 1.5, 0.5}, ("R", {"D": 18.0, "TH": 3.0})),
			({0.0,  0.5,  1.0,  1.5}, ("R", {"TH": 1.0})),
			({18.0,  25.0,  19.0}, ("D", {"TH": 3.0,  "R": 0.5})),
			({13.5,  14.5,  15.0,  16.0}, ("D", {"TH": 1.0,  "R": 1.0})),
			({3.5,  2.5}, ("TH", {"R": 1.5,  "D": 17.5}))
		]
		for _er in er:
			expected = _er[0]
			key = _er[1][0]
			filters = _er[1][1]
			returned = self.catalog.values(key, filters)
			self.assertEqual(expected, returned)

'''
The initial domains:

{
	'L1': {'min': 20, 'max': inf},
	'L2': {'min': 20, 'max': inf}, 
	'L3': {'min': 20, 'max': inf}, 
	'L4': {'min': 50, 'max': inf},
	'L5': {'min': 70, 'max': inf},
	'L6': {'min': 30, 'max': inf}, 
	'L7': {'min': 20, 'max': inf}, 
	'D1': {18.5, 18.0, 19.0, 20.5, 21.0, 21.5, 20.0, 19.5, 23.5, 24.0}, 
	'D2': {13.5, 14.0, 15.0, 14.5, 15.5, 18.5, 16.5, 17.5, 
		  18.0, 19.0, 20.5, 21.0, 21.5, 20.0, 19.5, 23.5, 
		  25.0, 24.0, 16.0, 17.0}, 
	'D3': {13.5, 14.0, 15.0, 14.5, 15.5, 18.5, 16.5, 17.5, 
	       18.0, 19.0, 20.5, 21.0, 21.5, 20.0, 19.5, 23.5, 
	       25.0, 24.0, 16.0, 17.0}, 
	'D4': {13.5, 14.0, 15.0, 14.5, 15.5, 18.5, 16.5, 17.5, 
		  18.0, 19.0, 20.5, 21.0, 21.5, 20.0, 19.5, 23.5, 
		  25.0, 24.0, 16.0, 17.0}, 
	'D5': {13.5, 14.0, 15.0, 14.5, 15.5, 18.5, 16.5, 17.5, 
	       18.0, 19.0, 20.5, 21.0, 21.5, 20.0, 19.5, 23.5, 
	       25.0, 24.0, 16.0, 17.0}, 
	'D6': {13.5, 14.0, 15.0, 14.5, 15.5, 18.5, 16.5, 17.5, 
	       18.0, 19.0, 20.5, 21.0, 21.5, 20.0, 19.5, 23.5, 
	       25.0, 24.0, 16.0, 17.0}, 
	'D7': {13.5, 14.0, 15.0, 14.5, 15.5, 18.5, 16.5, 17.5, 
	       18.0, 19.0, 20.5, 21.0, 21.5, 20.0, 19.5, 23.5, 
	       25.0, 24.0, 16.0, 17.0}, 
	'R1': {0.0, 0.5, 2.0, 1.0, 1.5, 2.5}, 
	'R2': {0.0, 0.5, 2.0, 1.0, 1.5, 2.5}, 
	'R3': {0.0, 0.5, 2.0, 1.0, 1.5, 2.5}, 
	'R4': {0.0, 0.5, 2.0, 1.0, 1.5, 2.5}, 
	'R5': {0.0, 0.5, 2.0, 1.0, 1.5, 2.5}, 
	'R6': {0.0, 0.5, 2.0, 1.0, 1.5, 2.5}, 
	'R7': {0.0, 0.5, 2.0, 1.0, 1.5, 2.5}, 
	'TH1': {1.5, 2.5, 3.0, 2.0, 1.0, 2.1, 3.5}, 
	'TH2': {1.5, 2.5, 3.0, 2.0, 1.0, 2.1, 3.5}, 
	'TH3': {1.5, 2.5, 3.0, 2.0, 1.0, 2.1, 3.5}, 
	'TH4': {1.5, 2.5, 3.0, 2.0, 1.0, 2.1, 3.5}, 
	'TH5': {1.5, 2.5, 3.0, 2.0, 1.0, 2.1, 3.5}, 
	'TH6': {1.5, 2.5, 3.0, 2.0, 1.0, 2.1, 3.5}
	'TH7': {1.5, 2.5, 3.0, 2.0, 1.0, 2.1, 3.5}, 
}
'''
	
class TestDDEC(unittest.TestCase):

	def d_dec_1(self, csp, asmnt, d_dec):
		res = d_dec.b_update(asmnt)
		impacted_exp = {"D2", "D3", "D3", "D4", "D5", "D6", "D7"}
		self.assertEqual(res[1], impacted_exp)		
		ddiff = csp.spec["ddiff"]
		prev_upper = max(csp.D["D1"])
		for i in range(2, 8):
			di = "D"+str(i)
			upper = max(csp.D[di])
			self.assertTrue(upper <= prev_upper - ddiff["min"])
			prev_upper = upper
	
	def d_dec_2(self, csp, asmnt, d_dec):
		res = d_dec.establish(asmnt, "D1", 18)
		impacted_exp = {"D2", "D3", "D3", "D4", "D5", "D6", "D7"}
		self.assertEqual(res[1], impacted_exp)
		ddiff = csp.spec["ddiff"]
		prev_upper = 18
		for i in range(2, 8):
			di = "D"+str(i)
			upper = max(csp.D[di])
			self.assertTrue(upper <= prev_upper - ddiff["min"])
			prev_upper = upper

	def d_dec_3(self, csp, asmnt, d_dec):
		impacted_exp = {"D7"}
		res = d_dec.establish(asmnt, "D6", 15.0)
		self.assertEqual(res[1], impacted_exp)
	
	def test_d_dec(self):
		catalog = CATALOG("measures_of_drained_pieces.csv")
		csp = CSP(catalog, spec)
		asmnt = ASSIGNMENT(csp)		
		d_dec = D_DEC(csp)
		self.d_dec_1(csp, asmnt, d_dec)
		self.d_dec_2(csp, asmnt, d_dec)
		self.d_dec_3(csp, asmnt, d_dec)

class TestL1_HALF_L2(unittest.TestCase):

	def half_1(self, catalog, csp, asmnt, half):
		res = half.b_update(asmnt)
		self.assertEqual(res[1], {"L2"}) # L2 only is expected to be impacted		
		L1 = csp.D["L1"]
		L2 = csp.D["L2"]
		self.assertTrue(L2["min"] == L1["min"] * 2)
		self.assertTrue(L2["max"] == L1["max"] * 2)

	def half_2(self, catalog, csp, asmnt, half):
		half.establish(asmnt, "L1", 25)
		L2 = csp.D["L2"]
		self.assertTrue(L2["max"] == 50)
	
	def half_3(self, catalog, csp, asmnt, half):
		csp.D["L1"] = {"min": 30, "max": 100}
		csp.D["L2"] = {"min": 40, "max": 400}
		res = half.b_update(asmnt)
		self.assertEqual(res[1], {"L2"}) # L2 only is expected to be impacted
		L1 = csp.D["L1"]
		L2 = csp.D["L2"]
		self.assertTrue(L2["min"] == L1["min"] * 2)
		self.assertTrue(L2["max"] == L1["max"] * 2)

	def half_4(self, catalog, csp, asmnt, half):
		csp.D["L1"] = {"min": 30, "max": 100}
		csp.D["L2"] = {"min": 80, "max": 200}
		res = half.b_update(asmnt)
		self.assertEqual(res[1], {"L1"}) # L2 only is expected to be impacted
		L1 = csp.D["L1"]
		L2 = csp.D["L2"]
		self.assertTrue(L2["min"] == L1["min"] * 2)
		self.assertTrue(L2["max"] == L1["max"] * 2)

	def test_half(self):
		catalog = CATALOG("measures_of_drained_pieces.csv")
		csp = CSP(catalog, spec)
		asmnt = ASSIGNMENT(csp)		
		half = L1_HALF_L2(csp)
		self.half_1(catalog, csp, asmnt, half)
		self.half_2(catalog, csp, asmnt, half)
		self.half_3(catalog, csp, asmnt, half)
		self.half_4(catalog, csp, asmnt, half)

class TestIN_STOCK(unittest.TestCase):

	def stock_3(self, catalog, csp, asmnt, in_stock):
		csp.revert_d()
		res = in_stock.establish(asmnt, "TH1", 3)
		asmnt.assign("TH1", 3)
		res = in_stock.establish(asmnt, "R1", 0.5)
		asmnt.assign("R1", 0.5)
		self.assertEqual({18, 19, 25}, csp.D["D1"])
		self.assertEqual(csp.D["L1"]["max"], 85+55+25)
		res = in_stock.establish(asmnt, "D1", 19)
		asmnt.assign("D1", 19)
		self.assertEqual(csp.D["L1"]["max"], 55)
		
	def stock_2(self, catalog, csp, asmnt, in_stock):
		csp.revert_d()
		res = in_stock.establish(asmnt, "TH1", 3)
		asmnt.assign("TH1", 3)
		res = in_stock.establish(asmnt, "R1", 1)
		self.assertTrue(not "TH1" in res[1])
		self.assertEqual({18}, csp.D["D1"])
		
	def stock_1(self, catalog, csp, asmnt, in_stock):
		res = in_stock.establish(asmnt, "TH1", 3.5)
		self.assertEqual(res[1], {"D1", "R1", "L1"})
		self.assertEqual(csp.D["D1"], {17.5})		
		self.assertEqual(csp.D["R1"], {1.5})
		self.assertEqual(csp.D["L1"]["max"], 60)		
		
	def test_stock(self):
		catalog = CATALOG("measures_of_drained_pieces.csv")
		csp = CSP(catalog, spec)
		asmnt = ASSIGNMENT(csp)		
		in_stock = IN_STOCK(csp)
		csp.backup_d()
		self.stock_1(catalog, csp, asmnt, in_stock)
		csp.revert_d()
		csp.backup_d()
		self.stock_2(catalog, csp, asmnt, in_stock)
		csp.revert_d()
		csp.backup_d()
		self.stock_3(catalog, csp, asmnt, in_stock)

class TestSAMETHR(unittest.TestCase):
	
	def test_same_thr(self):
		catalog = CATALOG("measures_of_drained_pieces.csv")
		csp = CSP(catalog, spec)
		asmnt = ASSIGNMENT(csp)		
		same_thr = SAME_THR(csp)
		res = same_thr.establish(asmnt, "R1", 0)
		res = same_thr.establish(asmnt, "TH1", 2)
		for i in range(2, 8):
			thi = "TH"+str(i)
			ri = "R"+str(i)		
			self.assertEqual({0}, csp.D[ri])
			self.assertEqual({2}, csp.D[thi])

if __name__ == '__main__':
	unittest.main()
