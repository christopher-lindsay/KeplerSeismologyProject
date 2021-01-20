#!/usr/bin/env python

import re
from os import system
import numpy as np

def MESA_runner(name, initial_z, logg, f, f0):
    '''
    Runs ms MESA model for a given name, mass, initial_y, initial_z, and alpha
    '''
    log_dir = 'log_directory = \'LOGS_ms_' + str(name) + '_overshoot_f=' + str(f) +'_log(g)=' + str(logg) + '\''
    model_name  = 'saved_model_name = \'' + str(name) + '_overshoot_f='+ str(f) + '_ZAMS.mod\''
    relax_z = 'new_Z = ' + str(initial_z)
    log_g_lower_limit = 'log_g_lower_limit = ' + str(logg)
    overshoot_f = 'overshoot_f = ' + str(f)
    overshoot_f0 = 'overshoot_f0 = ' + str(f0)

    # have MESA read the inlist_ms options
    with open('inlist', 'r') as f:
        inlist_main = f.read()
    inlist_main = re.sub(r"extra_star_job_inlist1_name = (.+)", "extra_star_job_inlist1_name = \'inlist_ms\'", inlist_main)
    inlist_main = re.sub(r"extra_controls_inlist1_name = (.+)", "extra_controls_inlist1_name = \'inlist_ms\'", inlist_main)
    with open('inlist' , 'w') as f:
        f.write(inlist_main)
    
    # make changes to inlist_ms
    with open('inlist_ms', 'r') as f:
        inlist_ms = f.read()
    inlist_ms = re.sub(r"log_directory = (.+)", log_dir, inlist_ms)
    inlist_ms = re.sub(r"saved_model_name = (.+)", model_name, inlist_ms)
    inlist_ms = re.sub(r"overshoot_f = (.+)", overshoot_f, inlist_ms)
    inlist_ms = re.sub(r"overshoot_f0 = (.+)", overshoot_f0, inlist_ms)
    inlist_ms = re.sub(r"new_Z = (.+)", relax_z, inlist_ms)
    inlist_ms = re.sub(r"log_g_lower_limit = (.+)", log_g_lower_limit, inlist_ms)
    
    with open('inlist_ms', 'w') as f:
        f.write(inlist_ms)

    system('./rn > /dev/null')
    print('succcessful run for MS '+ str(name) + str(overshoot_f))


MESA_runner('1.5solarmassTest',  0.03, 2.0, 0.0, 0.0)
MESA_runner('1.5solarmassTest',  0.03, 2.0, 0.2, 0.1)



'''
loggs = [3.0, 2.9, 2.8, 2.7, 2.6, 2.5, 2.4, 2.3, 2.2, 2.1, 2.0]
for g in loggs:
    MESA_runner('KIC2437933',  0.04121812, g, 0.2, 0.1)

for g in loggs:
    MESA_runner('KIC2437933',  0.04121812, g, 0.25, 0.125)
'''
