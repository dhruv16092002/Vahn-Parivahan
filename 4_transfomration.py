import pandas as pd # type: ignore
import json
import os

with open('state.json', 'r') as state_file:
    state_list = json.load(state_file)['state']

with open('rto_list.json') as rto_file:
    rto_list = json.load(rto_file)

# Change the sub_folder path according to your download folder path
sub_folder = 'D:/vahan2024/vahan/raw'

"""
Change these filters according to you requirements.
"""
vehicle_class = "MOTOR CAR"
year = '2024'
x_filter = 'Fuel'
months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

for state in state_list:
    for rto in rto_list[state]:
        for month in months:
            if os.path.exists(os.path.join(sub_folder,year,state,rto,x_filter,vehicle_class,month)):
                file_path = os.path.join(sub_folder,year,state,rto,x_filter,vehicle_class,month,'reportTable.xlsx').replace('\\','/')
                print(file_path)
                df = pd.read_excel(file_path)[2:]
                if len(df) > 3:
                    if int(len(df.iloc[0])) > 1 :
                        df.columns = df.iloc[0]
                        df = df[1:]
                        df = df.reset_index(drop=True)
                        df['State'] = state
                        df['rto'] = rto
                        df['Year'] = year
                        df['Month'] = month
                        df['Vehicle Category'] = vehicle_class
                        maker_fuel_df = df
                        maker_fuel_df.columns = ['sr','Maker',"CNG ONLY","DIESEL","DIESEL/HYBRID","DI-METHYL ETHER","DUAL DIESEL/BIO CNG","DUAL DIESEL/CNG","DUAL DIESEL/LNG","ELECTRIC(BOV)","ETHANOL","FUEL CELL HYDROGEN","LNG","LPG ONLY","METHANOL","NOT APPLICABLE","PETROL","PETROL/CNG","PETROL/ETHANOL","PETROL/HYBRID","PETROL/LPG","PETROL/METHANOL","PLUG-IN HYBRID EV","PURE EV","SOLAR","STRONG HYBRID EV",'Sale','State','rto','Year','Month','Vehicle Category']

                        df_melted = pd.melt(maker_fuel_df, 
                                id_vars=['Maker'], 
                                value_vars=["CNG ONLY", "DIESEL", "DIESEL/HYBRID", "DI-METHYL ETHER",
                                            "DUAL DIESEL/BIO CNG", "DUAL DIESEL/CNG", "DUAL DIESEL/LNG",
                                            "ELECTRIC(BOV)", "ETHANOL", "FUEL CELL HYDROGEN", "LNG", "LPG ONLY",
                                            "METHANOL", "NOT APPLICABLE", "PETROL", "PETROL/CNG",
                                            "PETROL/ETHANOL", "PETROL/HYBRID", "PETROL/LPG", "PETROL/METHANOL",
                                            "PLUG-IN HYBRID EV", "PURE EV", "SOLAR", "STRONG HYBRID EV"],
                                var_name='Fuel Type', 
                                value_name='Sales')
                        main_df = df_melted.merge(maker_fuel_df,how='left',on='Maker')
                        main_df = main_df[['Maker', 'Fuel Type', 'Sales','Vehicle Category', 'State', 'rto', 'Year', 'Month']]
                        main_df['RTO Code'] = main_df['rto'].str.extract(r'-\s*([A-Z]+\d+)\s*\(')
                        main_df['RTO Name'] = main_df['rto'].str.extract(r'(.+?)\s*-\s*[A-Z]{1,2}\d{1,3}')
                        main_df = main_df[['Maker', 'Fuel Type','Vehicle Category','State','RTO Name','RTO Code','Year', 'Month', 'Sales']]
                        save_file_path = os.path.join(sub_folder,year,state,rto,x_filter,vehicle_class,month,'result.csv')
                        print(save_file_path)
                        main_df.to_csv(save_file_path, header=True, index=False)

