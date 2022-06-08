from constraints import *

# References to constraints callbacks 
ccs = {
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

def satisfies(constraint, assignments):
	return ccs[constraint](assignments)

def is_consistent(csp, assignments, var, value):
	if len(assignments.keys()) == 0:
		return (True, None)
	common_constraints = set([])
	for constraint in csp["X_C"][var]:
		for assigned_var in assignments.keys():
			if var != assigned_var and assigned_var in csp["C"][constraint]:
				common_constraints.add(constraint)
	_assignments = assignments.copy()
	_assignments[var] = value
	for constraint in common_constraints:	
		sat_res = satisfies(constraint, _assignments)
		if sat_res[0] == False:
			return sat_res
	return (True, None)

# node consistency
def make_A_consistent(csp):
	legal_values = []
	for value in csp["D"]["A"]:
		asmnt = {"A": value}
		res1 = top_diameter(asmnt)
		res2 = top_llower(asmnt)
		res3 = top_lupper(asmnt)
		if res1[0] and res2[0] and res3[0]:
			legal_values.append(value)
	csp["D"]["A"] = legal_values

def make_consistent(csp, asmnt, curvar):
	legal_values = []
	for value in csp["D"][curvar]:
		cons_res = is_consistent(csp, asmnt, curvar, value)
		if cons_res[0]:
			legal_values.append(value)
		else:
			# add the conflict assignment to the conflict set of curvar
			try:
				if curvar in cons_res[1]:
					cons_res[1].remove(curvar)
				confasmnt = {(confvar, tuple(asmnt[confvar].values())) \
					for confvar in cons_res[1]}
				csp["confset"][curvar].update(confasmnt)
				csp["confvars"][curvar].update(cons_res[1])
			except:
				print(cons_res)
				print(asmnt)
				print(curvar)
				print(confasmnt)
#				exit()
	csp["D"][curvar] = legal_values
