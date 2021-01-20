#!/usr/bin/env python

import re
from os import system
import numpy as np

def MESA_runner(name, mass, initial_y, alpha, f, f0):
    '''
    Runs pms MESA model for a given name, mass, initial_y, initial_z, and alpha
    '''
    initial_mass = 'initial_mass = ' + str(mass)
    initial_y = 'initial_y = ' + str(initial_y)
    mixing_length = 'mixing_length_alpha = ' + str(alpha)
    overshoot_f = 'overshoot_f = ' + str(f)
    overshoot_f0 = 'overshoot_f0 = ' + str(f0)
    log_dir = 'log_directory = \'LOGS_pms_' + str(name) + '_overshoot_f=' + str(f)  +'\''
    model_name  = 'save_model_filename = \'' + str(name) + '_overshoot_f='+ str(f) + '_ZAMS.mod\''
    
    # have MESA read the inlist_pms options
    with open('inlist', 'r') as f:
        inlist_main = f.read()
    inlist_main = re.sub(r"extra_star_job_inlist1_name = (.+)", "extra_star_job_inlist1_name = \'inlist_pms\'", inlist_main)
    inlist_main = re.sub(r"extra_controls_inlist1_name = (.+)", "extra_controls_inlist1_name = \'inlist_pms\'", inlist_main)
    with open('inlist' , 'w') as f:
        f.write(inlist_main)
    
    # make changes to inlist_pms
    with open('inlist_pms', 'r') as f:
        inlist_pms = f.read()
    inlist_pms = re.sub(r"initial_mass = (.+)", initial_mass, inlist_pms)
    inlist_pms = re.sub(r"initial_y = (.+)", initial_y, inlist_pms)
    inlist_pms = re.sub(r"mixing_length_alpha = (.+)", mixing_length, inlist_pms)
    inlist_pms = re.sub(r"overshoot_f = (.+)", overshoot_f, inlist_pms)
    inlist_pms = re.sub(r"overshoot_f0 = (.+)", overshoot_f0, inlist_pms)
    inlist_pms = re.sub(r"log_directory = (.+)", log_dir, inlist_pms)
    inlist_pms = re.sub(r"save_model_filename = (.+)", model_name, inlist_pms)
    with open('inlist_pms', 'w') as f:
        f.write(inlist_pms)

    system('./rn > /dev/null')
    print('succcessful run for PMS '+ str(name) + str(overshoot_f))




MESA_runner('1.5solarmassTest', 1.5, 0.3, 2.0, 0.0, 0.0)

MESA_runner('1.5solarmassTest', 1.5, 0.3, 2.0, 0.2, 0.1)

