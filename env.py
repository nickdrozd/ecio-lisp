# ENV consists of pair [ {<env vals>}, [<lower env / empty>] ]

def lookup(reg):
	frame, lower = fetch(ENV)
	var = fetch(reg)
	
	while frame:
		if var in frame:
			return frame[var]
		elif lower:
			frame, lower = lower
		else:
			return 'UNBOUND'

def defineVar():
	frame, lower = fetch(ENV)
	var, val = fetch(UNEV), fetch(VAL)
	frame[var] = val
	# write frame to ENV

def setVar()
	frame, lower = fetch(ENV)
	var, val = fetch(UNEV), fetch(VAL)

	while frame:
		if var in frame:
			frame[var] = val
			# write frame to ENV
		elif lower:
			frame, lower = lower
		else:
			pass
			# raise exception? return dummy val