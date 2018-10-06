#!/bin/bash

# Restart a calculix simulation changing using results from a previous one.
# This script handles output and input file renaming.

time_and_date=$(date +%m-%d_%H.%M.%S)

(time ccx_preCICE -i pipe_monoNL) 2> run_times_$time_and_date.txt 
cp pipe_monoNL.rout pipe_monoNL_restart.rin
cp pipe_monoNL.rout /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoNL_restart_$time_and_date.rin
rm pipe_monoNL.rout

cp pipe_monoNL.dat /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoNL_$time_and_date.dat
cp pipe_monoNL.inp /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoNL$time_and_date.inp
cp pipe_monoNL.frd /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoNL_$time_and_date.frd
cp pipe_monoNL.cvg /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoNL_$time_and_date.cvg
cp pipe_monoNL.sta /media/alextru/Maxtor/Thesis/L-NL_test/Results/pipe_monoNL_$time_and_date.sta
rm pipe_monoNL.dat
rm pipe_monoNL.frd
rm pipe_monoNL.cvg
rm pipe_monoNL.sta
