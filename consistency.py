from constraints import *
from csp import assigned_vars
from conflict import in_confset
import os
c = 0

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

def satisfies(const, asmnt):
	asmnt_dict = {a[0]: a[1] for a in asmnt}
	return constraints_ref[const](asmnt_dict)

def is_consistent(csp, asmnt, var, value):
	'''Checks consistency of assignments to at least two variables'''
	asmnt_vars = assigned_vars(asmnt)
	if len(asmnt_vars) == 0:
		return (True, None)
	# common constraints between assigned vars and current var
	common_consts = set([])
	for assigned_var in asmnt_vars:
		common_consts.update(csp["X_C"][var].intersection(csp["X_C"][assigned_var]))
	_asmnt = asmnt.copy()
	_asmnt.append(tuple([var, value]))
	for const in common_consts:
		sat_res = satisfies(const, _asmnt)
		if sat_res[0] == False:
			return sat_res
	return (True, None)

# node consistency
def make_A_consistent(csp):
	for value in csp["D"]["A"].copy():
		asmnt = [("A", value)]
		res1 = satisfies("top_diameter", asmnt)
		res2 = satisfies("top_llower", asmnt)
		res3 = satisfies("top_lupper", asmnt)
		if not res1[0] or not res2[0] or not res3[0]:
			csp["D"]["A"].remove(value)

def make_consistent(csp, asmnt, curvar):
	'''Makes curvar consistent with respect to the given assignments'''
	global c
	for value in csp["D"][curvar].copy():
		if in_confset(csp, asmnt, curvar, value):
			csp["D"][curvar].remove(value)
			continue
		cons_res = is_consistent(csp, asmnt, curvar, value)
		if cons_res[0] == False:
			csp["D"][curvar].remove(value)
			confvars = cons_res[1]
			consasmnt = asmnt.copy()
			consasmnt.append((curvar, value))
			csp["confset"][curvar].add(tuple(consasmnt))
			c += 1
			for a in asmnt:
				if a[0] in confvars and a[0] != curvar: # do not add curvar
					if not a[0] in csp["confvars"][curvar]: # prevent duplicates
						csp["confvars"][curvar].append(a[0])
	os.system("clear")
	print("added ", c, "to all conflict sets, latest var:", curvar)
