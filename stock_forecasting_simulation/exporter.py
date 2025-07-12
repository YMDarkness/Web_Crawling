from modules.utils import domestics, worlds, goldoil, etc

from flask import Flask, Response, jsonify

# Exporter 서버 실행을 위해 프로메테우스-그라파나 연동

# 카테고리 통합
all_collectors = domestics + worlds + goldoil + etc

# 각 클래스를 인스턴스로 초기화
collectors = [cls() for cls in all_collectors]

app = Flask(__name__)

@app.route('/metrics')

def metrics():
    results = []
    try:
        for collector in collectors:
            print(f'[DEBUG] running : {collector.__class__.__name__}', flush=True)
            collector.fetch_data()
            collector.parse_data()
            results.append(collector.prometheus_format())
            if hasattr(collector, 'quit'):
                collector.quit()
    except Exception as e:
        import traceback
        print('/Metrics Error : ', traceback.format_exc(), flush=True)
        return Response('Interval Server Error', status=500)
    # 응답 상태 구체화 (정상 200 명시)
    return Response('\n'.join(results), mimetype='text/plain', status=200)

# Prometheus의 livenessProbe, readinessProbe 용도
@app.route('/ping')
def ping():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9100)
    