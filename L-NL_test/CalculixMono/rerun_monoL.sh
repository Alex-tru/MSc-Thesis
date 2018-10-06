#!/bin/bash

# Restart a calculix simulation changing using results from a previous one.
# This script handles output and input file renaming, and stores results.

time_and_date=$(date +%m-%d_%H.%M.%S)

(time ccx_preCICE -i pipe_monoL_restart) 2> run_times_$time_and_date.txt 
cp pipe_monoL_restart.rout pipe_monoL_restart.rin
cp pipe_monoL_restart.rout /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoL_restart_$time_and_date.rin
rm pipe_monoL_restart.rout

cp pipe_monoL_restart.dat /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoL_restart_$time_and_date.dat
cp pipe_monoL.inp /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoL$time_and_date.inp
cp pipe_monoL_restart.frd /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoL_restart_$time_and_date.frd
cp pipe_monoL_restart.cvg /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoL_restart_$time_and_date.cvg
cp pipe_monoL_restart.sta /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoL_restart_$time_and_date.sta
rm pipe_monoL_restart.dat
rm pipe_monoL_restart.frd
rm pipe_monoL_restart.cvg
rm pipe_monoL_restart.sta
