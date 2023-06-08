from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import os
from functions import GetCenterCoordinates

# Lấy đường dẫn tuyệt đối của tệp Python hiện tại
current_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path_1 = os.path.join(current_directory, 'facilitiesIDs.json')

# Đọc dữ liệu từ tệp JSON
with open (json_file_path_1,"r") as file:
    input= json.load(file)

driver = webdriver.Chrome()

facilities={
    "facilities":[

    ]
}

for area in input["area"]:
    wayIDs=[]
    wayIDs.append(area["id"])
    for buildingID in area["buildingIDs"]:
        wayIDs.append(buildingID)
    for wayID in wayIDs:
        facility={
            "id":"",
            "master_facility_id":area["id"],
            "name":"unknown",
            "address":"unknown",
            "label":"unknown",
            "capacity":"unknown",
            "geometry":"polygon"
        }
        facility["id"]=wayID
        driver.get("https://www.openstreetmap.org/api/0.6/"+wayID)
        tags=driver.find_elements(By.TAG_NAME,"tag")
        for tag in tags:
            key=tag.get_attribute("k")
            value=tag.get_attribute("v")
            if(key=="name"):
                facility["name"]=value
            if(key=="building" or key=="landuse"):
                facility["label"]=value

        nodes_coordinates=[]
        nodes_ids=[]
        nds=driver.find_elements(By.TAG_NAME,"nd")
        for node_id in nds:
            nodes_ids.append(node_id.get_attribute("ref"))

        for node_id in nodes_ids:
            driver.get("https://www.openstreetmap.org/api/0.6/node/"+node_id)
            node=driver.find_element(By.TAG_NAME,"node")
            nodes_coordinates.append([node.get_attribute("lat"),node.get_attribute("lon")])

        facility["geolocation"]=GetCenterCoordinates(nodes_coordinates)
        facilities["facilities"].append(facility)


driver.close()

# Kết hợp đường dẫn tuyệt đối với tên tệp JSON
json_file_path_2 = os.path.join(current_directory,'output.json')
# Ghi dữ liệu JSON vào file
with open(json_file_path_2, 'w') as file:
    json.dump(facilities, file, indent=4)



