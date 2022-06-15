'''
Conflict set of each variable is a sorted list. Preserving the order in which new
variables are added to the conflict set is important. Backjump callback 
picks the latest variable in the conflict set.
'''

def accum_confset(csp, asmnt, confset, curvar):
	'''Accumulates the conflict set for curvar.'''
	for cfv in [a[0] for a in asmnt if a[0] in confset and a[0] != curvar]:
		if not cfv in csp["confset"][curvar]: # prevent duplicates
			csp["confset"][curvar].append(cfv)

def absorb_confset(csp, curvar, jump_origin):
	'''Absorbing conflict set from jump origin.
	
	We need to know what set of variables contradict the future.
	'''
	origin_confset = csp["confset"][jump_origin]
	for o_confset in [v for v in origin_confset if v !=curvar]:
		if not o_confset in csp["confset"][curvar]:
			csp["confset"][curvar].append(o_confset)
