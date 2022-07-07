# Specification of the desired Ney
spec = {
	"len":			round(524.4),				# total height, including the mouthpiece
	"h6":			round(467.2),				# 1st hole from top
	"h5":			round(428.4),				# 2nd hole from top
	"h4":			round(392.9),				# 3rd hole from top
	"h3":			round(370.8),				# 4th hole from top
	"h2":			round(350.0),				# 5th hole from top
	"h1":			round(311.8),				# 6th hole from top
	"mp":			10,						# mouthpiece length
	"holed":			10,						# holes diameter
	"topd":			{"min": 18, "max": 24},		# diamter at top
	"minl":			20,						# minimum chunk length
	"hmarg":			7,						# minimum hole/hole and hole/junction space
	"ddiff":			{"min": 0.5, "max": 1.5},	# diameter difference between adjacent nodes
}
