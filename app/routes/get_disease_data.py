from flask import Blueprint, request, jsonify
import os
import sys
import json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from config.database import Database
from src.data.api import GetGeometryDataAPI
from src.data.pnu_geolocation_lookup import get_pnu, get_word
from src.data.convert_code import code2addr

get_disease_data_routes = Blueprint("get_disease_data", __name__)

def _get_disease_clustering_datas(lat, lng, level, target_filter="all"):
    db = Database()
    pnu, address = get_pnu(float(lat), float(lng))

    return_list = []
    if level <= 8:
        addr_length = 2
        like_pattern = f"%"
        
    elif level <= 12:
        addr_length = 5
        like_pattern = f"{pnu[0:2]}%"
    else:
        addr_length = 8
        like_pattern = f"{pnu[0:5]}%"

    sql = """
    WITH grouped_data AS (
        SELECT 
            LEFT(addr_code, %s) AS addr_code_prefix, 
            SUM(occur_count) AS total_count
        FROM 
            disease_status
        WHERE
            addr_code LIKE %s AND livestock_type RLIKE '^(돼지|소|닭)'
        GROUP BY 
            addr_code_prefix
    ),
    stats AS (
        SELECT 
            SUM(total_count) AS total
        FROM 
            grouped_data
    )
    SELECT 
        g.addr_code_prefix, 
        g.total_count, 
        g.total_count / NULLIF(s.total, 0) AS normalized_ratio,
        gd.centroid_lat,
        gd.centroid_lng,
        gd.multi_polygon
    FROM 
        grouped_data g
    CROSS JOIN 
        stats s
    INNER JOIN 
        geometry_data gd ON gd.code = g.addr_code_prefix
    ORDER BY 
        g.total_count DESC;
    """
    res = db.executeAll(sql, (addr_length, like_pattern))
    db.close()
    if len(res) == 0:
        return []

    for r in res:
        target_addr = code2addr(r["addr_code_prefix"])
        return_list.append({
            "addr_name": target_addr,
            "addr_code": r["addr_code_prefix"],
            "lat": r["centroid_lat"],
            "lng": r["centroid_lng"],
            "geometry": json.loads(r["multi_polygon"]),
            "total_occur_count": r["total_count"],
            "alpha": r["normalized_ratio"],
            "filter": target_filter
        })
    return return_list

def _get_occur_disease_list(lat=None, lng=None, level=None, pnu=None, target_filter="all"):
    db = Database()
    if not pnu and lat and lng:
        pnu, address = get_pnu(float(lat), float(lng))
        target_addr = code2addr(pnu[0:8])
        if target_addr:
            if level <= 8:
                target_addr = code2addr(pnu[0:2], all_name=False)
                like_pattern = f"{pnu[0:2]}%"
            elif level <= 12:
                target_addr = code2addr(pnu[0:5], all_name=False)
                like_pattern = f"{pnu[0:5]}%"
            else:
                target_addr = code2addr(pnu[0:8], all_name=False)
                like_pattern = f"{pnu[0:8]}%"
        else: 
            if level <= 8:
                target_addr = address.split(" ")[0]
                like_pattern = f"{pnu[0:2]}%"
            elif level <= 12:
                target_addr = address.split(" ")[1]
                like_pattern = f"{pnu[0:5]}%"
            else:
                target_addr = address.split(" ")[2]
                like_pattern = f"{pnu[0:8]}%"
    
    if target_filter == "all":
        sql = "SELECT * FROM disease_status where addr_code LIKE %s AND livestock_type RLIKE '^(돼지|소|닭)' ORDER BY occur_date DESC"
    elif target_filter == "pig":
        sql = "SELECT * FROM disease_status where addr_code LIKE %s AND livestock_type LIKE '돼지%' ORDER BY occur_date DESC"
    elif target_filter == "cow":
        sql = "SELECT * FROM disease_status where addr_code LIKE %s AND livestock_type LIKE '소%' ORDER BY occur_date DESC"
    elif target_filter == "chicken":
        sql = "SELECT * FROM disease_status where addr_code LIKE %s AND livestock_type LIKE '닭%' ORDER BY occur_date DESC"
    res = db.executeAll(sql, (like_pattern))
    db.close()
    sum_count = 0
    for r in res:
        sum_count += r["occur_count"]
    
    return_dict = {
        "addr": target_addr,
        "disease_list": res,
        "total_occur_count": sum_count,
        "filter": target_filter
    }
    return return_dict


@get_disease_data_routes.route("/get_center_addr", methods=["GET"])
def get_center_addr():
    """
    Params:
        lat `float`(필수): 
            위도 좌표
        lng `float`(필수): 
            경도 좌표
    Returns:
        result `str`:
            응답 성공 여부 (success, error)
        msg `str`:
            응답 메시지
        addr `str`:

    """
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    level = int(request.args.get("level"))

    if not lat or not lng or not level:
        return jsonify({
            "result":"error", 
            "msg":"request parameter missing"
        }), 401

    pnu, address = get_pnu(float(lat), float(lng))

    target_addr = code2addr(pnu[0:8])
    if target_addr:
        if level <= 8:
            target_addr = "전체"
        elif level <= 12:
            target_addr = target_addr.split(" ")[0]
        else:
            target_addr = target_addr.split(" ")[1]
    else: 
            if level <= 8:
                target_addr = "전체"
            elif level <= 12:
                target_addr = address.split(" ")[0]
            else:
                target_addr = address.split(" ")[1]
    
    return jsonify({
        "result":"success", 
        "msg":"get disease clustering datas", 
        "addr": target_addr, 
    }), 200

@get_disease_data_routes.route("/get_disease_clustering", methods=["GET"])
def get_disease_clustering():
    """
    Params:
        lat `float`(필수): 
            위도 좌표
        lng `float`(필수): 
            경도 좌표
        level `int`(필수):
            지도의 확대 레벨
        target_filter `str`(선택, 기본값=all):
            가축 타입 필터 (돼지 pig, 소 cow, 닭 chicken, 전체 all)
    Returns:
        result `str`:
            응답 성공 여부 (success, error)
        msg `str`:
            응답 메시지
        data `list`:
            질병 발생 현황 클러스터링 데이터
    """
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    level = int(request.args.get("level"))
    target_filter = request.args.get("target_filter")

    if not lat or not lng or not level:
        return jsonify({
            "result":"error", 
            "msg":"request parameter missing"
        }), 401
    if not target_filter:
        target_filter = "all"

    data = _get_disease_clustering_datas(lat, lng, level, target_filter)
    
    return jsonify({
        "result":"success", 
        "msg":"get disease clustering datas", 
        "data": data, 
    }), 200

@get_disease_data_routes.route("/get_occur_disease_list", methods=["GET"])
def get_occur_disease_list():
    """
    Params:
        lat `float`: 
            위도 좌표
        lng `float`: 
            경도 좌표
        level `int`:
            지도의 확대 레벨
        target_filter `str`:
            가축 타입 필터 (돼지 pig, 소 cow, 닭 chicken, 전체 all)
    Returns:
        result `str`:
            응답 성공 여부 (success, error)
        msg `str`:
            응답 메시지
        data `list`:
            질병 발생 현황 클러스터링 데이터
    """
    pnu = request.args.get("pnu")
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    level = int(request.args.get("level"))
    target_filter = request.args.get("target_filter")
    if not target_filter:
        target_filter = "all"
    
    if not lat and not lng and not level and pnu:
        data = _get_occur_disease_list(pnu=pnu, target_filter=target_filter)
    elif not pnu and lat and lng and level:
        data = _get_occur_disease_list(lat=lat, lng=lng, level=level, target_filter=target_filter)
    else:
        return jsonify({
            "result":"error", 
            "msg":"request parameter missing"
        }), 401
    
    return jsonify({
        "result":"success", 
        "msg":"get occur disease datas", 
        "data": data, 
    }), 200

if __name__ == "__main__":
    _get_disease_clustering_datas(37.0047135, 127.2988799, 5)
