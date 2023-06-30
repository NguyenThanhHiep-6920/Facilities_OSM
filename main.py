from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import os
from functions import GetFacilityData

# Číst data ze souboru facilitiesIDs.json
current_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path_1 = os.path.join(current_directory, 'facilitiesIDs.json')

with open (json_file_path_1,"r") as file:
    input= json.load(file)

facilityTypesIDs = ["areaTypeID","buildingTypeID"]
#databáze
facilities={
    "facilities":[

    ]
}
#provádět načítání dat
driver = webdriver.Chrome()

for area in input["areas"]:
    facilities["facilities"].append(GetFacilityData(driver,area["id"],area["id"],facilityTypesIDs,0))
    for buildingID in area["buildingIDs"]:
        facilities["facilities"].append(GetFacilityData(driver,buildingID,area["id"],facilityTypesIDs,1))

driver.close()

# Zapište data do souboru output.json
json_file_path_2 = os.path.join(current_directory,'output.json')
with open(json_file_path_2, 'w') as file:
    json.dump(facilities, file, indent=4)



