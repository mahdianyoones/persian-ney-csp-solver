import csv
from ney_spec import desired_ney

VAR_NOT_USED None

def init_domain(csp):
	f = open("measures_of_drained_pieces.csv")
	reader = csv.reader(f)
	domain = []
	for piece in reader:
		length_mm = float(piece[1]) * 10 # mm -> cm
		# "chunk minimum length" constraint
		if length_mm < desired_ney["min_chunk_l"]:
			continue
		for length in range(20, int(length_mm) + 1):
			chunk = {
				"NO": 	piece[0], 
				"L": 	length,
				"TH": 	float(piece[2]),
				"R":		float(piece[3]),
				"D":		float(piece[4])) 
			}
			domain.append(chunk)
	for var in csp["X"]:
		csp["D"][var] = domain
		if var in csp["optional_vars"]:
			csp["D"][var].append(VAR_NOT_USED)
