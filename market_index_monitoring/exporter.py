from flask import Flask, Response, jsonify
from modules.market_collector import MarketCollector
from modules.gold_collector import GoldCollector
from modules.news_collector import NewsCollector
from modules.kospi_collector import KospiCollector
from modules.dji_collector import DJICollector
from modules.n225_collector import N225Collector
from modules.ixic_collector import IXICCollector
from modules.sp_collector import SpCollector
from modules.wti_collector import WTICollector
from modules.gasoline_collector import GasolineCollector

# 프로메테우스 exporter 실행

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    collectors = [
        MarketCollector(), 
        GoldCollector(), 
        KospiCollector(), 
        DJICollector(), 
        N225Collector(), 
        IXICCollector(), 
        SpCollector(),
        WTICollector(),
        GasolineCollector()
        ]
    output = ""
    try:
        for c in collectors:
            print(f'[DEBUG] running : {c.__class__.__name__}', flush=True)
            c.fetch()
            c.parse()
            output += c.to_prometheus_format()
    except Exception as e:
        import traceback
        print('/metrics error : ', traceback.format_exc(), flush=True)
        return Response('Interval Server Error', status=500)
    return Response(output, mimetype="text/plain")

@app.route("/news")
def news():
    news_collector = NewsCollector()
    output = ""
    try:
        print(f'[DEBUG] running : {news_collector.__class__.__name__}', flush=True)
        news_collector.fetch()
        news_collector.parse()
        output = news_collector.data
    except Exception as e:
        import traceback
        print('/metrics error : ', traceback.format_exc(), flush=True)
        return jsonify({'error' : 'Interval Server Error'}), 500
    return jsonify(output)
    
    '''
    jsonify
    Flask에서 딕셔너리 데이터를 JSON 응답으로 변환해주는 함수
    브라우저나 API 클라이언트가 이해할 수 있는 JSON 포맷으로 결과를 반환
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
