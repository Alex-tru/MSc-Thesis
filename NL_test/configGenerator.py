#!/usr/bin/python
# -*- coding: utf-8 -*-
from lxml import etree as ET
import numpy as np
import os

template = "precice-config.xml"  # template precice-config.xml used to generate series of configs
basepath = os.path.dirname(template)
basename = os.path.basename(template)
yaml1_path = "config1.yml"
yaml2_path = "config2.yml"

def change_option(ID, varied_variable, attrib, varied_values):
	
	elems = tree.findall('**/' + varied_variable) + tree.findall('**/*' + varied_variable)
	for value in varied_values:
		for elem in elems:
			elem.attrib[attrib] = str(value)# change values
		identifier = ID + "_" + '{0:.0e}'.format(value).replace('.','_') + "_"
		newname = identifier + basename
		tree.write(os.path.join(outfolder,newname))# write .xml

		# create new .yml configs
		new_yaml1 = identifier + "config1.yml"
		new_yaml2 = identifier + "config2.yml"
		with open(os.path.join(yamlfolder,new_yaml1), 'w') as f:
			for line in yaml1_template:
				f.writelines(line+'\n')
			f.writelines("precice-config-file: ./configs/"+newname)
		with open(os.path.join(yamlfolder,new_yaml2), 'w') as f:
			for line in yaml2_template:
				f.writelines(line+'\n')
			f.writelines("precice-config-file: ./configs/"+newname)

def change_2options( ID, varied_variable1, varied_variable2, attrib1, attrib2, varied_values1, varied_values2):
	elems1 = tree.findall('**/' + varied_variable1) + tree.findall('**/*' + varied_variable1)
	elems2 = tree.findall('**/' + varied_variable2) + tree.findall('**/*' + varied_variable2)
	for value1,value2 in zip(varied_values1, varied_values2):
		for elem in elems1:
			elem.attrib[attrib1] = str(value1)# change values
		for elem in elems2:
			elem.attrib[attrib2] = str(value2)# change values
		identifier = ID + '{0:.0e}'.format(value1).replace('.','_')+"_"
		newname = identifier + basename
		tree.write(os.path.join(outfolder,newname))# write .xml

		# create new .yml configs
		new_yaml1 = identifier + "config1.yml"
		new_yaml2 = identifier + "config2.yml"
		with open(os.path.join(yamlfolder,new_yaml1), 'w') as f:
			for line in yaml1_template:
				f.writelines(line+'\n')
			f.writelines("precice-config-file: ./configs/"+newname)
		with open(os.path.join(yamlfolder,new_yaml2), 'w') as f:
			for line in yaml2_template:
				f.writelines(line+'\n')
			f.writelines("precice-config-file: ./configs/"+newname)

def change_option_simple( varied_variable, attrib, value):

	elem = tree.findall('**/*'+varied_variable)[0]
	elem.attrib[attrib] = value

tree = ET.parse(template)

# read yaml templates, except for last line (the line with precice-config.xml path)
with open(yaml1_path, 'r') as f:
	yaml1_template = f.read().strip().split('\n')[:-1]
with open(yaml2_path, 'r') as f:
	yaml2_template = f.read().strip().split('\n')[:-1]


## create folders to write output to (xml and yaml files)
outfolder = 'configs'
yamlfolder = 'configs/yaml'
if os.path.exists(outfolder):
	if os.path.exists(yamlfolder):
		for file in os.listdir(yamlfolder):
			os.remove(os.path.join(yamlfolder,file))
		os.rmdir(yamlfolder)
	for file in os.listdir(outfolder):
		os.remove(os.path.join(outfolder,file))
	os.rmdir(outfolder)
os.mkdir(outfolder)
os.mkdir(yamlfolder)


## EXPERIMENTS - Uncomment the experiment you want to run

## iterate through list varied_values and create a precice-config.xml based on the given template with modified varied_variable, and also yaml files that reference that .xml

## vary limit of relative convergence measure
#varied_variable = "relative-convergence-measure"
#elems = tree.findall('**/'+varied_variable)

# case: convergence_measure

# SET EXPERIMENTAL PARAMETERS HERE (varied_values)
varied_values = 1./10.**np.arange( 1, 11 )
#varied_values2 = 1e-2 * np.arange(2,6)
#varied_values = np.concatenate([ varied_values1, varied_values2 ])
change_option( "conv_limit", "relative-convergence-measure", "limit", varied_values)

# case: QR1 filter limit
#varied_values = 1./10.**np.arange( 5, 15 )
##varied_values2 = [ 1e-6 ]
##varied_values = np.concatenate([ varied_values1, varied_values2 ])
#change_option_simple( "filter", "type", "QR1")
#change_option( "QR1_limit", "filter", "limit", varied_values )

# case: QR2 filter limit
#varied_values = [1e-4,1e-8,1e-12]
#varied_values = 1./10**np.arange( 1, 15 )
#varied_values2 = 1e-9*np.arange( 1, 10 )
#varied_values = np.concatenate([ varied_values1, varied_values2 ])
#change_option_simple( "filter", "type", "QR2")
#change_option( "QR2_limit", "filter", "limit", varied_values )

# case: initial relaxation
#varied_values = 1e-1*np.arange( 1, 10 )
##varied_values2 = 1e-9*np.arange( 1, 10 )
##varied_values = np.concatenate([ varied_values1, varied_values2 ])
#change_option( "init_relax", "initial-relaxation", "value", varied_values )

# case: timestep length
#varied_values1 = [2.5e-3, 4e-3, 1e-2, 2e-2, 5e-2]
#varied_values2 = [.5/x for x in varied_values1]# N_timesteps depends on timestep length
#change_2options( "timestep", "timestep-length", "max-timesteps", "value", "value", varied_values1, varied_values2 )








