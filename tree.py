from constants import *

class TREE():

	def __init__(self, key=None, meta=0):
		self.children = []
		self.children_keys = set([])
		self.key = key
		self.meta = meta
		
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
	
	def get_child(self, key):
		if not self.has_child(key):
			return NODE_NOT_FOUND
		for child in self.children:
			if key == child.key:
				return child
