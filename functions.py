import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By

def GetCenterCoordinates(coordinatesData):
    lat_sum=0
    lon_sum=0
    for i in range(len(coordinatesData)):
        lat_sum=lat_sum+float(coordinatesData[i][0])
        lon_sum=lon_sum+float(coordinatesData[i][1])
    center_lat=round(lat_sum/len(coordinatesData),4)
    center_lon=round(lon_sum/len(coordinatesData),4)
    return [center_lat,center_lon]

def randomUUID(limit):
    random_uuid = [uuid.uuid4() for _ in range(limit)]
    return random_uuid

def ReturnFacilityData(driver,facilityID,masterFacilityID,facilityTypesIDs,facilityType):
        facility={
            "id":facilityID,
            "name":"unknown",
            "address":"unknown",
            "label":"unknown",
            "capacity":"unknown",
            "geometry":"polygon",
            "geolocation":"unknown",      #center coordinates
            "zoom":17,
            'facilitytype_id':facilityTypesIDs[facilityType],
            'valid': True,
            'startdate':"unknown",
            'enddate':"unknown",
            "lastchange":"unknown",
            "master_facility_id":masterFacilityID,
            "coordinates":"unknown"
        }
        driver.get("https://www.openstreetmap.org/api/0.6/"+facilityID)
        way= driver.find_element(By.TAG_NAME,"way")
        facility["lastchange"]=way.get_attribute("timestamp")

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
        facility["coordinates"]=nodes_coordinates
        return facility
        