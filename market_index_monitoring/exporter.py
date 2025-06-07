from flask import Flask, Response
from modules.market_collector import MarketCollector
from modules.gold_collector import GoldCollector
from modules.news_collector import NewsCollector

# 프로메테우스 exporter 실행

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    collectors = [MarketCollector(), GoldCollector()]
    output = ""
    for c in collectors:
        c.fetch()
        c.parse()
        output += c.to_prometheus_format()
    return Response(output, mimetype="text/plain")

@app.route("/news")
def news():
    news_collector = NewsCollector()
    news_collector.fetch()
    news_collector.parse()
    return jsonify(news_collector.data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
