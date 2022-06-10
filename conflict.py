'''
Conflict set of each variable is a sorted list. Preserving the order in which new
variables are added to the conflict set is important. Backjump callback 
picks the latest variable in the conflict set.
'''

def accum_confset(csp, asmnt, confset, curvar):
	'''Accumulates the conflict set for curvar.
	
	A set of variables in valid assignments in the past that exhausted curvar.
	Examples:
		{A, E1}
		{A}
		{B1}
	'''
	ordered_confset = set([a[0] for a in asmnt if a[0] in confset and a[0] != curvar])
	if not ordered_confset in csp["confset"][curvar]: # prevent duplicates
		csp["confset"][curvar].append(set(ordered_confset))

def absorb_confset(csp, curvar, origin_confset):
	'''Absorbing conflict set from jump origin.
	
	We need to know what set of variables contradict the future.
	'''
	for o_confset in origin_confset:
		if not o_confset in csp["confset"][curvar]:
			csp["confset"][curvar].append(o_confset)
