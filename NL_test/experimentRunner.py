#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import multiprocessing
import os
import time

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("participant", choices=["Calculix1","Calculix2"])
args = parser.parse_args()

def run_Calculix1(config):
	subprocess.call([ "ccx_preCICE","-i","Calculix1/beam1","-precice-participant","Calculix1","-precice-config",config ])


def run_Calculix2(config):
	subprocess.call([ "ccx_preCICE","-i","Calculix2/beam2","-precice-participant","Calculix2","-precice-config",config ])


configfolder = os.path.join(os.getcwd(),'configs/yaml')

# file names to be changed after every simulation
fnames_cwd = ["convergence-Calculix2.txt","iterations-Calculix1.txt","iterations-Calculix2.txt"]
fnames_subdir1 = ["Calculix1/beam1.dat","Calculix1/beam1.sta","Calculix1/beam1.cvg","Calculix1/beam1.frd"]
fnames_subdir2 = ["Calculix2/beam2.dat","Calculix2/beam2.sta","Calculix2/beam2.cvg","Calculix2/beam2.frd"]

# prepare lists for yaml files
full_yaml_list = os.listdir(configfolder)
full_yaml_list.sort()
if args.participant == "Calculix1":
	yaml_list = full_yaml_list[::2]
else: yaml_list = full_yaml_list[1::2]

for yaml in yaml_list:
	print "processing " + yaml

	yamlpath = os.path.join(configfolder, yaml)

	# run calculix in command-line with yamlpath
	if args.participant == "Calculix1":
		run_Calculix1(yamlpath)
		for fname in fnames_subdir1:
			while True:
				try:
					os.rename(fname,"conv_studies/"+yaml[:-12]+"_"+fname[10:])
				except OSError:
					continue
				break
	else: 
		run_Calculix2(yamlpath)
		# rename and move results files so they're not overwritten
		for fname in fnames_cwd:
			while True:
				try:
					os.rename(fname,"conv_studies/"+yaml[:-12]+"_"+fname)
				except OSError:
					continue
				break
		for fname in fnames_subdir2:
			while True:
				try:
					os.rename(fname,"conv_studies/"+yaml[:-12]+"_"+fname[10:])
				except OSError:
					continue
				break
