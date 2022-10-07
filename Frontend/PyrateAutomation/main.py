#!/usr/bin/python3.10


################################################################################


import json
import subprocess

import init_json as ij
import runs_pyrate as rp
import fetch_results as fr
import cleaner as cl

from Asterix_libs.prints import *
from Asterix_libs import log
from datetime import datetime


################################################################################


subprocess.call("/bin/cp /mnt/DataShare/dirty.json inputs.json", shell = True)

with open("inputs.json", "r") as inp:
    js = json.load(inp)
    if len(js["ind_results"]) == 0:
        exit()

start = datetime.now()

log.log('BEGINING OF SANITIZING PROCESS.')

print()

# Initialize environment
info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Initializing environment.')
ij.init_res('Pyrate/san_results.json')

print()

info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Cleaning Pyrate folders.')
cl.clean_fold('Pyrate/Inputs')
log.log('Cleaned Pyrate/Inputs')
cl.clean_fold('Pyrate/Outputs')
log.log('Cleaned Pyrate/Outputs')


print()

info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Fetching inputs.')
lst = rp.getlist('inputs.json')
fls = rp.move(lst, 'Pyrate/Inputs')

print()

# Run Pyrate
info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Attempting sanitizing operations.')
rp.runs_(fls)

print()

# Get results
info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Fetching results')

ij.init_res('clean.json')

res = fr.get_stats('Pyrate/san_results.json')

with open('clean.json', 'r+') as outp:

    log.log('Opened clean.json')

    files = []

    for suc in res[0]:
        success(f'File {suc["FileName"]} was sanatized succesfully.')
        files.append(suc)

    js = json.load(outp)

    js['ind_results'] = files

    outp.seek(0)

    js = json.dumps(js, indent = 4)

    outp.write(js)

log.log('Closed clean.json')

print()

for fai in res[1]:
    fail(f'File {fai["FileName"]} couls not be sanitized.')

end = datetime.now()

elapsed = end-start

print()

info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Exhausted in ' + str(elapsed))
log.log('END OF SANITIZING PROCESS.')


################################################################################
