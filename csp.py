import csv
from ney_spec import desired_ney

EMPTY_VALUE = (0, 0, 0, 0, 0)

csp = {
	"X": set(["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4",
				"D1", "D2", "D3", "E1", "E2", "F1", "F2", "G"
	]),
	"C": {
		"h1_length": ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4",
					"D1", "D2", "D3", "E1", "E2", "F1", "F2", "G"
		],
		"no_overlap": ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4",
					"D1", "D2", "D3", "E1", "E2",	"F1", "F2", "G"
		],
		"len_decrement": ["B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4",
						"D1", "D2", "D3", "E1", "E2", "F1", "F2"
		],
		"h2_startof_n6": ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4",
					"D1", "D2", "D3", "E1", "E2"
		],
		"h3_endof_n5": ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4",
					"D1", "D2", "D3", "E1", "E2"
		],
		"h4_on_n5": ["A",	"B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4",
					"D1", "D2", "D3"
		],
		"h5_on_n5": ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4",
					"D1", "D2", "D3"
		],
		"h6_end_n4": ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4",
					"D1", "D2", "D3"
		],				
		"chunks_similar": ["B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4",
					"D1", "D2", "D3"
		],		
		"h7_on_n4": ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4"],
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
	"D": {},
	"X_C": {},
	"confset": {},
	"R": {}
}

def init_domain(csp):
	f = open("measures_of_drained_pieces.csv")
	reader = csv.reader(f)
	domain = set([])
	optional_vars= set(["B2", "B3", "B4", "C2", "C3", "C4", 
		"D2", "D3", "E2", "F2"])
	for piece in reader:
		length_mm = float(piece[1]) * 10 # cm -> mm
		# "chunk minimum length" constraint
		if length_mm < desired_ney["min_chunk_l"]:
			continue
		for length in range(20, int(length_mm) + 1):
			no = piece[0]
			l = length
			th = float(piece[2])
			r = float(piece[3])
			d = float(piece[4])
			domain.add((no, l, th, r, d))
	for var in csp["X"]:
		csp["D"][var] = domain.copy()
		if var in optional_vars:
			csp["D"][var].add(EMPTY_VALUE)

def assigned_vars(asmnt):
	'''Preserving the order, extracts assigned variables from asmnt.'''
	return [_asmnt[0] for _asmnt in asmnt]

def remove_var(var, asmnt):
	for i, a in enumerate(asmnt):
		if var == a[0]:
			del asmnt[i]

def update_consts(csp):
	for var in csp["X"]:
		for constraint, variables in csp["C"].items(): 
			if var in variables:
				csp["X_C"][var].add(constraint)
	
def init_csp():
	init_domain(csp)
	for var in csp["X"]:
		csp["confset"][var] = []
		csp["X_C"][var] = set([])
	update_consts(csp)
	return csp
