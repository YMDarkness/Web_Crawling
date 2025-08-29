from .modules.utils.Amazon import Amazon
from .modules.utils.Apple import Apple
from .modules.utils.AMD import AMD

from .modules.utils.BerkshireHathaway import BerkshireHathaway
from .modules.utils.BTC import BTC

from .modules.utils.COMEXGold import COMEXgold

from .modules.utils.Dxy import DXY

from .modules.utils.Google import Google

from .modules.utils.HanwhaAerospace import HanwhaAerospace
from .modules.utils.Hyundai import Hyundai

from .modules.utils.IXIC import IXIC

from .modules.utils.JPY import Jpy

from .modules.utils.Kakao import Kakao
from .modules.utils.Kia import Kia
from .modules.utils.Kospi import Kospi

from .modules.utils.LGensol import LGensol

from .modules.utils.Meta import Meta
from .modules.utils.Microsoft import Microsoft

from .modules.utils.Naver import Naver
from .modules.utils.Netflix import Netflix
from .modules.utils.Nvidia import Nvidia
from .modules.utils.N225 import N225

from .modules.utils.PoscoHoldings import PoscoHoldings

from .modules.utils.SamsungBioLogics import SamsungBioLogics
from .modules.utils.SamsungElectronics import SamsungElectronics
from .modules.utils.SKHynix import SKHynix
from .modules.utils.SP500 import GSPC

from .modules.utils.Tesla import Tesla

from .modules.utils.US10Y import US10Y
from .modules.utils.USD import Usd

from .modules.utils.Vix import VIX

from .modules.utils.Wti import WTI

# 메인

def main():
    # 국내
    # 한화에어로스페이스
    hanwha = HanwhaAerospace()
    hanwha.fetch_data()
    hanwha.parse_data()

    print(hanwha.prometheus_format())

    # 카카오
    kakao = Kakao()
    kakao.fetch_data()
    kakao.parse_data()

    print(kakao.prometheus_format())

    # 기아
    kia = Kia()
    kia.fetch_data()
    kia.parse_data()

    print(kia.prometheus_format())

    # LG 에너지솔루션
    lgensol = LGensol()
    lgensol.fetch_data()
    lgensol.parse_data()

    print(lgensol.prometheus_format())

    # 네이버
    naver = Naver()
    naver.fetch_data()
    naver.parse_data()

    print(naver.prometheus_format())

    # 포스코홀딩스
    posco = PoscoHoldings()
    posco.fetch_data()
    posco.parse_data()

    print(posco.prometheus_format())

    # SK하이닉스
    skhynix = SKHynix()
    skhynix.fetch_data()
    skhynix.parse_data()

    print(skhynix.prometheus_format())

    # 삼성전자
    samsung_electro = SamsungElectronics()
    samsung_electro.fetch_data()
    samsung_electro.parse_data()

    print(samsung_electro.prometheus_format())

    # 삼성바이오로직스
    samsung_bio = SamsungBioLogics
    samsung_bio.fetch_data()
    samsung_bio.parse_data()

    print(samsung_bio.prometheus_format())

    # 현대
    hyundai = Hyundai()
    hyundai.fetch_data()
    hyundai.parse_data()

    print(hyundai.prometheus_format())
    

    # 해외
    # AMD
    amd = AMD()
    amd.fetch_data()
    amd.parse_data()

    print(amd.prometheus_format())

    # 아마존
    amazon = Amazon()
    amazon.fetch_data()
    amazon.parse_data()

    print(amazon.prometheus_format())

    # 애플
    apple = Apple()
    apple.fetch_data()
    apple.parse_data()

    print(apple.prometheus_format())

    # 버크셔헤서웨이
    hathaway = BerkshireHathaway()
    hathaway.fetch_data()
    hathaway.parse_data()

    print(hathaway.prometheus_format())

    # 알파벳(구글)
    google = Google()
    google.fetch_data()
    google.parse_data()

    print(google.prometheus_format())

    # 메타(구 페이스북)
    meta = Meta()
    meta.fetch_data()
    meta.parse_data()

    print(meta.prometheus_format())

    # 마이크로소프트
    microsoft = Microsoft()
    microsoft.fetch_data()
    microsoft.parse_data()

    print(microsoft.prometheus_format())

    # 넷플릭스
    netflix = Netflix()
    netflix.fetch_data()
    netflix.parse_data()

    print(netflix.prometheus_format())

    # 엔비디아
    nvidia = Nvidia()
    nvidia.fetch_data()
    nvidia.parse_data()

    print(nvidia.prometheus_format())

    # 테슬라
    tesla = Tesla()
    tesla.fetch_data()
    tesla.parse_data()

    print(tesla.prometheus_format())


    # 시장
    # 코스피
    kospi = Kospi()
    kospi.fetch_data()
    kospi.parse_data()

    print(kospi.prometheus_format())

    # 비트코인
    btc = BTC()
    btc.fetch_data()
    btc.parse_data()

    print(btc.prometheus_format())

    # 국제 금
    comex_gold = COMEXgold()
    comex_gold.fetch_data()
    comex_gold.parse_data()

    print(comex_gold.prometheus_format())

    # 달러 인덱스
    dxy = DXY()
    dxy.fetch_data()
    dxy.parse_data()

    print(dxy.prometheus_format())

    # 나스닥
    ixic = IXIC()
    ixic.fetch_data()
    ixic.parse_data()

    print(ixic.prometheus_format())

    # S&P500
    sp500 = GSPC()
    sp500.fetch_data()
    sp500.parse_data()

    print(sp500.prometheus_format())

    # 미국 국채 10년
    us10y = US10Y()
    us10y.fetch_data()
    us10y.parse_data()

    print(us10y.prometheus_format())

    # 변동성 지수
    vix = VIX()
    vix.fetch_data()
    vix.parse_data()

    print(vix.prometheus_format())

    # 서부 텍사스 중질유
    wti = WTI()
    wti.fetch_data()
    wti.parse_data()

    print(wti.prometheus_format())

    # 일본 니케이 225
    n225 = N225()
    n225.fetch_data()
    n225.parse_data()

    print(n225.prometheus_format())


    # 환율
    # 달러
    usd = Usd()
    usd.fetch_data()
    usd.parse_data()

    print(usd.prometheus_format())

    # 엔화
    jpy = Jpy()
    jpy.fetch_data()
    jpy.parse_data()

    print(jpy.prometheus_format())

if __name__ == "__main__":
    main()