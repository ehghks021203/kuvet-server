import requests
import xmltodict
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from config import api

class LivestockDiseaseOccurrenceStatusAPI():
    def get_data(self, start_point: int, count: int):
        url = f"http://211.237.50.150:7080/openapi/{api.MAFRA_API_KEY}/xml/Grid_20151204000000000316_1/{start_point}/{start_point + count - 1}?"
        response = xmltodict.parse(requests.get(url).text)
        return response["Grid_20151204000000000316_1"]["row"]
    
class GetGeometryDataAPI():
    # 요청 파라미터 (변동되지 않음)
    service = "data"
    req = "GetFeature"
    page = 1
    size = 1000

    # 엔드포인트
    endpoint = "http://api.vworld.kr/req/data"
    def get_data(self, pnu, region_type="sido"):
        key = api.VWORLD_API_KEY

        if region_type == "sido":
            data = "LT_C_ADSIDO_INFO"
            attrFilter = f"ctprvn_cd:LIKE:{pnu[0:2]}"
        elif region_type == "sig":
            data = "LT_C_ADSIGG_INFO"
            attrFilter = f"sig_cd:LIKE:{pnu[0:5]}"
        elif region_type == "emd":
            data = "LT_C_ADEMD_INFO"
            attrFilter = f"emd_cd:LIKE:{pnu[0:8]}"
        # if len(pnu) == 5:
        #     data = "LT_C_ADEMD_INFO"
        #     attrFilter = f"emd_cd:LIKE:{pnu}"
        # elif len(pnu) == 2:
        #     data = "LT_C_ADSIGG_INFO"
        #     attrFilter = f"sig_cd:LIKE:{pnu}"
        
        url = f"{self.endpoint}?service={self.service}&request={self.req}&data={data}&key={key}&attrFilter={attrFilter}&page={self.page}&size={self.size}"
        response = json.loads(requests.get(url).text)
        if (response["response"]["status"] == "NOT_FOUND"):
            return None
        else:
            return response["response"]["result"]["featureCollection"]["features"]

if __name__ == "__main__":
    api = LivestockDiseaseOccurrenceStatusAPI()
    print(api.get_data(1, 10))