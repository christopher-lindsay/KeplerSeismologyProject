#!/usr/bin/env python

import re
from os import system
import subprocess
import numpy as np
import pandas as pd

def last_gyre_file(log_dir):
    # find the last gyre profile from each run
    
    move_index = 'mv ' + str(log_dir) + '/profiles.index ' + log_dir + '.profiles.index'
    system(move_index)
    move_history = 'mv ' + str(log_dir) + '/history.data ' + log_dir + '.history.data'
    system(move_history)
    move_pgstar = 'mv ' + str(log_dir) + '/pgstar.dat ' + log_dir + '.pgstar.dat'
    system(move_pgstar)
    
    last_profile = subprocess.check_output( 'ls -t ' + str(log_dir) + ' | head -1', shell=True)
    last_prof = last_profile.split("\n")[0]
    
    return str(last_prof)

def scaling_params(KIC, M, logg, f):
    nu_max_solar = 3090
    delta_nu_solar = 135
    T_eff_solar = 5776
    
    log_dir = 'LOGS_ms_' + str(KIC) + '_overshoot_f=' + str(f) + '_log(g)=' + str(logg)

    history_df = pd.read_csv(str(log_dir) + '.history.data', skiprows=5, delim_whitespace=True)
    last_val = history_df.iloc[-1]
    
    logR = float(last_val['log_R'])
    R = 10**logR
    logTeff = float(last_val['log_Teff'])
    T = 10**logTeff
    print(R)
    print(T)
    
    nu_max = ( nu_max_solar * M * (np.power(R,-2)) * np.power(T_eff_solar/T, 0.5) )
    delta_nu = delta_nu_solar * np.sqrt(M / np.power(R,3))
    
    print(nu_max, delta_nu)
    freq_max = nu_max + 10*delta_nu
    
    freq_min = nu_max - 10*delta_nu
    if freq_min < 0:
        freq_min = 1
    else: freq_min = freq_min
    
    return freq_min, freq_max
    
def run_gyre(filename, freq_min, freq_max):
    with open('gyre.in', 'r') as f:
        gyre = f.read()
    outfile = str(filename) + '.out'
    new_output = 'summary_file = \'GYRE_OUTPUTS/' + outfile + '\''
    new_model = 'file = \'' + str(filename) + '\''
    new_freq_min = 'freq_min = ' + str(freq_min)
    new_freq_max = 'freq_max = ' + str(freq_max)
    
    gyre = re.sub(r"file = (.+)", new_model, gyre)
    gyre = re.sub(r"summary_file = (.+)", new_output, gyre)
    gyre = re.sub(r"freq_min = (.+)", new_freq_min, gyre)
    gyre = re.sub(r"freq_max = (.+)", new_freq_max, gyre)
    with open('gyre.in', 'w') as f:
        f.write(gyre)
    command = '$GYRE_DIR/bin/gyre gyre.in'
    system(command)
    print('successful run for ' + str(filename))


def get_gyre_prof(KIC, M, logg, f):
    '''
    go into the given directory and copy the desired gyre file into the work directory then run gyre to get modes
    '''
    log_dir = 'LOGS_ms_' + str(KIC) + '_overshoot_f=' + str(f) + '_log\(g\)=' + str(logg)
    name = str(KIC) + '_overshoot_f=' + str(f) + '_log\(g\)=' + str(logg)
    filename = str(name) + ".GYRE"
    
    last_prof = last_gyre_file(log_dir)
    print(last_prof)
    command = 'cp ' + str(log_dir) + '/' + str(last_prof) + ' ' + str(filename)
    system(command)
    
    freq_min, freq_max = scaling_params(KIC, M, logg, f)
    print(freq_min, freq_max)
    
    filename_g = str(KIC) + '_overshoot_f=' + str(f) + '_log(g)=' + str(logg) + ".GYRE"
    run_gyre(filename_g, freq_min, freq_max)


loggs = [3.0, 2.9, 2.8, 2.7, 2.6, 2.5, 2.4, 2.3, 2.2, 2.1, 2.0]
fs = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25]

for f in fs:
    for logg in loggs:
        get_gyre_prof('KIC2437933', 1.23246195, logg, f)

