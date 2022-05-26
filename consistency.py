from constraints import top_diameter, top_llower, top_lupper

def make_A_node_consistent(CSP, desired_ney):
	for piece in CSP["C"]["A"].items():
		if not top_diameter(piece[1], desired_ney) or \
			not top_llower(piece[1], desired_ney) or \
			not top_lupper(piece[1], desired_ney):
				del CSP["C"]["A"][piace[0]]
				

