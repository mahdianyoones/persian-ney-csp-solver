from domain import init_domain
from csp import CSP
from consistency import make_arc_consistent, make_A_node_consistent
from select_variable import select_var

# Specification of the desired Ney
desired_ney = {
	"h1":			round(524.4),
	"h2":			round(467.2),
	"h3":			round(428.4),
	"h4":			round(392.9),
	"h5":			round(370.8),
	"h6":			round(350.0),
	"h7":			round(311.8),
	"mp_lenght":		10,			# mouthpiece length
	"h_diameter":		10,			# holes diameter
	"min_top_diam":	18,			# minimum diamter at top
	"min_chunk_l":		20,			# minimum chunk length
	"min_hj_dist":		10,			# minimum distance between holes and junctions
	"min_hh_dist":		10,			# minimum distance between holes
	"diam_diff_lower":	0.5,			# lower bound for diameter diff between adjacent nodes
	"diam_diff_upper":	1.3,			# upper bound for that!
}

init_domain(CSP, desired_ney)
make_A_node_consistent(CSP, desired_ney)

