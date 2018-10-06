#!/bin/bash

# Restart a calculix simulation changing using results from a previous one.
# This script handles output and input file renaming, and stores results.

time_and_date=$(date +%m-%d_%H.%M.%S)

(time ccx_preCICE -i pipe1_restart -precice-participant Calculix1) 2> run_times_$time_and_date.txt 
cp pipe1_restart.rout pipe1_restart.rin
cp pipe1_restart.rout /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe1_restart_$time_and_date.rin 
rm pipe1_restart.rout

cp pipe1_restart.dat /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe1_restart_$time_and_date.dat
cp pipe1.inp /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe1_$time_and_date.inp
cp pipe1_restart.frd /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe1_restart_$time_and_date.frd
cp pipe1_restart.cvg /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe1_restart_$time_and_date.cvg
cp pipe1_restart.sta /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe1_restart_$time_and_date.sta
rm pipe1_restart.dat
rm pipe1_restart.frd
rm pipe1_restart.cvg
rm pipe1_restart.sta
