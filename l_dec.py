from constants import *
import math

class L_DEC():
	'''Applies length decrement consistency.
	
	The following relations must hold:
		L2 > L3 > 2/3 L2
		L3 > L4 > 2/3 L3
		L4 > L5 > 2/3 L4
		L5 > L6 > 2/3 L5
		L6 > L7
	
	If value == None, this is an indirect bound propagation:
	
		upper3 = min(upper3, upper2 - 1)
		upper4 = min(upper4, upper3 - 1)
		upper5 = min(upper5, upper4 - 1)
		upper6 = min(upper6, upper5 - 1)
		upper7 = min(upper7, upper6 - 1)
		
		lower3 = max(lower3, 2/3 lower2)
		lower4 = max(lower4, 2/3 lower3)
		lower5 = max(lower5, 2/3 lower4)
		lower6 = max(lower6, 2/3 lower5)

	if value != None, an L variable is assigned the impact is direct:
	
		upper3 = min(upper3, L2 - 1)
		upper4 = min(upper4, upper3 - 1)
		upper5 = min(upper5, upper4 - 1)
		upper6 = min(upper6, upper5 - 1)
		upper7 = min(upper7, upper6 - 1)
		
		lower3 = max(lower3, 2/3 * L2)
		lower4 = max(lower4, 2/3 lower3)
		lower5 = max(lower5, 2/3 lower4)
		lower6 = max(lower6, 2/3 lower5)
			
	This consistency function is called on two occasions:
		1- An L variable is assigned a value
		2- Domain of an L variable has been reduced
		
		In case 1, we use the assigned value to determine a new 
		consistent range for further variables. For example, if L3 
		is assigned, say, 100, upper bound on L4, L5, L6 reduce to 
		99, 98, 97, and 96 respectively. Furthermore, the lower bounds
		of L4, L5, and L6 reduce to around 66, 44, and 29 respectively.
		i.e. {L3: 100} propagates to
		
			L4 -> [66, 99] 
			L5 -> [44, 98]
			L6 -> [29, 96]
		
		In case 2, we use new bounds on the variable whose domain has
		been reduced. That variable is curvar. For example, if the 
		domain of L3 has reduced to, say, [80, 120], the domain of 
		L4, L5, and L6 change as such:
		
			L4 -> [53, 119]
			L5 -> [35, 118]
			L6 -> [23, 117]
		
		From the two examples above, we can observe that assigning
		values to variables can trigger strongger domain reduction
		in propagation.
	'''

	def __init__(self, csp):
		self.csp = csp
	
	def _establish(self, asmnt, ds, start):		
		uppers = [None, None, 0, 0, 0, 0, 0, 0]
		lowers = [None, None, 0, 0, 0, 0, 0, 0]
		for i in range(2, 8):
			uppers[i] = ds[i]["max"]
			lowers[i] = ds[i]["min"]
		impacted = set([])
		for i in range(start, 8): # 3 to 7
			li = "L"+str(i)
			if li in asmnt.assigned:
				# further variables are already consistent via establish
				break
			if i < 7: # lower of L7 is not restricted
				lowers[i] = max(lowers[i], math.ceil(2/3 * lowers[i-1]))
				lowers[i] = lowers[i] if lowers[i] == float("inf") else \
				 				math.ceil(lowers[i])				
			uppers[i] = min(uppers[i], uppers[i-1] - 1)
			if lowers[i] < ds[i]["min"]:
				return (CONTRADICTION, None)
			if uppers[i] > ds[i]["max"]:
				return (CONTRADICTION, None)
			if lowers[i] > ds[i]["min"] or uppers[i] < ds[i]["max"]:
				self.csp.update_d(li, {"min": lowers[i], "max": uppers[i]})
				impacted.add(li)
		if len(impacted) == 0:
			return (DOMAINS_INTACT, None)
		return (DOMAINS_REDUCED, impacted)
				
	def domains(self, asmnt):
		assignment = asmnt.assignment
		domains = [None, None, 0, 0, 0, 0, 0, 0]
		for i in range(2, 8):
			li = "L"+str(i)
			if li in asmnt.assigned:
				val = assignment[li]
				domains[i] = {"min": val,"max": val}
			else:
				domains[i] = self.csp.D[li]
		return domains

	def b_update(self, asmnt):
		ds = self.domains(asmnt)
		return self._establish(asmnt, ds, 3)
		
	def var_i(self, var):
		if var[0] in {"R", "D", "L"}:
			return int(var[1])
		else:
			return int(var[2])
	
	def var_name(self, var):
		if len(var) == 2:
			return var[0]
		else:
			return var[0:2]

	def establish(self, asmnt, curvar, value):
		if curvar == "L7":
			return (DOMAINS_INTACT, None)
		ds = self.domains(asmnt)
		var_i = self.var_i(curvar)
		ds[var_i] = {"min": value,"max": value}
		return self._establish(asmnt, ds, var_i+1)
