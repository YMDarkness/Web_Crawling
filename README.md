파이썬을 활용한 웹 크롤링입니다.

market_index_monitoring 프로젝트는 도커와 쿠버네티스를 접목해 실시간 모니터링이 가능하도록 하였습니다.

stock_forecasting_monitoring 프로젝트는 market_index_monitoring의 확장판입니다
market_index_monitoring에서 bs4를 활용해 크롤링을 했다면 stock_forecasting_monitoring에서는 셀레니움을 도입하였습니다

kospi_test, market_index, gold_price_test, naver_pay에는 파일명_schedule.py 이라는 자동화 파일이 있어 이를 통해 데이터를 수집합니다.
수집된 데이터는 각각의 예측 모델에 대입됩니다.
