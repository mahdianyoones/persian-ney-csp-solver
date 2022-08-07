import csv
from constants import *

class TREE():

	def __init__(self, key=None, meta=0):
		self.__children = []
		self.__children_keys = set([])
		self.__key = key
		self.__meta = meta

	def add_child(self, key, meta=0):
		if key in self.children_keys:
			raise Exception("Already has the child ", keys, "!")
		child = TREE(key, meta)
		self.children.append(child)
		self.children_keys.add(key)
		return child

	def update_meta(self, meta):
		self.meta = meta	
	
	def has_child(self, key):
		return key in self.children_keys
	
	def meta(self):
		return self.__meta

	def child(self, key):
		if not self.has_child(key):
			return NODE_NOT_FOUND
		for child in self.children:
			if key == child.key:
				return child
				
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
		self.__indices = {}
		self.__path_to_idx = {}	
		self.init_indices()
		self.index_csv(csvfile)
	
	def __index_csv(self, csvfile):
		with open(csvfile) as f:
			reader = csv.reader(f)
			for p in reader:
				NO = p[0]
				L = float(p[1]) * 10 # cm -> mm
				TH = float(p[2])
				R = float(p[3])
				D = float(p[4])
				self.__index(TH, D, R, L)
	
	def __init_indices(self):
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
			index_name = '-'.join(paths)
			self.__indices[index_name] = {
				"keys": keys,
				"tree": TREE(),			
			}
			path_combinations = {
				paths[0],
				paths[0] + paths[1],
				paths[0] + paths[1] + paths[2]
			}
			for path in path_combinations:
				if not path in self.__path_to_idx:
					self.__path_to_idx[path] = index_name	
	
	def __locate_index(self, filters, key=""):
		'''Figures out which index can be used W.R.T. key and filters.'''
		path = "".join(filters.keys()) + key
		if not path in self.__path_to_idx:
			return None
		return self.__path_to_idx[path]
	
	def __locate_node(self, index, filters):
		cursor = self.__indices[index]["tree"]
		for index_key in self.__indices[index]["keys"]:
			if index_key in filters.keys():
				cursor = cursor.child(filters[index_key])
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
			index = self.__indices[0] 			# any index would do
			node = self.__indices[index]["tree"] # root
		else:
			index = self.locate_index(filters)
			node = self.locate_node(index, filters)
		return node.meta if node != NODE_NOT_FOUND else 0.0
	
	def __build_paths(self, paths, TH, D, R):
		'''Creates nodes for the abset steps in the paths.'''
		vals = {"D": D, "R": R, "TH": TH}
		for idx_name, path in paths.copy().items():
			for i, step in path.enumerate():
				if step["cursor"] != None:
					cursor = step["cursor"]
					continue
				else:
					cursor = cursor.add_child(vals[step["key"]])
					step["cursor"] = cursor
					step["meta"] = cursor.meta()
					paths[idx_name][i] = step
		
	def __index(self, TH, D, R, L):
		'''Adds the given chunk data to all indices.'''
		paths = self._paths(self.__indices, TH, D, R)
		self.__build_paths(paths, TH, D, R)
		paths = self.__update_metas(paths, L)
		for cursor, meta in pairs.items():
			cursor.update_meta(meta)
	
	def __paths(self, indices, TH, D, R):
		'''Determines what paths do not exist and what paths do.
		
		This is a mathematical function.'''
		paths = {}
		vals = {"D": D, "R": R, "TH": TH}
		for idx_name, index in indices.items():
			stepskeys = idx_name.split("-")
			cursor = index["tree"]
			path = []
			step = {
				"cursor": cursor, 
				"key": "root", 
				"meta": cursor.meta()
			}
			path.append(step)
			for stepkey in stepskeys:
				step[key] = stepkey
				if cursor.has_child(vals[stepkey]):
					step["cursor"] = cursor.child(vals[stepkey])
					step["meta"] = step["cursor"].meta()
				else:
					step["cursor"] = None
					step["meta"] = None
				path.append(step)
			paths[idx_name] = path
		return paths
	
	def __update_metas(self, paths, L):
		'''Adds L to all nodes in the paths.
		
		This is a mathematical function.'''
		vals = {"D": D, "R": R, "TH": TH}
		for idx_name, path in paths.items():
			for i, step in pathcopy.enumerate():
				cursor = step["cursor"]
				paths[idx_name][i]["meta"] = step["meta"] + L
		return paths
