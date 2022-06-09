def in_confset(csp, asmnt, curvar, value):
	# is the assignments plus curvar:‌value in the conflict set?
	confasmnt = asmnt.copy()
	confasmnt.append((curvar, value))
	if tuple(confasmnt) in csp["confset"][curvar]:
		return True
	return False
