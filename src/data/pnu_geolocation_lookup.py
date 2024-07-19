from PyKakao import Local
from config import api

def get_pnu(lat: float, lng: float) -> tuple:
    """입력된 좌표의 PNU 코드 조회
        
    Params:
        lat `float`: 
            위도 좌표
        lng `float`: 
            경도 좌표
    
    Returns:
        pnu `str`:
            19자리 PNU 코드
        addressName `str`:
            토지 지번 주소
    """
    # 로컬 API 인스턴스 생성
    local = Local(service_key=api.KAKAO_API_KEY)
    request_address = local.geo_coord2address(lng, lat, dataframe=False)
    request_region = local.geo_coord2regioncode(lng, lat, dataframe=False)
    if request_region == None:
        return None, None
    i = 0 if request_region["documents"][0]["region_type"] == "B" else 1
    pnu = request_region["documents"][i]["code"]
    address = request_region["documents"][i]["address_name"]
    
    if request_address["meta"]["total_count"] == 0:
        return pnu, address
    address = address + " " + request_address["documents"][i]["address"]["main_address_no"]
    if request_address["documents"][i]["address"]["sub_address_no"] != "":
        address = address + "-" + request_address["documents"][i]["address"]["sub_address_no"]
    if request_address["documents"][i]["address"]["mountain_yn"] == "N":
        mountain = "1"   # 산 X
    else:
        mountain = "2"   # 산 O

    # 본번과 부번의 포멧을 '0000'으로 맞춰줌
    main_no = request_address["documents"][0]["address"]["main_address_no"].zfill(4)
    sub_no = request_address["documents"][0]["address"]["sub_address_no"].zfill(4)
    pnu = str(pnu + mountain + main_no + sub_no)
    return pnu, address

def get_word(word: str) -> tuple:
    """입력된 주소의 좌표 조회

    Params:
        word `str`: 
            지번 주소
    
    Returns:
        lat `float`:
            위도 좌표
        lng `float`:
            경도 좌표
    """
    # 로컬 API 인스턴스 생성
    local = Local(service_key=api.KAKAO_API_KEY)
    request_address = local.search_address(word, dataframe=False)
    if len(request_address["documents"]) == 0:
        return None, None
    lng = request_address["documents"][0]["x"]
    lat = request_address["documents"][0]["y"]
    return lat, lng
