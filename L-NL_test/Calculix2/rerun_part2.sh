#!/bin/bash

# Restart a calculix simulation changing using results from a previous one.
# This script handles output and input file renaming, and stores results.

time_and_date=$(date +%m-%d_%H.%M.%S)

(time ccx_preCICE -i pipe2_restart -precice-participant Calculix2) 2> run_times_$time_and_date.txt 
cp pipe2_restart.rout pipe2_restart.rin
cp pipe2_restart.rout /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe2_restart_$time_and_date.rin 
rm pipe2_restart.rout

cp pipe2_restart.dat /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe2_restart_$time_and_date.dat
cp pipe2.inp /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe2_$time_and_date.inp
cp pipe2_restart.frd /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe2_restart_$time_and_date.frd
cp pipe2_restart.cvg /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe2_restart_$time_and_date.cvg
cp pipe2_restart.sta /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe2_restart_$time_and_date.sta
cp iterations-Calculix2.txt /media/alextru/Maxtor/Thesis/L-NL_test/Results/iterations-Calculix2_$time_and_date.txt
cp convergence-Calculix2.txt /media/alextru/Maxtor/Thesis/L-NL_test/Results/convergence-Calculix2_$time_and_date.txt
rm pipe2_restart.dat
rm pipe2_restart.frd
rm pipe2_restart.cvg
rm pipe2_restart.sta
