import csv
from constants import *

class TREE(object):
	def __init__(self, key=None, meta=0):
		self.children = []
		self.key = key
		self.meta = meta
		
	def add_child(self, key=None, meta=0):
		child = TREE(key, meta)
		self.children.append(child)
		return child
	
	def update_meta(self, meta):
		self.meta = meta	
	
	def has_child(self, key):
		if self.get_child(key) != NODE_NOT_FOUND:
			return True
		return False
	
	def get_child(self, key):
		for child in self.children:
			if key == child.key:
				return child
		return NODE_NOT_FOUND

class CATALOG(object):
	'''
	Builds up 6 B+Tree indices to enable quick enquiries of the following formats:

	- What diameters exist in the stock?
		catalog.values("D")
		
	- What diameters exist in the stock, given thickness=2.0mm?
		catalog.values("D", {"TH": "2.0"})
		
	- What thicknesses exist in the stock, given diameter=18.0mm?
		catalog.values("TH", {"D": "18.0"})
		
	- What is the length of all nodes in the stock?
		catalog.getL()

	- What is the length of all nodes with diameter=18.0mm?
		catalog.getL({"D": 18.0})

	- What is the length of all nodes with diameter=18.0mm and thickness=2.0?
		catalog.getL({"D": 18.0, "TH": 2.0})
		
	- What is the length of all nodes with diameter=18.0mm and thickness=2.0 and roundness=0.0mm?
		catalog.getL({"D": "18.0", "TH": "2.0", "R": "0.0"})

	* Any combinations of TH, R, and D could be given as filters to both values and getL methods.
	* Both methods execute in constant time.	
	'''
	def locate_index(self, filters, key=""):
		'''Figures out which index can be used W.R.T. key and filters.'''
		path = ""
		for filter_key in filters.keys():
			path += filter_key
		path += key
		ind2path = {
			"DRTH": set(["D", "DR", "DRTH"]),
			"DTHR": set(["DTH", "DTHR"]),
			"RDTH": set(["R", "RD", "RDTH"]),
			"RTHD": set(["RTH", "RTHD"]),
			"THRD": set(["TH", "THR", "THRD"]),
			"THDR": set(["THD", "THDR"]),
		}
		for index, paths in ind2path.items():
			if path in paths:
				return index
		return None
	
	def locate_node(self, index, filters):
		cursor = self.indices[index]["tree"]
		for index_key in self.indices[index]["keys"]:
			if index_key in filters.keys():
				cursor = cursor.get_child(filters[index_key])
			if cursor == NODE_NOT_FOUND:
				break
		return cursor
			
	def values(self, key="D", filters={}):
		'''Returns values for key, given the filters (one or two of D,TH,R)'''
		index = self.locate_index(filters, key=key)
		if index == None:
			raise Exception("Index could not be found.", filters, key)
		node = self.locate_node(index, filters)
		if node == NODE_NOT_FOUND:
			return set([])
		values = set([])
		for child in node.children:
			values.add(child.key)
		return values		
	
	def get_l(self, filters={}):
		'''Given the filters, searchs in indices for L.'''
		if filters == {}:
			index = "DRTH" 				# any index would do
			node = self.indices[index]["tree"] # root
		else:
			index = self.locate_index(filters)
			node = self.locate_node(index, filters)
		if node != NODE_NOT_FOUND:
			return node.meta # L
		return 0

	def index(self, TH, D, R, L):
		'''Adds the given data to all indices.'''
		vals = {
			"D": D,
			"R": R,
			"TH": TH
		}
		for index in self.indices.values():
			cursor = index["tree"]
			root_meta = cursor.meta + L
			cursor.update_meta(cursor.meta + L)	# root
			for index_key in index["keys"]:
				node_key = vals[index_key]
				if not cursor.has_child(node_key):
					cursor = cursor.add_child(node_key, 0)
				else:
					cursor = cursor.get_child(node_key)
				node_meta = cursor.meta + L
				cursor.update_meta(node_meta)
					
	def __init__(self, csvfile):
		self.indices = {
			"DRTH":	{
				"keys": ["D", "R", "TH"],
				"tree": TREE(),
			},
			"DTHR":	{
				"keys": ["D", "TH", "R"],
				"tree": TREE(),
			},
			"THDR":	{
				"keys": ["TH", "D", "R"],
				"tree": TREE(),
			},
			"THRD":	{
				"keys": ["TH", "R", "D"],
				"tree": TREE(),
			},
			"RTHD":	{
				"keys": ["R", "TH", "D"],
				"tree": TREE(),
			},
			"RDTH":	{
				"keys": ["R", "D", "TH"],
				"tree": TREE(),
			}
		}
		with open(csvfile) as f:
			reader = csv.reader(f)
			for p in reader:
				NO = p[0]
				L = float(p[1]) * 10 # cm -> mm
				TH = float(p[2])
				R = float(p[3])
				D = float(p[4])			
				self.index(TH, D, R, L)
