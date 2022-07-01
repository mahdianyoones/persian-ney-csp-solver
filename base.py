class BASE():
		
	def var_i(self, var):
		if len(var) == 2 and var[0] in {"R", "D", "L"}:
			return int(var[1])
		elif len(var) == 3 and var[0:2] == "TH":
			return int(var[2]) # th
		raise Exception(var, "is not a valid variable name!")
	
	def var_name(self, var):
		if len(var) == 2 and var[0] in {"R", "D", "L"}:
			return var[0]
		elif len(var) == 3 and var[0:2] == "TH":
			return var[0:2]
		raise Exception(var, "is not a valid variable name!")
			
