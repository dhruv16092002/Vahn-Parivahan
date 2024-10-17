from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import time
import json

# Load the state list from 'state.json'
with open('state.json', 'r') as file:
    state_list = json.load(file)['state']

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

driver.minimize_window()
driver.get("https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml")

wait = WebDriverWait(driver, 20)

try:
    with open('rto_list.json', 'r') as file:
        all_rto_dict = json.load(file)
except FileNotFoundError:
    all_rto_dict = {}

for state in state_list:
    state_select_drop_down = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[2]/div/div/div[1]/div[2]/div[3]/div/div[3]/span')))
    time.sleep(1)
    state_select_drop_down.click()
    
    send_text = wait.until(EC.visibility_of_element_located((By.XPATH, f"//li[text()='{state}']")))
    time.sleep(1)
    send_text.click()
    time.sleep(2)
    
    rto_select_drop_down = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="selectedRto"]/div[3]')))
    time.sleep(1)
    rto_select_drop_down.click()
    time.sleep(1)
    
    options = driver.find_elements(By.XPATH, '//*[@id="selectedRto_panel"]')
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    select_element = soup.find('select', {'id': 'selectedRto_input'})
    rto_options = []
    for option in select_element.find_all('option'):
        rto_value = option.get('value')
        rto_name = option.text
        rto_options.append(rto_name)
    rto_options.pop(0)

    rto_dict = {state: rto_options}
    all_rto_dict.update(rto_dict)

    with open('rto_list.json', 'w') as file:
        json.dump(all_rto_dict, file, indent=4)

    print(f'Done -> {state}')
driver.close()
