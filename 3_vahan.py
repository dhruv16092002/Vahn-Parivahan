from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
import shutil

chrome_options = webdriver.ChromeOptions()

'''
Cahge this path
'''
# Change this path as per your project directory
# download_directory = 'C:\\Users\\Admin\\Downloads\\vahan'
download_directory = 'D:\\vahan2024\\Downloads'


prefs = {"download.default_directory": download_directory,}
chrome_options.add_experimental_option("prefs", prefs)


driver = webdriver.Chrome(options=chrome_options)
driver.minimize_window()
driver.get("https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml")


# Change this download path as per above chagned and dont change reportTable.xlsx
dowloaded_file = str(f"{download_directory}/reportTable.xlsx").replace("\\","/")


wait = WebDriverWait(driver, 20)

with open('state.json','r') as st_file:
    state_list = json.load(st_file)['state']

with open('rto_list.json', 'r') as rto_file:
    rto_list = json.load(rto_file)

"""
Change these filters according to you requirements.
"""
# Change filter as per your requirement.
vehicle_category = 'MOTOR CAR'

first_time = False
# loop for y axis
list_yAxis = ['Maker']
for y_filter in list_yAxis:
    yAxis_dropdown_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div[1]/div/div[3]/span')))
    time.sleep(1)
    yAxis_dropdown_button.click()
    yAxis_option = wait.until(EC.visibility_of_element_located((By.XPATH, f"//li[text()='{y_filter}']")))
    time.sleep(1)
    yAxis_option.click()
    
    # loop for year list
    time.sleep(1)
    # Change as per your requirement
    year_filter_list = ['2023','2024'] 
    for year in year_filter_list:
        if os.path.exists(dowloaded_file):
            os.remove(dowloaded_file)
        select_year_dropdown_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/div[3]/span')))
        time.sleep(1)
        select_year_dropdown_button.click()
        select_year_dropdown_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[text()='{year}']"))) 
        select_year_dropdown_option.click()
        time.sleep(1) 

        # Loop For x filter
        x_axis_filters = ['Fuel']
        for x_filter in x_axis_filters:
            time.sleep(2)
            xAxis_dropdown_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="xaxisVar"]/div[3]/span')))
            time.sleep(1)
            xAxis_dropdown_button.click()
            time.sleep(1) 
            if x_filter == 'Fuel':
                x_filter_test = '//*[@id=\"xaxisVar_3\"]'
                xAxis_dropdown_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"{x_filter_test}"))) 
            else:
                xAxis_dropdown_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[text()='{x_filter}']"))) 
            time.sleep(1)
            xAxis_dropdown_option.click()
            time.sleep(1)

            # Loop For state filter
            for state in state_list:
                with open('rto_completed.json', 'r') as f:
                    completed_json = json.load(f)
                if state not in completed_json['completed']:
                    time.sleep(2)
                    state_select_drop_down = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[2]/div/div/div[1]/div[2]/div[3]/div/div[3]/span')))
                    time.sleep(1)
                    state_select_drop_down.click()
                    
                    send_text = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[text()='{state}']")))
                    time.sleep(1)
                    send_text.click()
                    
                    # loop for rto list
                    for rto in rto_list[state]:
                        with open('rto_completed.json', 'r') as f:
                            completed_rto_json = json.load(f)
                        if rto not in completed_rto_json['completed'] :
                            time.sleep(4)
                            rto_select_drop_down = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[2]/div/div/div[1]/div[2]/div[4]/div/div[3]/span')))
                            time.sleep(1)
                            rto_select_drop_down.click()
                            time.sleep(2)
                            rto_text = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[text()='{rto}']")))
                            time.sleep(2)
                            rto_text.click()
                            time.sleep(2)
                            
                            # Refresh button 
                            refresh_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[2]/div/div/div[1]/div[3]/div[3]/div/button')))
                            time.sleep(1)
                            refresh_button.click()
                            time.sleep(2)

                            if vehicle_category == 'TWO WHEELER(NT)':
                                vehilcle_filter_variable = '//*[@id="VhCatg"]/tbody/tr[2]/td/div/div[2]/span'
                            if vehicle_category == 'MOTOR CAR':
                                vehilcle_filter_variable = '//*[@id="VhClass"]/tbody/tr[7]/td/div/div[2]'

                            if first_time == False:
                                # Main filter opetion
                                time.sleep(1)
                                main_filter = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[2]/div/div/div[3]/div/div[3]/div')))
                                time.sleep(1)
                                main_filter.click()
                                time.sleep(2)
                                first_time = True

                            #vehicle category select from main filter
                            vehicle_category_filter = wait.until(EC.element_to_be_clickable((By.XPATH, f'{vehilcle_filter_variable}')))
                            vehicle_category_filter.click()


                            months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
                            if year == '2024':
                                months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP']
                            for month in months:
                                path = os.path.join('vahan/raw',year,state,rto,x_filter,vehicle_category,month)
                                file_path = os.path.join(path,'reportTable.xlsx')
                                if os.path.exists(file_path):
                                    print("exists")
                                else:
                                    time.sleep(1)
                                    month_filter = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="groupingTable:selectMonth"]/div[3]/span')))
                                    month_filter.click()
                                    time.sleep(2)
                                    month_text = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[text()='{month}']")))
                                    month_text.click()
                                    # Refresh Button

                                    time.sleep(2)
                                    refresh_filter = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="filterLayout"]/div[1]/span')))
                                    refresh_filter.click()
                                    # # download button
                                    time.sleep(2)
                                    # download_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vchgroupTable:xls"]')))
                                    download_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[2]/div/div/div[3]/div/div[2]/div/div/div[1]/div[1]/a')))
                                    time.sleep(1)
                                    download_button.click()
                                    time.sleep(2)
                                    os.makedirs(path, exist_ok=True)
                                    shutil.move(dowloaded_file, path)  
                            with open('rto_completed.json', 'r') as f:
                                completed_rto = json.load(f)

                            # Append the state
                            array_rto_completed = completed_rto.get('completed', [])
                            array_rto_completed.append(rto)
                            completed_rto['completed'] = array_rto_completed

                            # Write back to the file
                            with open('rto_completed.json', 'w') as fc:
                                json.dump(completed_rto, fc, indent=4) 
                    # if not os.path.exists('state_completed.json'):
                    #     with open('state_completed.json', 'w') as fc:
                    #         json.dump({"completed": []}, fc, indent=4)
                    with open('state_completed.json', 'r') as f:
                        completed_json = json.load(f)

                    # Append the state
                    array_completed = completed_json.get('completed', [])
                    array_completed.append(state)
                    completed_json['completed'] = array_completed

                    # Write back to the file
                    with open('state_completed.json', 'w') as fc:
                        json.dump(completed_json, fc, indent=4)
                    
driver.quit()