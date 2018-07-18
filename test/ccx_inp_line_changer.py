#!usr/bin/python

import os
import argparse

"Changes a line in the calculix input files of Calculix1, Calculix2 and CalculixMono."

parser = argparse.ArgumentParser()
parser.add_argument( "card", help = "Card with the parameter/s to change. (e.g. DENSITY)" )
parser.add_argument( "newline", help = "New line, as it should be written in the .inp file in the card." )
args = parser.parse_args()

def changeLine( path ):

	with open( path, "r" ) as old:
		with open ( path + "_temp", "w" ) as new:

			line = old.readline()
			while line:
				new.write( line )

				# look for the card to modify
				if args.card in line:
					old.readline()
					new.write( args.newline + '\n' )
				line = old.readline()
	os.rename( path + "_temp", path)

changeLine("CalculixMono/beam_mono.inp")

