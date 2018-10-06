#!/usr/bin/python

# adapt this to the mesh you work with
nsize1 = 4320
nsize2 = 1488
nsizem = 5736


def make_planes_mono():

		fix = ""
		interface = ""

		with open("CalculixMono/CalculixMesh/all_pipe.msh", "r") as f:
			f.readline()
			for i in xrange(nsizem):
				line = f.readline()
				node = line.strip().split(",")
				if float(node[-2]) <= 0.01 or float(node[-2]) >= 7999.99:
					fix += node[0] + ", \n"
				if float(node[-2]) <= 6000.01 and float(node[-2]) >= 5999.99:
					interface += node[0] + ", \n"

		# fixed nodes
		with open("CalculixMono/CalculixMesh/fix_pipe.nam", "w") as f:
			f.write("*NSET,NSET=Nfix \n")
			f.write(fix)


def make_planes_part1():

		fix = ""
		interface = ""

		with open("Calculix1/Calculix1Mesh/all_pipe.msh", "r") as f:
			f.readline()
			for i in xrange(nsize1):
				line = f.readline()
				node = line.strip().split(",")
				if float(node[-2]) <= 0.01 or float(node[-2]) >= 7999.99:
					fix += node[0] + ", \n"
				if float(node[-2]) <= 6000.01 and float(node[-2]) >= 5999.99:
					interface += node[0] + ", \n"

		# fixed nodes
		with open("Calculix1/Calculix1Mesh/fix_pipe.nam", "w") as f:
			f.write("*NSET,NSET=Nfix \n")
			f.write(fix)

		# interface nodes
		with open("Calculix1/Calculix1Mesh/interface_pipe.nam", "w") as f:
			f.write("*NSET,NSET=Nsurface \n")
			f.write(interface)


def make_planes_part2():

		fix = ""
		interface = ""

		with open("Calculix2/Calculix2Mesh/all_pipe.msh", "r") as f:
			f.readline()
			for i in xrange(nsize2):
				line = f.readline()
				node = line.strip().split(",")
				if float(node[-2]) <= 0.01 or float(node[-2]) >= 7999.99:
					fix += node[0] + ", \n"
				if float(node[-2]) <= 6000.01 and float(node[-2]) >= 5999.99:
					interface += node[0] + ", \n"

		# fixed nodes
		with open("Calculix2/Calculix2Mesh/fix_pipe.nam", "w") as f:
			f.write("*NSET,NSET=Nfix \n")
			f.write(fix)

		# interface nodes
		with open("Calculix2/Calculix2Mesh/interface_pipe.nam", "w") as f:
			f.write("*NSET,NSET=Nsurface \n")
			f.write(interface)


#####################################################################################
#####################################################################################

#make_planes_mono()
make_planes_part1()
make_planes_part2()
