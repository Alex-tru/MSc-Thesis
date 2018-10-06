#!/usr/bin/python

#Nnodes = 2945
#Nnodes = 19809
#Nnodes = 3231
#Nnodes = 2080
Nnodes = 5736
#Nelements = 512
#Nelements = 4096
#Nelements = 544
#Nelements = 4096
Nelements = 11264


Npart1 = ""
Npart2 = ""
Epart1 = ""
Epart2 = ""

Nodes1 = []
Nodes2 = []

with open("CalculixMono/CalculixMesh/all_pipe.msh", "r") as f:
	f.readline()
	for i in xrange(Nnodes):
		line = f.readline()
		node = line.strip().split(",")
		if float(node[-2]) <= 6000.001:
			Nodes1.append(int(node[0]))
			Npart1 += line
		if float(node[-2]) >= 5999.999:
			Nodes2.append(int(node[0]))
			Npart2 += line
	f.readline()
	for i in xrange(Nelements):
		#here read as many lines as necessary, depending on how many lines an element spans in all.msh
		line = f.readline() 
		el = line.strip().split(",")
		el_nodes = el[1:]
		# if all nodes of current element belong to part 1
		if all([int(x) in Nodes1 for x in el_nodes]):
			Epart1 += line
		elif all([int(x) in Nodes2 for x in el_nodes]):
			Epart2 += line

with open("Calculix1/Calculix1Mesh/all_pipe.msh", "w") as f:
	f.write("*NODE, NSET=Nall \n")
	f.write(Npart1)
	f.write("*ELEMENT, TYPE=S3   , ELSET=Eall \n")
	f.write(Epart1)

with open("Calculix2/Calculix2Mesh/all_pipe.msh", "w") as f:
	f.write("*NODE, NSET=Nall \n")
	f.write(Npart2)
	f.write("*ELEMENT, TYPE=S3, ELSET=Eall \n")
	f.write(Epart2)
