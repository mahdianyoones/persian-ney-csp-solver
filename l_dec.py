from constants import *

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
	
	def establish(self, asmnt, curvar, value):
		impacted = set({})
		for i in range(int(curvar[1])+1, 8): # curvar up to L7
			li = "L"+str(i)
			if value != None:
				curvar_d = {"min": value, "max": value}
			else:
				curvar_d = self.csp.D[curvar]
			last_d = self.csp.D["L"+str(i)]
			new_max = curvar_d["max"] - 1
			new_min = curvar_d["min"] * 2/3 if i < 7 else last_d["min"]
			if new_max < new_min:
				return (CONTRADICTION, set([]))
			reduced = False
			if new_max < last_d["max"] or new_min > last_d["min"]:
				new_d = last_d.copy()
				new_d["max"] = new_max
				new_d["min"] = new_min
				impacted.add(li)
				self.csp.update_d(li, new_d)
				reduced = True
			if reduced:
				curvar = li
			else:
				break # stop propagating nothing!
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)
		else:
			return (DOMAINS_INTACT, None)		
