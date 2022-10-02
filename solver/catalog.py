import csv
import copy
from constants import *

class TREE():

	def __init__(self, key=None, meta=0):
		self.__children = []
		self.__children_keys = set([])
		self.__key = key
		self.__meta = meta

	def add_child(self, key, meta=0):
		child = TREE(key, meta)
		self.__children.append(child)
		self.__children_keys.add(key)
		return child

	def update_meta(self, meta):
		self.meta = meta	
	
	def has_child(self, key):
		return key in self.__children_keys
		
	def get_chkeys(self):
		return self.__children_keys
	
	def get_meta(self):
		return self.__meta
	
	def get_key(self):
		return self.__key
		
	def get_child(self, key):
		if not self.has_child(key):
			return NODE_NOT_FOUND
		for child in self.__children:
			if key == child.get_key():
				return child

class INDEX():

	def __init__(self, idx_name):
		self.__keys = idx_name.split("-")		
		self.__head = TREE()

	def index(self, T, D, R, L):
		'''Adds the given chunk data to the index.'''
		self.__build_route(T, D, R)
		vals = {"D": D, "R": R, "T": T}
		cursor = self.__head
		for key in self.__keys:
			cursor.update_meta(cursor.get_meta() + L)
			cursor = cursor.get_child(vals[key])
	
	def __build_route(self, T, D, R):
		'''Creates nodes for the abset steps in the route.
		
		This function does not add L to the route.'''
		vals = {"D": D, "R": R, "T": T}
		cursor = self.__head
		for key in self.__keys:
			if not cursor.has_child(vals[key]):
				cursor = cursor.add_child(vals[key])
			else:		
				cursor = cursor.get_child(vals[key])
					
	def find(self, filters):
		'''Finds the node in the index tree given the filters.
		
		This is a mathematical function.'''
		cursor = self.__head
		if filters == {}:
			return cursor
		for key in self.__keys:			
			if key in filters:
				cursor = cursor.get_child(filters[key])
				if cursor == NODE_NOT_FOUND:
					return NODE_NOT_FOUND
		return cursor
				
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
	def __init__(self):
		self.__idxs = {}
		self.__routes = {}

	def setup(self, csvfile=""):
		'''Performs everything required before a query can be executed.
		
		This is the first method to invoke, after instantiating an object
		from the CATALOG class.'''
		self.__build_idx_objects()
		if csvfile != "":
				self.add_from_csv(csvfile)
		self.__setup_query()

	def values(self, key, filters={}):
		'''Returns values for key, filters include one or two of D,TH,R.'''
		idx = self.__locate_idx(filters, key=key)
		node = idx.find(filters)
		if node != NODE_NOT_FOUND:
			return node.get_chkeys()
		return set([])
	
	def l(self, filters={}):
		'''Given the filters, searchs in indices for L.'''
		idx = self.__locate_idx(filters)
		node = idx.find(filters)
		if node != NODE_NOT_FOUND:
			return node.get_meta()
		return 0.0

	def add_from_csv(self, csvfile):
		with open(csvfile) as f:
			reader = csv.reader(f)
			for p in reader:
				NO = p[0]
				L = float(p[1]) * 10 # cm -> mm
				T = float(p[2])
				R = float(p[3])
				D = float(p[4])
				self.add_piece(T, D, R, L)

	def add_piece(self, T, D, R, L):
		for idx in self.__idxs.values():
			idx.index(T, D, R, L)

	def __setup_query(self):
		'''Helps find the appropriate index given the filters.'''
		for idx_name in self.__idx_names():
			steps = idx_name.split('-')
			route1 = steps[0]
			route2 = steps[0] + steps[1]
			route3 = steps[0] + steps[1] + steps[2]
			for route in [route1, route2, route3]:
				if not route in self.__routes:
					self.__routes[route] = idx_name

	def __idx_names(self):
		return {	"D-R-T", "D-T-R", 
				"R-D-T", "R-T-D",
				"T-D-R", "T-R-D"}
	
	def __build_idx_objects(self):
		for idx_name in self.__idx_names():
			self.__idxs[idx_name] = INDEX(idx_name)
		
	def __locate_idx(self, filters, key=""):
		'''Returns an index that can be queried against.
		
		This is a mathematical function.'''
		route = "".join(filters.keys()) + key
		idx_name = ""
		if route == "":
			idx_name = "T-R-D" # any index would do
		elif route in self.__routes:
			idx_name = self.__routes[route]
		if idx_name == "":
			raise Exception("Index not found.", filters, key, route)
			return None
		return self.__idxs[idx_name]
