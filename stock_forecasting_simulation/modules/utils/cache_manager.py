import os
import pickle
import time

# 캐심 로직 처리 (예: 파일 기반 또는 메모리 기반)

def save_cache(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

def load_cache(path):
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        return pickle.load(f)
    
def is_cache_valid(path, max_age_seconds=3600):
    if not os.path.exists(path):
        return False
    return (os.path.getmtime(path) + max_age_seconds) > time.time()
