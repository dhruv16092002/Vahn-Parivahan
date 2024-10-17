import pandas as pd
import json
import os

# Load the state list and RTO list from JSON files
with open('state.json', 'r') as state_file:
    state_list = json.load(state_file)['state']

with open('rto_list.json') as rto_file:
    rto_list = json.load(rto_file)

# Set folder paths and filters
sub_folder = 'D:/vahan2024/vahan/raw'


"""
Change these filters according to you requirements.
"""
x_filter = 'Fuel'
vehicle_class = "MOTOR CAR"
year = '2024'
months = ['JAN','FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

for state in state_list:
    for rto in rto_list[state]:
        for month in months:
            folder_path = os.path.join(sub_folder, year, state, rto, x_filter, vehicle_class, month)
            if os.path.exists(folder_path):
                file_path = os.path.join(folder_path, 'result.csv').replace('\\', '/')
                if os.path.isfile(file_path):
                    df = pd.read_csv(file_path).iloc[2:] 
                    if not os.path.exists(vehicle_class+'.csv'):
                        df.to_csv(vehicle_class+'.csv',index=False, header=True)
                    else:
                        df.to_csv(vehicle_class+'.csv',index=False,mode='a',header=False)

print("All file Merged")