# Specification of the desired Ney
desired_ney = {

	# The length of each hole. h7 is equal with the length of entire Ney
	"h1":			round(524.4),
	"h2":			round(467.2),
	"h3":			round(428.4),
	"h4":			round(392.9),
	"h5":			round(370.8),
	"h6":			round(350.0),
	"h7":			round(311.8),
	
	# Specifications related to the top node
	"mp_lenght":		10,			# mouthpiece length
	"h_diameter":		10,			# holes diameter
	"n1_diameter":		18,			# diamter at top
	
	"min_chunk_l":		20,			# minimum chunk length
	
	"min_hj_dist":		10,			# minimum distance between holes and junctions
	"min_hh_dist":		10,			# minimum distance between holes
	
	"diam_diff_lower":	0.5,			# lower bound for diameter diff between adjacent nodes
	"diam_diff_upper":	1.5,			# upper bound for that!
	
	# The following bounds are driven from two constraints:
	# 	1. Node 2 must be double the length of Node 1
	# 	2. Nodes 3 to 6 must increase in length (at least 1mm)
	
	"n1_llower":		36.5,		# lower bound for the length of the top node
								# without considering the length of the mouthpiece
	"n1_lupper":		round(524.4) - 263) / 3, # = 87mm
	
	"n3_llower":		72,			# third node
	"n4_llower":		71,			# fourth node
	"n5_llower":		70,			# fifth node
	"n6_llower":		30			# sixth node
}	
