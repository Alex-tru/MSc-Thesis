#!/usr/bin/python

Nnodes = 2945
fix = ""


with open("all2.msh", "r") as f:
	f.readline()
	for i in xrange(Nnodes):
		line = f.readline()
		node = line.strip().split(",")
		if float(node[-1]) == 0. or float(node[-1]) == 8.:
			fix += node[0] + ", \n"

with open("fix2.nam", "w") as f:
	f.write("*NSET,NSET=Nfix \n")
	f.write(fix)
