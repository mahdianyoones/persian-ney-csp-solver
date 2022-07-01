from constants import *

class LOG():

	def __init__(self):
		self.f = open("log.log", "w")
			
	def log(self, **args):
		print("---------------------\n", file=self.f)
		print(args["a"], " : ", args["b"], "\n", file=self.f)
		print(args["f"], " on ", args["g"], "\n", file=self.f)
		print(args["c"][0], ": ", args["c"][1], "\n", file=self.f)
		if args["c"][0] == DOMAINS_REDUCED:
			d = args["d"]
			e = args["e"]
			for v in args["c"][1]:
				msg = "-- " + v + "\n" + args["e"][v]
				msg += "\n" + "=> " + "\n" + args["d"][v] + "\n"
				print(msg,file=self.f)
		if args["r"] != None:
			print("propagated to: ", args["r"],file=self.f)
			
logger = LOG()
