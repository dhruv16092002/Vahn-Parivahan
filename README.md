# Vahan-Parivahan Data Scraping Project

This project involves web scraping using Selenium and Beautiful Soup to extract data from the Vahan Parivahan portal. The goal is to gather month-wise and RTO-wise information on registered cars and two-wheelers across all states.

## Website
[Vahan Parivahan Dashboard](https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml)

## Key Features
- Scrapes data for every state and Regional Transport Office (RTO) listed on the website.
- Extracts monthly data on the number of registered vehicles (cars and two-wheelers).
- Utilizes **Selenium** for automating navigation of dynamic web elements.
- **Beautiful Soup** is used for parsing and cleaning HTML data.

## Tools & Technologies
- **Selenium** - for browser automation.
- **Beautiful Soup** - for parsing and scraping HTML data.
- **Python** - as the primary programming language.

## How to Run the Project

1. Clone the repository.
2. Install the required dependencies:
    ```bash
    pip install -r requirement.txt
    ```
3. Step 0: Create a Python environment:
    ```bash
    python -m venv env
    env\Scripts\activate 
    cd /path/to/your/project/directory
    ```
4. Step 1: Scrape the list of states from the website:
    ```bash
    python 1_get_state_list.py
    ```
After running this command, a file named `state.json` will be created.

5. Step 2: Scrape all RTOs from the website:
    ```bash
    python 2_get_rto_list.py
    ```
After running this command, a file named `rto.json` will be created.

### Important Notes
- Change the `download_directory` path to your desired folder.
- Set the `vehicle_category` according to your specific needs.

6. Step 3: Start scraping the website:
    ```bash
    python 3_vahan.py
    ```
After running this, all scraped data will be stored in the `vahan` folder.

7. Step 4: Transform the data according to your requirements:
    ```bash
    python 4_transformation.py
    ```
   After running this, a new file `result.csv` will be created under the folder with the scraped data.

8. Step 5: Merge the data:
    ```bash
    python 5_merge.py
    ```
    After running this, a file will be created based on the variables, such as `vehicle_class` in the `5_merge.py` file, e.g., `MOTOR_CAR.csv`. Adjust the output file name according to your needs.
