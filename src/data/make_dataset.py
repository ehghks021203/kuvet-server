import os
import sys
import pymysql
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from config.database import Database
from api import LivestockDiseaseOccurrenceStatusAPI

if __name__ == "__main__":
    start_point = 1001
    end_point = 45000
    api = LivestockDiseaseOccurrenceStatusAPI()
    db = Database()
    
    for i in range(start_point, end_point, 1000):
        print(f"GET DATA: {i} ~ {i + 999}")
        response = api.get_data(start_point=i, count=1000)
        for r in response:
            try:
                sql = f"""
                INSERT INTO disease_status 
                (disease_code, disease_name, farm_name, addr_code, addr_name, occur_date, livestock_type, occur_count, dgnss_engn, end_date)
                VALUE 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                db.execute(sql, (r["ICTSD_OCCRRNC_NO"], r["LKNTS_NM"], r["FARM_NM"], r["FARM_LOCPLC_LEGALDONG_CODE"], r["FARM_LOCPLC"], r["OCCRRNC_DE"], r["LVSTCKSPC_NM"], r["OCCRRNC_LVSTCKCNT"], r["DGNSS_ENGN_NM"], r["CESSATION_DE"]))
                db.commit()
                db.close()
            except:
                print(f"Error Occured:: {r}")