from crwal_kospi import kospi_crwal
from process_kospi import process_kospi_date
from kospi_days import day_of_kospi
from kospi_ratio import ratio_kospi
from forect_kospi import randomforest_kospi
from kospi_bollinger_bands import bollinger_kospi
from kospi_XGBClassifier import kospi_model_upgrade

def main():
    #코스피 지수 크롤링
    df_kospi = kospi_crwal()

    #코스피 지수 전처리
    df_kospi = process_kospi_date(df_kospi)

    #코스피 지수 요일 칼럼
    df_kospi = day_of_kospi(df_kospi)

    #코스피 지수 상승여부 및 변동성 지표
    df_kospi = ratio_kospi(df_kospi)

    #코스피 지수 등락율 기준으로 양/음봉
    #df_kospi = 
    
    #랜덤포레스트
    df_kospi = randomforest_kospi(df_kospi)
    
    #볼린저 밴드
    df_kospi = bollinger_kospi(df_kospi)

    #코스피 지수 예측 – XGBoost / LightGBM
    #df_kospi = kospi_model_upgrade(df_kospi, model_type='XGB')
    df_kospi = kospi_model_upgrade(df_kospi, model_type='XGB')

if __name__ == '__main__':
    main()
