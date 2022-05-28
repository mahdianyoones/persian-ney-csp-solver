from constraints import top_diameter, top_llower, top_lupper

# Makes A node consistent
def make_A_consistent(csp):
	csp["D"]["A"] = set(filter(lambda chunk: top_diameter(chunk) and \
		top_llower(chunk) and \
		top_lupper(chunk),
	csp["D"]["A"]))
