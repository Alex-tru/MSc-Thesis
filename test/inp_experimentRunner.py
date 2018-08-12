#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Runs experiments changing parameters of the calculix input files.
"""

import subprocess
import os
import time
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("participant", choices=["Calculix1","Calculix2"])
args = parser.parse_args()

def run_Calculix1():
	subprocess.call([ "ccx_preCICE","-i","Calculix1/beam1","-precice-participant","Calculix1","-precice-config","Calculix1/config_inp_experiments.yml" ])


def run_Calculix2():
	subprocess.call([ "ccx_preCICE","-i","Calculix2/beam2","-precice-participant","Calculix2","-precice-config","Calculix2/config_inp_experiments.yml" ])

def run_CalculixMono():
	subprocess.call([ "ccx_preCICE","-i","CalculixMono/beam_mono" ])

def changeLine( path, card, newline ):
	"Changes a line in a calculix input file."
	with open( path, "r" ) as old:
		with open ( path + "_temp", "w" ) as new:

			line = old.readline()
			while line:
				new.write( line )

				# look for the card to modify
				if card in line:
					old.readline()
					new.write( newline + '\n' )
				line = old.readline()
	os.rename( path + "_temp", path)

def reset_inp():
	if args.participant == "Calculix1":
		changeLine( "Calculix1/beam1.inp", "DENSITY", " 7.8E-09" )
		changeLine( "Calculix1/beam1.inp", "ELASTIC", " 210000.0,        .3" )
	elif args.participant == "Calculix2":
		changeLine( "Calculix2/beam2.inp", "DENSITY", " 7.8E-09" )
		changeLine( "Calculix2/beam2.inp", "ELASTIC", " 210000.0,        .3" )


# file names to be changed after every simulation
fnames_cwd = ["convergence-Calculix2.txt","iterations-Calculix1.txt","iterations-Calculix2.txt"]
fnames_subdir1 = ["Calculix1/beam1.dat","Calculix1/beam1.sta","Calculix1/beam1.cvg","Calculix1/beam1.frd"]
fnames_subdir2 = ["Calculix2/beam2.dat","Calculix2/beam2.sta","Calculix2/beam2.cvg","Calculix2/beam2.frd"]

reset_inp()

## EXPERIMENTS - Uncomment the experiment you want to run

## density experiments
# SET EXPERIMENTAL PARAMETERS HERE (varied_values)
#densities = 7.8 / 10.**np.arange(22,26)
#for rho in densities:

#	if args.participant == "Calculix1":
#		changeLine( "Calculix1/beam1.inp", "DENSITY", '{:0.1E}'.format(rho) )
#	elif args.participant == "Calculix2":
#		changeLine( "Calculix2/beam2.inp", "DENSITY", '{:0.1E}'.format(rho) )

#	if args.participant == "Calculix1":
#		run_Calculix1()
#		for fname in fnames_subdir1:
#			while True:
#				print fname
#				try:
#					os.rename( fname, "conv_studies/" + '{:0.1E}'.format(rho) + "_" + fname[10:] )
#				except OSError:
#					continue
#				break
#	else:
#		run_Calculix2()

#		# rename and move results files so they're not overwritten
#		for fname in fnames_cwd:
#			while True:
#				print fname
#				try:
#					os.rename( fname, "conv_studies/" + '{:0.1E}'.format(rho) + "_" + fname )
#				except OSError:
#					continue
#				break
#		for fname in fnames_subdir2:
#			while True:
#				print fname
#				try:
#					os.rename( fname, "conv_studies/" + '{:0.1E}'.format(rho) + "_" + fname[10:] )
#				except OSError:
#					continue
#				break

reset_inp()

# Young modulus experiments
# SET EXPERIMENTAL PARAMETERS HERE (varied_values)
Young_moduli = 2.1 * 10.**np.arange(8,15)
for E in Young_moduli:

	if args.participant == "Calculix1":
		changeLine( "Calculix1/beam1.inp", "ELASTIC", str(E) + ",   .3" )
	elif args.participant == "Calculix2":
		changeLine( "Calculix2/beam2.inp", "ELASTIC", str(E) + ",   .3" )

	if args.participant == "Calculix1":
		run_Calculix1()
		for fname in fnames_subdir1:
			while True:
				print fname
				try:
					os.rename( fname, "conv_studies/" + str(E) + "_" + fname[10:] )
				except OSError:
					continue
				break
	else:
		run_Calculix2()

		# rename and move results files so they're not overwritten
		for fname in fnames_cwd:
			while True:
				print fname
				try:
					os.rename( fname, "conv_studies/" + str(E) + "_" + fname )
				except OSError:
					continue
				break
		for fname in fnames_subdir2:
			while True:
				print fname
				try:
					os.rename( fname, "conv_studies/" + str(E) + "_" + fname[10:] )
				except OSError:
					continue
				break
reset_inp()

## Poisson coefficient experiments
## SET EXPERIMENTAL PARAMETERS HERE (varied_values)
##Poisson_coefficients = 0.1 * np.arange(1,5)
##for nu in Poisson_coefficients:

#	if args.participant == "Calculix1":
#		changeLine( "Calculix1/beam1.inp", "ELASTIC", "210000.0,   " + str(nu) )
#	elif args.participant == "Calculix2":
#		changeLine( "Calculix2/beam2.inp", "ELASTIC", "210000.0,   " + str(nu) )

#	if args.participant == "Calculix1":
#		run_Calculix1()
#		for fname in fnames_subdir1:
#			while True:
#				print fname
#				try:
#					os.rename( fname, "conv_studies/" + str(nu) + "_" + fname[10:] )
#				except OSError:
#					continue
#				break
#	else:
#		run_Calculix2()

#		# rename and move results files so they're not overwritten
#		for fname in fnames_cwd:
#			while True:
#				print fname
#				try:
#					os.rename( fname, "conv_studies/" + str(nu) + "_" + fname )
#				except OSError:
#					continue
#				break
#		for fname in fnames_subdir2:
#			while True:
#				print fname
#				try:
#					os.rename( fname, "conv_studies/" + str(nu) + "_" + fname[10:] )
#				except OSError:
#					continue
#				break


