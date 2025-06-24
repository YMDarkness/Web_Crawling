from modules.market_collector import MarketCollector
from modules.gold_collector import GoldCollector
from modules.news_collector import NewsCollector
from modules.kospi_collector import KospiCollector
from modules.dji_collector import DJICollector
from modules.n225_collector import N225Collector
from modules.sp_collector import SpCollector
from modules.ixic_collector import IXICCollector
from modules.wti_collector import WTICollector
from modules.gasoline_collector import GasolineCollector

# main

def main():
    # 환율
    market = MarketCollector()
    market.fetch()
    market.parse()
    
    print(market.to_prometheus_format())

    # 금 시세
    gold = GoldCollector()
    gold.fetch()
    gold.parse()
    
    print(gold.to_prometheus_format())

    # 증권 뉴스
    news = NewsCollector()
    news.fetch()
    news.parse()

    print(news.to_prometheus_format())

    # kospi
    kospi = KospiCollector()
    kospi.fetch()
    kospi.parse()

    print(kospi.to_prometheus_format())

    # s&p500
    sp = SpCollector()
    sp.fetch()
    sp.parse()

    print(sp.to_prometheus_format())

    # 나스닥
    ixic = IXICCollector()
    ixic.fetch()
    ixic.parse()

    print(ixic.to_prometheus_format())

    # 다우존스
    dji = DJICollector()
    dji.fetch()
    dji.parse()

    print(dji.to_prometheus_format())

    # 니케이225
    n225 = N225Collector()
    n225.fetch()
    n225.parse()

    print(n225.to_prometheus_format())

    # WTI
    wti = WTICollector()
    wti.fetch()
    wti.parse()

    print(wti.to_prometheus_format())

    # 휘발유
    gasoline = GasolineCollector()
    gasoline.fetch()
    gasoline.parse()

    print(gasoline.to_prometheus_format())

if __name__ == "__main__":
    main()
