import csv

def init_domain(CSP, desired_ney):
	f = open("measures_of_drained_pieces.csv")
	reader = csv.reader(f)
	domain = []
	for piece in reader:
		piece_length_mm = float(piece[1]) * 10 # mm -> cm

		# Enforcing chunk minimum length constraint
		if piece_length_mm < desired_ney["min_chunk_l"]:
			continue

		domain[piece[0]] = {
			"length":			piece_length_mm, 
			"thickness":		float(piece[2]),
			"roundness":		float(piece[3]),
			"diameter":		float(piece[4]),
			"chunk":			(0, piece_length_mm)
		}

	for var in CSP["X"]:
		CSP["D"][var] = domain

def update_piece(CSP, piece_number, assigned_chunk, desired_ney):
	assigned_chunk_l = assigned_chunk[1] - assigned_chunk[0] # in mm
	
	for var in CSP["D"]:
		var_d = CSP["D"][var]
		piece = var_d[piece_number]
		
		# the whole piace has been assigned
		# [..........]
		if piece["length"] == assigned_chunk_l:
			del CSP["D"][var][piece_number]
			continue
		
		# if the left part of the piece has been assigned
		if assigned_chunk[0] == piece["chunk"][0]:
			# [...].......
			right = piece
			right["length"] = piece["length"] - assigned_chunk[1]
			if right["length"] >= desired_ney["min_chunk_l"]:
				# [.........]. is not the case						
				right["chunk"] = (0, right["length"])
				CSP["D"][var][piece_number + "_r"] = right
			
		# if the right part of the piece has been assigned			
		elif assigned_chunk[1] == piece["chunk"][1]:
			# .......[...]
			left = piece
			left["length"] = piece["length"] - assigned_chunk[1]
			if left["length"] >= desired_ney["min_chunk_l"]:
				# .[.........] is not the case			
				left["chunk"] = (0, left["length"])
				CSP["D"][var][piece_number + "_l"] = left
			
		# if a middle part of the piece has been assigned			
		else:
			# ....[...]...
			right = piece
			right["length"] = piece["length"] - assigned_chunk[1]
			if right["length"] >= desired_ney["min_chunk_l"]:
				# ..[.........]. is not the case
				right["chunk"] = (0, right["length"])
				CSP["D"][var][piece_number + "_r"] = right
			
			left = piece
			left["length"] = piece["length"] - assigned_chunk[1]
			if left["length"] >= desired_ney["min_chunk_l"]:
				# .[.........].. is not the case
				left["chunk"] = (0, left["length"])
				CSP["D"][var][piece_number + "_l"] = left			
		
		del CSP["D"][var][piece_number]