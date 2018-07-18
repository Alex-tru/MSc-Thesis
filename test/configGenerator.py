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

tree = ET.parse(template)

# read yaml templates, remove line with precice-config.xml path
with open(yaml1_path, 'r') as f:
	yaml1_template = f.read().strip().split('\n')[:-1]
with open(yaml2_path, 'r') as f:
	yaml2_template = f.read().strip().split('\n')[:-1]


## make sure that template and configuration_file.py are consistent

#assert np.abs(float(tree.findall('**/max-time')[0].attrib['value']) - config.T_max) < 10**-10

## vary timestep length and generate multiple precice-config.xml from template

#varied_variable = "timestep-length"  # corresponding tag in precice-config.xml template
#elem = tree.findall('**/'+varied_variable)[0]  # find tag in template

## create list holding the values that you want to use for generating series of configs
#tau0 = config.tau0  # get smallest timestep length from python config
#N_experiments = config.n_tau
#varied_values = tau0 * .5**np.arange(0,N_experiments)  # create list of considered timestep sizes



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

## iterate through list varied_values and create a precice-config.xml based on the given template with modified varied_variable, and also yaml files that reference that .xml

## vary limit of relative convergence measure
#varied_variable = "relative-convergence-measure"
#elems = tree.findall('**/'+varied_variable)

#min_exp = 2
#N_experiments = 4
#varied_values1 = 1./10.**np.arange( min_exp, min_exp + N_experiments )
#varied_values2 = 1e-2 * np.arange(2,6)
#varied_values = np.concatenate([ varied_values1, varied_values2 ])

# case: convergence_measure
#for value in varied_values:
#    for elem in elems:
#        elem.attrib['limit'] = str(value)# change values
#    identifier = "conv_limit_"+'{0:.0e}'.format(value).replace('.','_')+"_"
#    newname = identifier + basename
#    tree.write(os.path.join(outfolder,newname))# write .xml

#	# create new .yml configs
#    new_yaml1 = identifier + "config1.yml"
#    new_yaml2 = identifier + "config2.yml"
#    with open(os.path.join(yamlfolder,new_yaml1), 'w') as f:
#        for line in yaml1_template:
#            f.writelines(line+'\n')
#        f.writelines("precice-config-file: ./configs/"+newname)
#    with open(os.path.join(yamlfolder,new_yaml2), 'w') as f:
#        for line in yaml2_template:
#            f.writelines(line+'\n')
#        f.writelines("precice-config-file: ./configs/"+newname)

## vary limit of QR1/QR2 filtering
#varied_variable = "filter"
#elem = tree.findall('**/*'+varied_variable)[0]

# case: QR1 filter limit
#varied_values = 1./10.**np.arange( 10, 13 )
#varied_values2 = [ 1e-6 ]
#varied_values = np.concatenate([ varied_values1, varied_values2 ])

#elem.attrib['type'] = "QR1"
#for value in varied_values:
#    elem.attrib['limit'] = str(value)# change values
#    identifier = "QR1_limit_"+'{0:.0e}'.format(value).replace('.','_')+"_"
#    newname = identifier + basename
#    tree.write(os.path.join(outfolder,newname))# write .xml

#	# create new .yml configs
#    new_yaml1 = identifier + "config1.yml"
#    new_yaml2 = identifier + "config2.yml"
#    with open(os.path.join(yamlfolder,new_yaml1), 'w') as f:
#        for line in yaml1_template:
#            f.writelines(line+'\n')
#        f.writelines("precice-config-file: ./configs/"+newname)
#    with open(os.path.join(yamlfolder,new_yaml2), 'w') as f:
#        for line in yaml2_template:
#            f.writelines(line+'\n')
#        f.writelines("precice-config-file: ./configs/"+newname)


# case: QR2 filter limit

##varied_values1 = 1e-3*np.arange( 1, 10 )
#varied_values1 = 1e-10*np.arange( 1, 10 )
#varied_values2 = 1e-9*np.arange( 1, 10 )
#varied_values = np.concatenate([ varied_values1, varied_values2 ])

#elem.attrib['type'] = "QR2"
#for value in varied_values:
#    elem.attrib['limit'] = str(value)# change values
#    identifier = "QR2_limit_"+'{0:.0e}'.format(value).replace('.','_')+"_"
#    newname = identifier + basename
#    tree.write(os.path.join(outfolder,newname))# write .xml

#	# create new .yml configs
#    new_yaml1 = identifier + "config1.yml"
#    new_yaml2 = identifier + "config2.yml"
#    with open(os.path.join(yamlfolder,new_yaml1), 'w') as f:
#        for line in yaml1_template:
#            f.writelines(line+'\n')
#        f.writelines("precice-config-file: ./configs/"+newname)
#    with open(os.path.join(yamlfolder,new_yaml2), 'w') as f:
#        for line in yaml2_template:
#            f.writelines(line+'\n')
#        f.writelines("precice-config-file: ./configs/"+newname)


# case: QR2 filter limit

## vary initial relaxation value
varied_variable = "initial-relaxation"
elem = tree.findall('**/*'+varied_variable)[0]

varied_values = 1e-1*np.arange( 1, 10 )
#varied_values2 = 1e-9*np.arange( 1, 10 )
#varied_values = np.concatenate([ varied_values1, varied_values2 ])

for value in varied_values:
    elem.attrib['value'] = str(value)# change values
    identifier = "init_relax_"+'{0:.0e}'.format(value).replace('.','_')+"_"
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


