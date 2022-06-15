from constraints import *
from csp import assigned_vars, update_consts
from conflict import accum_confset
import os
discarded_no_goods = 0

# References to constraints callbacks 
constraints_ref = {
	"h1_length" 		: h1_length,
	"no_overlap"		: no_overlap,
	"len_decrement"	: len_decrement,
	"h2_startof_n6"	: h2_startof_n6,
	"h3_endof_n5"		: h3_endof_n5,
	"h4_on_n5"		: h4_on_n5,
	"h5_on_n5"		: h5_on_n5,
	"h6_end_n4"		: h6_end_n4,
	"chunks_similar"	: chunks_similar,
	"h7_on_n4"		: h7_on_n4,
	"nodes_similar"	: nodes_similar,
	"diam_diff"		: diam_diff,
	"ddiff_similar"	: ddiff_similar,
	"n3n4_llower"		: n3n4_llower,
	"n1_half_n2"		: n1_half_n2,
	"n5_chunks_sim"	: n5_chunks_sim,
	"n6_chunks_sim"	: n6_chunks_sim,
	"n6_llower"		: n6_llower,
	"n5_llower"		: n5_llower,
	"top_diameter"		: top_diameter,
	"top_llower"		: top_llower,
	"top_lupper"		: top_lupper
}	

def satisfies(csp, const, asmnt):
	asmnt_dict = {a[0]: a[1] for a in asmnt}
	return constraints_ref[const](asmnt_dict)

#def forward_check(csp, asmnt, curvar):
	

def is_consistent(csp, asmnt, curvar, value):
	'''Checks if curvar: value violates the given assignments.
	
	Assumes the given assignments(asmnt) are already consistent.
	'''
	# Check for learned constraints
	_asmnt = asmnt.copy()
	_asmnt.append((curvar, value))
	if len(csp["learned_consts"]) > 0:
		for lc_vars in csp["learned_consts"]:
			const = str(list(lc_vars))
			subasmnt = [a for a in _asmnt if a[0] in lc_vars]
			if len(subasmnt) == len(lc_vars):
				if tuple(subasmnt) in csp["R"][const]:
					return (False, lc_vars)
	# Check for standard constraints
	if len(asmnt) == 0: # leaves unary constraints alone
		return (True, None)
	consts = set([])
	for assigned_var in assigned_vars(asmnt):
		consts.update(csp["X_C"][curvar].intersection(csp["X_C"][assigned_var]))
	for const in consts:
		if not const in csp["R"]:
			sat_res = satisfies(csp, const, _asmnt)
			if sat_res[0] == False:
				return sat_res
	return (True, None)

# node consistency
def make_A_consistent(csp):
	for value in csp["D"]["A"].copy():
		asmnt = [("A", value)]
		res1 = satisfies(csp, "top_diameter", asmnt)
		res2 = satisfies(csp,"top_llower", asmnt)
		res3 = satisfies(csp, "top_lupper", asmnt)
		if not res1[0] or not res2[0] or not res3[0]:
			csp["D"]["A"].remove(value)

def learn_constraint(csp, asmnt, confset, curvar):
	confvars = [a[0] for a in asmnt if a[0] in confset and a[0] != curvar]
	constraint = str(confvars)
	if constraint == "[]":
		print(asmnt, confset, curvar)
		exit()
	if not constraint in csp["C"]:
		csp["C"][constraint] = confvars
		csp["R"][constraint] = set([])
	no_good = [(a[0], a[1]) for a in asmnt if a[0] in confvars]
	no_good = tuple(no_good)
	csp["R"][constraint].add(no_good)
	csp["learned_consts"].add(tuple(confvars))

def consistent_values(csp, asmnt, curvar):
	'''Returns consistent values W.R.T. the given assignments.
	
	Does nothing to unary constraints; the assumption is that they are
	made consistent before search starts.
	'''
	values = set([])
	for value in csp["D"][curvar]:
		cons_res = is_consistent(csp, asmnt, curvar, value)
		if cons_res[0]:
			values.add(value)
	if len(values) == 0: # store the latest conflict that exhausted the domain
		accum_confset(csp, asmnt, cons_res[1], curvar)
		learn_constraint(csp, asmnt, cons_res[1], curvar)
	return values
