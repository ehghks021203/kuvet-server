import json
import csv
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from config.default import BASE_DIR
from config.database import Database

def get_geo_polygon(region_type="emd"):
    if region_type not in ["sido", "sig", "emd"]:
        raise NameError("Wrong region type")
    with open(BASE_DIR + "/data/" + region_type + ".json", "r") as geo_file:
        data = json.load(geo_file)
    return data["features"]

def geo_polygon_centroid(multi_polygon):
    centroids = []
    total_area = 0
    
    for polygon in multi_polygon:
        for coords in polygon:
            x_sum = 0
            y_sum = 0
            n = len(coords)
            
            for coord in coords:
                x_sum += coord[1]
                y_sum += coord[0]
            centroid = [y_sum / n, x_sum / n]
            centroids.append(centroid)
            total_area += 1  # 각 폴리곤의 영역을 1로 간주 (단순화)
    
    x_sum = sum([centroid[1] for centroid in centroids])
    y_sum = sum([centroid[0] for centroid in centroids])
    
    return [y_sum / total_area, x_sum / total_area]

if __name__ == "__main__":
    db = Database()
    rt = "emd"
    polygon = get_geo_polygon(rt)
    count = 1
    for p in polygon:
        try:
            if rt == "emd":
                print(f"({count:4d}/{len(polygon):4d}) {p['properties']['EMD_CD']}")
                sql = "INSERT INTO geometry_data (code, centroid_lat, centroid_lng, multi_polygon) VALUES (%s, %s, %s, %s)"
                centroid = geo_polygon_centroid(p["geometry"]["coordinates"])
                db.execute(sql, (p["properties"]["EMD_CD"], centroid[1], centroid[0], json.dumps(p["geometry"]["coordinates"])))
                db.commit()
                count += 1
            elif rt == "sig":
                print(f"({count:4d}/{len(polygon):4d}) {p['properties']['SIG_CD']}")
                sql = "INSERT INTO geometry_data (code, centroid_lat, centroid_lng, multi_polygon) VALUES (%s, %s, %s, %s)"
                centroid = geo_polygon_centroid(p["geometry"]["coordinates"])
                db.execute(sql, (p["properties"]["SIG_CD"], centroid[1], centroid[0], json.dumps(p["geometry"]["coordinates"])))
                db.commit()
                count += 1
            elif rt == "sido":
                print(f"({count:4d}/{len(polygon):4d}) {p['properties']['CTPRVN_CD']}")
                sql = "INSERT INTO geometry_data (code, centroid_lat, centroid_lng, multi_polygon) VALUES (%s, %s, %s, %s)"
                centroid = geo_polygon_centroid(p["geometry"]["coordinates"])
                db.execute(sql, (p["properties"]["CTPRVN_CD"], centroid[1], centroid[0], json.dumps(p["geometry"]["coordinates"])))
                db.commit()
                count += 1
        except Exception as e:
            print(f"Error Occured! {e}")