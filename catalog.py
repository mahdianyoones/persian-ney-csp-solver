import csv
from constants import *
from tree import TREE

class CATALOG():
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
	def __init__(self, csvfile):
		self.init_indices()
		self.index_csv(csvfile)
	
	def index_csv(self, csvfile):
		with open(csvfile) as f:
			reader = csv.reader(f)
			for p in reader:
				NO = p[0]
				L = float(p[1]) * 10 # cm -> mm
				TH = float(p[2])
				R = float(p[3])
				D = float(p[4])
				self.index(TH, D, R, L)
	
	def init_indices(self):
		self.indices = {}
		self.path2index = {}
		keys = ("D", "R", "TH")
		indices_paths = {
			(keys[0], keys[1], keys[2]), # D, R, TH
			(keys[0], keys[2], keys[1]), # D, TH, R
			(keys[1], keys[0], keys[2]), # R, D, TH
			(keys[1], keys[2], keys[0]), # R, TH, D
			(keys[2], keys[0], keys[1]), # TH, D, R
			(keys[2], keys[1], keys[0]), # TH, R, D
		}
		for paths in indices_paths:
			index_name = ''.join(paths)
			self.indices[index_name] = {
				"keys": keys,
				"tree": TREE(),			
			}
			path_combinations = {
				paths[0],
				paths[0] + paths[1],
				paths[0] + paths[1] + paths[2]
			}
			for path in path_combinations:
				if not path in self.path2index:
					self.path2index[path] = index_name	
	
	def locate_index(self, filters, key=""):
		'''Figures out which index can be used W.R.T. key and filters.'''
		path = "".join(filters.keys()) + key
		if not path in self.path2index:
			return None
		return self.path2index[path]
	
	def locate_node(self, index, filters):
		cursor = self.indices[index]["tree"]
		for index_key in self.indices[index]["keys"]:
			if index_key in filters.keys():
				cursor = cursor.get_child(filters[index_key])
			if cursor == NODE_NOT_FOUND:
				break
		return cursor
	
	def values(self, key, filters={}):
		'''Returns values for key, given the filters (one or two of D,TH,R)'''
		index = self.locate_index(filters, key=key)
		if index == None:
			raise Exception("Index was not found.", filters, key)
		node = self.locate_node(index, filters)
		return node.children_keys if node != NODE_NOT_FOUND else set([])
	
	def get_l(self, filters={}):
		'''Given the filters, searchs in indices for L.'''
		if filters == {}:
			index = self.indices[0] 			# any index would do
			node = self.indices[index]["tree"] # root
		else:
			index = self.locate_index(filters)
			node = self.locate_node(index, filters)
		return node.meta if node != NODE_NOT_FOUND else 0.0
	
	def index(self, TH, D, R, L):
		'''Adds the given chunk data to all indices.'''
		if type(D) == 0:
			raise Exception("D is 0", D)
		if type(L) == 0:
			raise Exception("L is 0", L)
		vals = {"D": D, "R": R, "TH": TH}
		for index in self.indices.values():
			cursor = index["tree"]
			cursor.update_meta(cursor.meta + L)	# root
			for index_key in index["keys"]:
				node_key = vals[index_key]
				if not cursor.has_child(node_key):
					cursor = cursor.add_child(node_key, 0)
				else:
					cursor = cursor.get_child(node_key)
				cursor.update_meta(cursor.meta + L)
