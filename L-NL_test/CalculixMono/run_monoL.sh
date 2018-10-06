#!/bin/bash

# Restart a calculix simulation changing using results from a previous one.
# This script handles output and input file renaming.

time_and_date=$(date +%m-%d_%H.%M.%S)

(time ccx_preCICE -i pipe_monoL) 2> run_times_$time_and_date.txt 
cp pipe_monoL.rout pipe_monoL_restart.rin
cp pipe_monoL.rout /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoL_restart_$time_and_date.rin
rm pipe_monoL.rout

cp pipe_monoL.dat /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoL_$time_and_date.dat
cp pipe_monoL.inp /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoL$time_and_date.inp
cp pipe_monoL.frd /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoL_$time_and_date.frd
cp pipe_monoL.cvg /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoL_$time_and_date.cvg
cp pipe_monoL.sta /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoL_$time_and_date.sta
rm pipe_monoL.dat
rm pipe_monoL.frd
rm pipe_monoL.cvg
rm pipe_monoL.sta
