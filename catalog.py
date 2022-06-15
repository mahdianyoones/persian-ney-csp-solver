import csv
from ney_spec import spec
import pprint

class Tree(object):
	def __init__(self, key=None, val=0):
		self.children = []
		self.key = key
		self.val = val
		
	def addChild(self, key=None, val=0):
		child = Tree(key, val)
		self.children.append(child)
		return child
	
	def updateVal(self, val):
		self.val = val
		
	def getVal(self):
		return self.val
	
	def getKey(self):
		return self.key
	
	def hasChild(self, key):
		if self.getChild(key):
			return True
		return False
	
	def getChild(self, key):
		for child in self.children:
			if key == child.getKey():
				return child
		return None
	
	def getChildren(self):
		return self.children
	
class catalog(object):

	def values(self, key="D", filters={}):
		'''Returns values for key, given the filters (one or two of D,TH,R)'''
		fKeys = ""
		for f in filters.keys():
			fKeys += f
		fKeys += key
		idx2filters = {
			"DRTH": set(["D", "DR", "DRTH"]),
			"DTHR": set(["DTH", "DTHR"]),
			"RDTH": set(["R", "RD", "RDTH"]),
			"RTHD": set(["RTH", "RTHD"]),
			"THRD": set(["TH", "THR", "THRD"]),
			"THDR": set(["THD", "THDR"]),
		}
		for idx, _filters in idx2filters.items():
			if fKeys in _filters:
				cursor = self.idxs[idx]["tree"]
				break
		for k in self.idxs[idx]["keys"]:
			if k in filters.keys():
				cursor = cursor.getChild(filters[k])
		values = set([])
		for child in cursor.getChildren():
			values.add(child.getKey())
		return values
	
	def getL(self, filters={}):
		if filters == {}:
			idx = "DRTH" # any index would do
			cursor = self.idxs[idx]["tree"] 
		else:
			fKeys = ""
			for f in filters.keys():
				fKeys += f
			idx2filters = {
				"DRTH": set(["D", "DR", "DRTH"]),
				"DTHR": set(["DTH", "DTHR"]),
				"RDTH": set(["R", "RD", "RDTH"]),
				"RTHD": set(["RTH", "RTHD"]),
				"THRD": set(["TH", "THR", "THRD"]),
				"THDR": set(["THD", "THDR"]),
			}
			for idx, _filters in idx2filters.items():
				if fKeys in _filters:
					cursor = self.idxs[idx]["tree"]
					break
		for k in self.idxs[idx]["keys"]:
			if k in filters.keys():
				cursor = cursor.getChild(filters[k])
		return cursor.getVal()

	def index(self, TH, D, R, L):
		vals = {
			"D": str(D),
			"R": str(R),
			"TH": str(TH)
		}
		for idx in self.idxs.values():
			cursor = idx["tree"]
			cursor.updateVal(cursor.getVal() + L)	# root
			for key in idx["keys"]:
				if not cursor.hasChild(vals[key]):
					cursor = cursor.addChild(vals[key], 0)
				else:
					cursor = cursor.getChild(vals[key])
				cursor.updateVal(cursor.getVal() + L)
					
	def __init__(self, csvfile):
		self.idxs = {
			"DRTH":	{
				"keys": ("D", "R", "TH"),
				"tree": Tree(),
			},
			"DTHR":	{
				"keys": ("D", "TH", "R"),
				"tree": Tree(),
			},
			"THDR":	{
				"keys": ("TH", "D", "R"),
				"tree": Tree(),
			},
			"THRD":	{
				"keys": ("TH", "R", "D"),
				"tree": Tree(),
			},
			"RTHD":	{
				"keys": ("R", "TH", "D"),
				"tree": Tree(),
			},
			"RDTH":	{
				"keys": ("R", "D", "TH"),
				"tree": Tree(),
			}
		}
		f = open(csvfile)
		reader = csv.reader(f)
		for p in reader:
			NO = p[0]
			L = float(p[1]) * 10 # cm -> mm
			TH = float(p[2])
			R = float(p[3])
			D = float(p[4])			
			self.index(TH, D, R, L)
		
ca = catalog("measures_of_drained_pieces.csv")
print("Thicknesses: ", ca.values("TH"))
print("Roundnesses: ", ca.values("R"))
print("Diameters: ", ca.values("D"))

print(ca.values("TH", {"R": "2.0"}))
print(ca.getL({"R": "2.0", "TH": "2.0", "D": "19.5"}))
print(ca.getL({"TH": "1.0"}))
print(ca.getL())
