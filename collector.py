# Collects serial data in the format 'float,float,float.
# Collection is run for 'COLLECTION_TIME_S' seconds and
# saved to a CSV file. Successive runs are appended to
# the previous run.

# Usage: script.py <movement_name>

import serial
import pandas as pd
import os
import time
from argparse import ArgumentParser

SAVE_FILE = 'imu.csv'
COLLECTION_TIME_S = 30

parser = ArgumentParser()
parser.add_argument('movement')
args = parser.parse_args()

new_df = pd.DataFrame(columns=['x','y','z','movement_name'])

ser = serial.Serial('/dev/ttyS1', 9600)
start_time = time.time()
while time.time() - start_time < COLLECTION_TIME_S:
   row_bytes=ser.readline()
   row = row_bytes.decode("utf-8")
   # remove nl
   row = row.strip()
   components = row.split(',')

   # start processing from a whole line.
   # 3 elements are expected.
   if len(components) != 3:
      continue

   new_df = new_df.append({'x':components[0], 'y':components[1], 
                  'z':components[2], 'movement_name':args.movement}, ignore_index=True)

if os.path.exists(SAVE_FILE):
   old_df = pd.read_csv(SAVE_FILE)
   new_df = old_df.append(new_df)

print(new_df)
new_df.to_csv(SAVE_FILE, index=False)