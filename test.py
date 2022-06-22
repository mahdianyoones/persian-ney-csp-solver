import unittest
from catalog import CATALOG

class TestCatalog(unittest.TestCase):


	def test_test1(self):
		self.catalog = CATALOG("measures_of_drained_pieces.csv")
		er = [
			({"1.0", "1.5", "0.5"}, ("R", {"D": "18.0", "TH": "3.0"})),
			({"0.0", "0.5", "1.0", "1.5"}, ("R", {"TH": "1.0"})),
			({"18.0", "25.0", "19.0"}, ("D", {"TH": "3.0", "R": "0.5"})),
			({"13.5", "14.5", "15.0", "16.0"}, ("D", {"TH": "1.0", "R": "1.0"})),
			({"3.5", "2.5"}, ("TH", {"R": "1.5", "D": "17.5"}))
		]
		for _er in er:
			expected = _er[0]
			key = _er[1][0]
			filters = _er[1][1]
			returned = self.catalog.values(key, filters)
			self.assertEqual(expected, returned)

		er = [
			(441, {"TH": "1.0"}),
			(215, {"TH": "1.0", "R": "1.0"}),
			(40, {"TH": "1.0", "R": "1.5"}),
			(120, {"TH": "1.0", "R": "1.0", "D": "13.5"}),
			(7323, {"TH": "2.0"}),
			(578, {"TH": "2.0", "R": "1.0", "D": "21.0"}),
			(55, {"TH": "3.0", "R": "0.5", "D": "19.0"}),
			(60, {"TH": "3.5", "R": "1.5", "D": "17.5"}),
			(60, {"TH": "3.5", "R": "1.5"}),
			(60, {"TH": "3.5"}),
			(2661, {"R": "0.0"}),
			(185, {"D": "21.5"}),
			(26, {"D": "23.5"}),
			(47, {"D": "21.5", "R": "0.0"}),
			(138, {"D": "21.5", "TH": "2.0", "R": "0.5"}),
			(0, {"D": "87.5", "TH": "2.0", "R": "0.5"}),
		]
		for _er in er:
			expected = _er[0]
			filters = _er[1]
			returned = self.catalog.get_l(filters)
			self.assertEqual(expected, returned)

if __name__ == '__main__':
	unittest.main()
