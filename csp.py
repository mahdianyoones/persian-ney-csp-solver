from domain import init_domain

csp = {
	"X": [
					"A",					# n1
					"B1", "B2", "B3", "B4",	# n2
					"C1", "C2", "C3", "C4",	# n3
					"D1", "D2", "D3",		# n4
					"E1", "E2",			# n5
					"F1", "F2",			# n6
					"G"					# n7
	],
	"optional_vars": ["B2", "B3", "B4", "C2", "C3", "C4", "D2", "D3", "E2", "F2"],
	"C": {
		"h1_length": [ "A",
					"B1", "B2", "B3", "B4", 
				  	"C1", "C2", "C3", "C4",
					"D1", "D2", "D3",
					"E1", "E2",
					"F1", "F2",
					"G"
		],
		"no_overlap": [ "A",
					"B1", "B2", "B3", "B4",
				  	"C1", "C2", "C3", "C4",
					"D1", "D2", "D3",
					"E1", "E2",
					"F1", "F2",
					"G"
		],
		"len_decrement": [
					"B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4",
					"C1", "C2", "C3", "C4", "D1", "D2", "D3",
					"D1", "D2", "D3", "E1", "E2",
					"E1", "E2", "F1", "F2"
		],
		"h2_startof_n6": [
					"A",
					"B1", "B2", "B3", "B4",
					"C1", "C2", "C3", "C4",
					"D1", "D2", "D3", 
					"E1", "E2"
		],
		"h3_endof_n5": [	
					"A",
					"B1", "B2", "B3", "B4",
					"C1", "C2", "C3", "C4",
					"D1", "D2", "D3",
					"E1", "E2"
		],
		"h4_on_n5": [	
					"A",
					"B1", "B2", "B3", "B4",
					"C1", "C2", "C3", "C4",
					"D1", "D2", "D3"
		],
		"h5_on_n5": [	
					"A",
					"B1", "B2", "B3", "B4",
					"C1", "C2", "C3", "C4",
					"D1", "D2", "D3"
		],
		"h6_end_n4": [
					"A",
					"B1", "B2", "B3", "B4",
					"C1", "C2", "C3", "C4",
					"D1", "D2", "D3"
		],				
		"chunks_similar": [
					"B1", "B2", "B3", "B4",
					"C1", "C2", "C3", "C4",
					"D1", "D2", "D3"
		],		
		"h7_on_n4": [	
					"A",
					"B1", "B2", "B3", "B4",
					"C1", "C2", "C3", "C4"
		],
		"nodes_similar": ["A", "B1", "C1", "D1", "E1", "F1", "G"],
		"diam_diff": ["A",	"B1", "C1", "D1", "E1", "F1",	"G"],
		"ddiff_similar": ["A", "B1", "C1", "D1", "E1", "F1", "G"],
		"n3n4_llower": ["C1", "C2", "C3", "C4", "D1", "D2", "D3"],		
		"n1_half_n2": ["A", "B1", "B2", "B3", "B4"],		
		"n5_chunks_sim": ["E1", "E2"],
		"n6_chunks_sim": ["F1", "F2"],
		"n6_llower": ["F1", "F2"],
		"n5_llower": ["E1", "E2"],		
		"top_diameter": ["A"],
		"top_llower": ["A"], 	
		"top_lupper": ["A"]
	},
	# variable: [its values]
	"D": {},
	# variable: [its constraints]
	"X_C": {}
}

def init_csp():
	init_domain(_csp)
	for var in csp["X"]:
		csp["X_C"][var] = set([])
		for constraint, variables in csp["C"].items(): 
			if var in variables:
				csp["X_C"][var].add(constraint)
	return csp
