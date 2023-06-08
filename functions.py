def GetCenterCoordinates(coordinatesData):
    lat_sum=0
    lon_sum=0
    for i in range(len(coordinatesData)):
        lat_sum=lat_sum+float(coordinatesData[i][0])
        lon_sum=lon_sum+float(coordinatesData[i][1])
    center_lat=round(lat_sum/len(coordinatesData),4)
    center_lon=round(lon_sum/len(coordinatesData),4)
    return [center_lat,center_lon]