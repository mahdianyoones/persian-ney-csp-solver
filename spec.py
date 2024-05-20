# Specification of the desired Ney
common_specs = {
	"mp":			9,							# mouthpiece length
	"holed":		9,							# holes diameter
	"topd":			{"min": 21, "max": 24},		# diamter at top
	"minl":			20,							# minimum chunk length
	"hmarg":		4,							# minimum hole/hole and hole/junction space
	"ddiff":		{"min": 0.0, "max": 0.5},		# diameter difference between adjacent nodes
 	"top_ddiff":	{"min": 2.0, "max": 3.0}		# diameter difference between top and second node
}

holes = {}

holes["F_tall"] = {
	"len": round(785.7),
	"h6": round(700.0),
	"h5": round(641.9),
	"h4": round(588.6),
	"h3": round(555.6),
	"h2": round(524.4),
	"h1": round(467.2)
 }
 
holes["G"] = {
	"len": round(700.0),
	"h6": round(623.6),
	"h5": round(571.9),
	"h4": round(524.4),
	"h3": round(495.0),
	"h2": round(467.2),
	"h1": round(416.2) 
 }
 
holes["A"] = {
	"len": round(623.6),
	"h6": round(555.6),
	"h5": round(509.5),
	"h4": round(467.2),
	"h3": round(441.0),
	"h2": round(416.2),
	"h1": round(370.8)
 }
 
holes["Bb"] = {
	"len": round(588.6),
	"h6": round(524.4),
	"h5": round(480.9),
	"h4": round(441.0),
	"h3": round(416.2),
	"h2": round(392.9),
	"h1": round(350.0),
}

holes["C"] = {
	"len": round(524.4),
	"h6": round(467.2),
	"h5": round(428.4),
	"h4": round(392.9),
	"h3": round(370.8),
	"h2": round(350.0),
	"h1": round(311.8)
}

holes["D"] = {
	"len": round(467.2),
	"h6": round(416.2),
	"h5": round(381.7),
	"h4": round(350.0),
	"h3": round(330.4),
	"h2": round(311.8),
	"h1": round(277.8)
}

holes["E"] = {
	"len": round(416.2),
	"h6": round(370.8),
	"h5": round(340.0),
	"h4": round(311.8),
	"h3": round(294.3),
	"h2": round(277.8),
	"h1": round(247.5)
}

holes["F_short"] = {
	"len": round(392.9),
	"h6": round(350.0),
	"h5": round(321.0),
	"h4": round(294.3),
	"h3": round(277.8),
	"h2": round(262.2),
	"h1": round(233.6)
}

specs = {}

for cook, h in holes.items():
	specs[cook] = h
	specs[cook].update(common_specs)
