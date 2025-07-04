import pandas as pd
import json
import csv

# CSV/JSON 파일 불러오기 및 저장

def load_csv(path):
    return pd.read_csv(path)

def save_csv(df, path):
    df.to_csv(path, index=False)

def load_json(path):
    with open(path, 'r', encoding='utf-8-sig') as f:
        return json.load(f)
    
def save_json(data, path):
    with open(path, 'w', encoding='utf-8-sig') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
