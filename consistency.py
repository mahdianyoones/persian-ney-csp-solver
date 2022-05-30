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
	common_constraints = set([])
	for constraint in csp["X_C"][var]:
		for assigned_var in assignments.keys():
			if var != assigned_var and assigned_var in csp["C"][constraint]:
				common_constraints.add(constraint)
	_assignments = assignments.copy()
	_assignments[var] = value
	for constraint in common_constraints:
		if not satisfies(constraint, assignments):
			return False
	return True

# node consistency
def make_A_consistent(csp):
	b = []
	for index, value in enumerate(csp["D"]["A"]):
		if not top_diameter(value) or not top_llower(value) or not \
			top_lupper(value):
				continue
		b.append(value)
	csp["D"]["A"] = b
