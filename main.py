from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import os
from functions import ReturnFacilityData

# Lấy đường dẫn tuyệt đối của tệp Python hiện tại
current_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path_1 = os.path.join(current_directory, 'facilitiesIDs.json')

# Đọc dữ liệu từ tệp JSON
with open (json_file_path_1,"r") as file:
    input= json.load(file)

facilityTypesIDs = ["areaTypeID","buildingTypeID"]

driver = webdriver.Chrome()

facilities={
    "facilities":[

    ]
}

for area in input["areas"]:
    facilities["facilities"].append(ReturnFacilityData(driver,area["id"],area["id"],facilityTypesIDs,0))
    for buildingID in area["buildingIDs"]:
        facilities["facilities"].append(ReturnFacilityData(driver,buildingID,area["id"],facilityTypesIDs,1))

driver.close()

# Kết hợp đường dẫn tuyệt đối với tên tệp JSON
json_file_path_2 = os.path.join(current_directory,'output.json')
# Ghi dữ liệu JSON vào file
with open(json_file_path_2, 'w') as file:
    json.dump(facilities, file, indent=4)



