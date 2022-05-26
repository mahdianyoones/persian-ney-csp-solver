# Notes:
#
# - Contrary nodes, holes are numbered from bottom to top.
# - Length of h1 = the entire length of Ney.
# - The 7th node is allowed to be equal or larger than the 6th one.
# - The 7th node is free to have any size.
# - Enforcing lower bound on the length of chunks (e.g. 20mm) is done 
#		during value assignment.
#		Intially all chunks are taller than this bound.
#		Alternatively, it could be done via constraints. However,
#		that require one new unary constraint on each variable. This may
#		not incur extra computation, but it does make the design a bit messy.
#
# - In a partial solution, at least all requried variables must be assigned.

CSP = {
	"X": [
					"A",					# n1
					"B1", "B2", "B3", "B4",	# n2
					"C1", "C2", "C3", "C4",	# n3
					"D1", "D2", "D3",		# n4
					"E1", "E2",			# n5
					"F1", "F2",			# n6
					"G"					# n7
	],
	"required_vars": [
					"A", "B1", "C1", "D1", "E1", "F1", "G"
	],
	"optional_vars": [
					"B2", "B3", "B4",
					"C2", "C3", "C4",
					"D2", "D3",
					"E2",
					"F2"
	],
	"C": {

		# Enforces the entire length of Ney
		"h1_length": [ "A", "B1", "B2", "B3", 
				  	"B4", "C1", "C2", "C3", "C4",
					"D1", "D2", "D3",
					"E1", "E2",
					"F1", "F2",
					"G"
		],

		# All nodes must be similar in terms of thickness and roundness
		"nodes_similar": [	
					"A", "B1", "C1", "D1", "E1", "F1", "G"
		],
		
		# The diameter of nodes from top to bottom must decrease (conic)
		"diam_diff": [
					"A",	"B1", "C1", "D1", "E1", "F1",	"G"
		],
		
		# Hole 2 must locate at the beginning of the 6th node
		"h2_startof_n6": [
					"A",
					"B1", "B2", "B3", "B4",
					"C1", "C2", "C3", "C4",
					"D1", "D2", "D3", 
					"E1", "E2"
		],
		
		# Hole 3 must locate at the end of the 5th node
		"h3_endof_n5": [	
					"A",
					"B1", "B2", "B3", "B4",
					"C1", "C2", "C3", "C4",
					"D1", "D2", "D3",
					"E1", "E2"
		],
		
		# Hole 4 must locate somewhere on 5th node
		"h4_on_n5": [	
					"A",
					"B1", "B2", "B3", "B4",
					"C1", "C2", "C3", "C4",
					"D1", "D2", "D3"
		],
		
		# Hole 5 must locate somewhere on the 5th node
		"h5_on_n5": [	
					"A",
					"B1", "B2", "B3", "B4",
					"C1", "C2", "C3", "C4",
					"D1", "D2", "D3"
		],
		
		# Hole 6 must locate at the end of the 4th node
		"h6_end_n4": [
					"A",
					"B1", "B2", "B3", "B4",
					"C1", "C2", "C3", "C4",
					"D1", "D2", "D3"
		],
		
		# Hole 7 must locate somewhere on the 4th node
		"h7_on_n4": [	
					"A",
					"B1", "B2", "B3", "B4",
					"C1", "C2", "C3", "C4"
		],
		
		# Enforcing the decrement in length of nodes from top to bottom
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
			
		# Length(node 1) = 1/2 * n2
		"n1_half_n2": [
					"A", "B1", "B2", "B3", "B4"
		],
		
		# Enforcing that the diameter diff between all nodes are the same
		"ddiff_similar": [
					"A", "B1", "C1", "D1", "E1", "F1", "G"
		],
		
		# Enforcing similar qualities between chunks of nodes in terms of 
		# thickness, roundness, and diameter
		"chunks_similar": [
					"B1", "B2", "B3", "B4",	# chunks of n2
					"C1", "C2", "C3", "C4",	# chunks of n3
					"D1", "D2", "D3",		# chunks of n4
		],		
		"n5_chunks_sim": [
					"E1", "E2"
		],
		"n6_chunks_sim": [
					"F1", "F2"
		],
		
		"top_diameter": [
					"A"
		],
		
		# lowe bound for the length of the 1st node
		"top_llower": [
					"A"
		], 	
		
		# upper bound for length of 1st node
		"top_lupper": [
					"A"
		],
		
		# Enforcing lowr bound on the length of nodes
		"n6_llower": [
					"F1", "F2" 	# n6 >= 30mm
		],
		"n5_llower": [
					"E1", "E2"	# n5 >= 70mm
		],
		"n3n4_llower": [
					"D1", "D2", "D3", 		# n4 >= 71 (n5 + 1mm)
					"C1", "C2", "C3", "C4"	# n5 >= 72 (n6 + 1mm)
		],
	},
	"D": {
		"A":  [],
		"B1": [], "B2": [], "B3": [], "B4": [],
		"C1": [], "C2": [], "C3": [], "C4": [],
		"D1": [], "D2": [], "D3": [],
		"E1": [], "E2": [],
		"F1": [], "F2": [],
		"G":  []
	}
}
