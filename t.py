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
	"C": {
		"h1_length": [ "A", "B1", "B2", "B3", 
				  	"B4", "C1", "C2", "C3", "C4",
					"D1", "D2", "D3",
					"E1", "E2",
					"F1", "F2",
					"G"
		],
		"no_overlap": [ "A", "B1", "B2", "B3", 
				  	"B4", "C1", "C2", "C3", "C4",
					"D1", "D2", "D3",
					"E1", "E2",
					"F1", "F2",
					"G"
		],
		"len_decrement": [
					# n2 > n3
					"B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4",
					
					# n3 > n4
					"C1", "C2", "C3", "C4", "D1", "D2", "D3",
					
					# n4 > n5
					"D1", "D2", "D3", "E1", "E2",
					
					# n5 > n6
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
					"B1", "B2", "B3", "B4",	# chunks of n2
					"C1", "C2", "C3", "C4",	# chunks of n3
					"D1", "D2", "D3",		# chunks of n4
		],		
		"h7_on_n4": [	
					"A",
					"B1", "B2", "B3", "B4",
					"C1", "C2", "C3", "C4"
		],
		"nodes_similar": [	
					"A", "B1", "C1", "D1", "E1", "F1", "G"
		],
		"diam_diff": [
					"A",	"B1", "C1", "D1", "E1", "F1",	"G"
		],
		"ddiff_similar": [
					"A", "B1", "C1", "D1", "E1", "F1", "G"
		],
		"n3n4_llower": [
					"D1", "D2", "D3", 		# n4 >= 71 (n5 + 1mm)
					"C1", "C2", "C3", "C4"	# n5 >= 72 (n6 + 1mm)
		],		
		"n1_half_n2": [
					"A", "B1", "B2", "B3", "B4"
		],		
		"n5_chunks_sim": [
					"E1", "E2"
		],
		"n6_chunks_sim": [
					"F1", "F2"
		],
		"n6_llower": [
					"F1", "F2" 	# n6 >= 30mm
		],
		"n5_llower": [
					"E1", "E2"	# n5 >= 70mm
		],		
		"top_diameter": [
					"A"
		],
		"top_llower": [
					"A"
		], 	
		"top_lupper": [
					"A"
		]
	},
	"D": {
		"A":  [],
		"B1": [], "B2": [], "B3": [], "B4": [],
		"C1": [], "C2": [], "C3": [], "C4": [],
		"D1": [], "D2": [], "D3": [],
		"E1": [], "E2": [],
		"F1": [], "F2": [],
		"G":  []
	},
	# Constraints that each variable participate in
	"X_C": {
		"A":[
			"h1_length",
			"nodes_similar",
			"diam_diff",
			"h2_startof_n6",
			"h3_endof_n5",
			"h4_on_n5",
			"h5_on_n5",
			"h6_end_n4",
			"h7_on_n4",
			"n1_half_n2",
			"ddiff_similar",
			"top_diameter",
			"top_llower",
			"top_lupper",
			"no_overlap"
		],
		"B1":[
			"h1_length",
			"nodes_similar",
			"diam_diff",
			"h2_startof_n6",
			"h3_endof_n5",
			"h4_on_n5",
			"h5_on_n5",
			"h6_end_n4",
			"h7_on_n4",
			"len_decrement",
			"n1_half_n2",
			"ddiff_similar",
			"chunks_similar",
			"no_overlap"
		],
		"B2":[
			"h1_length",
			"h2_startof_n6",
			"h3_endof_n5",
			"h4_on_n5",
			"h5_on_n5",
			"h6_end_n4",
			"h7_on_n4",
			"len_decrement",
			"n1_half_n2",
			"chunks_similar",
			"no_overlap"
		],
		"B3":[
			"h1_length",
			"h2_startof_n6",
			"h3_endof_n5",
			"h4_on_n5",
			"h5_on_n5",
			"h6_end_n4",
			"h7_on_n4",
			"len_decrement",
			"n1_half_n2",
			"chunks_similar",
			"no_overlap"
		],
		"B4":[
			"h1_length",
			"h2_startof_n6",
			"h3_endof_n5",
			"h4_on_n5",
			"h5_on_n5",
			"h6_end_n4",
			"h7_on_n4",
			"len_decrement",
			"n1_half_n2",
			"chunks_similar",
			"no_overlap"
		],
		"C1":[
			"h1_length",
			"nodes_similar",
			"diam_diff",
			"h2_startof_n6",
			"h3_endof_n5",
			"h4_on_n5",
			"h5_on_n5",
			"h6_end_n4",
			"h7_on_n4",
			"len_decrement",
			"ddiff_similar",
			"chunks_similar",
			"n3n4_llower",
			"no_overlap"
		],
		"C2":[
			"h1_length",
			"h2_startof_n6",
			"h3_endof_n5",
			"h4_on_n5",
			"h5_on_n5",
			"h6_end_n4",
			"h7_on_n4",
			"len_decrement",
			"chunks_similar",
			"n3n4_llower",
			"no_overlap"
		],
		"C3":[
			"h1_length",
			"h2_startof_n6",
			"h3_endof_n5",
			"h4_on_n5",
			"h5_on_n5",
			"h6_end_n4",
			"h7_on_n4",
			"len_decrement",
			"chunks_similar",
			"n3n4_llower",
			"no_overlap"
		],
		"C4":[
			"h1_length",
			"h2_startof_n6",
			"h3_endof_n5",
			"h4_on_n5",
			"h5_on_n5",
			"h6_end_n4",
			"h7_on_n4",
			"len_decrement",
			"chunks_similar",
			"n3n4_llower",
			"no_overlap"
		],
		"D1":[
			"h1_length",
			"nodes_similar",
			"diam_diff",
			"h2_startof_n6",
			"h3_endof_n5",
			"h4_on_n5",
			"h5_on_n5",
			"h6_end_n4",
			"len_decrement",
			"ddiff_similar",
			"chunks_similar",
			"n3n4_llower",
			"no_overlap"
		],
		"D2":[
			"h1_length",
			"h2_startof_n6",
			"h3_endof_n5",
			"h4_on_n5",
			"h5_on_n5",
			"h6_end_n4",
			"len_decrement",
			"chunks_similar",
			"n3n4_llower",
			"no_overlap"
		],
		"D3":[
			"h1_length",
			"h2_startof_n6",
			"h3_endof_n5",
			"h4_on_n5",
			"h5_on_n5",
			"h6_end_n4",
			"len_decrement",
			"chunks_similar",
			"n3n4_llower",
			"no_overlap"
		],
		"E1":[
			"h1_length",
			"nodes_similar",
			"diam_diff",
			"h2_startof_n6",
			"h3_endof_n5",
			"len_decrement",
			"ddiff_similar",
			"n5_chunks_sim",
			"n5_llower",
			"no_overlap"
		],
		"E2":[
			"h1_length",
			"h2_startof_n6",
			"h3_endof_n5",
			"len_decrement",
			"n5_chunks_sim",
			"n5_llower",
			"no_overlap"
		],
		"F1":[
			"h1_length",
			"nodes_similar",
			"diam_diff",
			"len_decrement",
			"ddiff_similar",
			"n6_chunks_sim",
			"n6_llower",
			"no_overlap"
		],
		"F2":[
			"h1_length",
			"len_decrement",
			"n6_chunks_sim",
			"n6_llower",
			"no_overlap"
		],
		"G":[
			"h1_length",
			"nodes_similar",
			"diam_diff",
			"ddiff_similar",
			"no_overlap"
		]
	}
}

print(csp)
