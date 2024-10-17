from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json

driver = webdriver.Chrome()

wait = WebDriverWait(driver, 20)

driver.get('https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml') 

dropdown_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="j_idt40"]/div[3]')))
dropdown_button.click()

try:
    dropdown_panel = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="j_idt40_panel"]')))
    time.sleep(2)
    options = driver.find_elements(By.XPATH, '//*[@id="j_idt40_panel"]')
    options_list = [option.text for option in options]
    options_list = options_list[0].split('\n')
    options_list.pop(0)
    sate_dict = {}
    sate_dict['state'] = options_list
    with open('state.json', 'w') as file:
        json.dump(sate_dict, file)
except Exception as e:
    print(f"An error occurred: {e}")

driver.quit()
