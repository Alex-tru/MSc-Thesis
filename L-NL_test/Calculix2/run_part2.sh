#!/bin/bash

# Restart a calculix simulation changing using results from a previous one.
# This script handles output and input file renaming, and stores results.

time_and_date=$(date +%m-%d_%H.%M.%S)

(time ccx_preCICE -i pipe2 -precice-participant Calculix2) 2> run_times_$time_and_date.txt 
cp pipe2.rout pipe2_restart.rin
cp pipe2.rout /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe2_restart_$time_and_date.rin 
rm pipe2.rout

cp pipe2.dat /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe2_$time_and_date.dat
cp pipe2.inp /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe2$time_and_date.inp
cp pipe2.frd /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe2_$time_and_date.frd
cp pipe2.cvg /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe2_$time_and_date.cvg
cp pipe2.sta /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe2_$time_and_date.sta
cp iterations-Calculix2.txt /media/alextru/Maxtor/Thesis/L-NL_test/Results/iterations-Calculix2_$time_and_date.txt
cp convergence-Calculix2.txt /media/alextru/Maxtor/Thesis/L-NL_test/Results/convergence-Calculix2_$time_and_date.txt
rm pipe2.dat
rm pipe2.frd
rm pipe2.cvg
rm pipe2.sta
