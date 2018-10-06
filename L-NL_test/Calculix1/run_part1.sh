#!/bin/bash

# Restart a calculix simulation changing using results from a previous one.
# This script handles output and input file renaming, and stores results.

time_and_date=$(date +%m-%d_%H.%M.%S)

(time ccx_preCICE -i pipe1 -precice-participant Calculix1) 2> run_times_$time_and_date.txt 
cp pipe1.rout pipe1_restart.rin
cp pipe1.rout /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe1_restart_$time_and_date.rin 
rm pipe1.rout

cp pipe1.dat /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe1_$time_and_date.dat
cp pipe1.inp /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe1_$time_and_date.inp
cp pipe1.frd /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe1_$time_and_date.frd
cp pipe1.cvg /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe1_$time_and_date.cvg
cp pipe1.sta /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe1_$time_and_date.sta
cp ../precice-config.xml  /media/alextru/Maxtor/Thesis/L-NL_test/Results/precice-config_$time_and_date.xml
rm pipe1.dat
rm pipe1.frd
rm pipe1.cvg
rm pipe1.sta
