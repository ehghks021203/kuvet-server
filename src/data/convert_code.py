import csv
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from config.default import BASE_DIR

def code2addr(code: str, all_name=True):
    with open(BASE_DIR + "/data/PnuCode.csv") as data:
        csv_mapping = list(csv.DictReader(data))
    if all_name:
        if len(code) == 2:
            for d in csv_mapping:
                if d["code"][0:2] == code:
                    return f"{d['sido']}"
        elif len(code) == 5:
            for d in csv_mapping:
                if d["code"][0:5] == code:
                    return f"{d['sido']} {d['sigungu']}"
        elif len(code) == 8:
            for d in csv_mapping:
                if d["code"][0:8] == code:
                    return f"{d['sido']} {d['sigungu']} {d['eupmyeondong']}"
    else:
        if len(code) == 2:
            for d in csv_mapping:
                if d["code"][0:2] == code:
                    return f"{d['sido']}"
        elif len(code) == 5:
            for d in csv_mapping:
                if d["code"][0:5] == code:
                    return f"{d['sigungu']}"
        elif len(code) == 8:
            for d in csv_mapping:
                if d["code"][0:8] == code:
                    return f"{d['eupmyeondong']}"