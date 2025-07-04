from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from kospi_bollinger_bands import bollinger_kospi

#코스피 지수 예측 – XGBoost / LightGBM
def kospi_model_upgrade(df_kospi, model_type='XGB'):
    df_kospi = bollinger_kospi(df_kospi)

    #df_kospi['종가_3일후'] = df_kospi['종가'].shift(-3)
    #df_kospi['종가_5일후'] = df_kospi['종가'].shift(-5)

    df_kospi['이동평균_3일'] = df_kospi['종가'].rolling(window=3).mean()
    df_kospi['이동평균_5일'] = df_kospi['종가'].rolling(window=5).mean()

    df_kospi['전일_대비_변화율(%)'] = df_kospi['종가'].pct_change() * 100

    df_kospi['볼린저밴드_상단'] = df_kospi['종가'].rolling(window=20).mean() + 2 * df_kospi['종가'].rolling(window=20).std()
    df_kospi['볼린저밴드_하단'] = df_kospi['종가'].rolling(window=20).mean() - 2 * df_kospi['종가'].rolling(window=20).std()

    df_kospi['거래량'] = df_kospi['종가'].diff().abs()  # 거래량은 종가의 차이로 계산

    df_kospi['날짜'] = pd.to_datetime(df_kospi['날짜'])  # '날짜' 컬럼 이름은 실제 컬럼명에 맞춰 수정
    
    df_kospi['요일'] = df_kospi['날짜'].dt.dayofweek  # 월: 0, 일: 6
    df_kospi = pd.get_dummies(df_kospi, columns=['요일'], drop_first=True)

    #df_kospi = pd.concat([df_kospi, pd.DataFrame(['요일'])], ignore_index=True)

    #특정 변수
    features = [
        '종가', '거래량', 
        '이동평균_3일', '이동평균_5일', 
        '전일_대비_변화율(%)', 
        '볼린저밴드_상단', '볼린저밴드_하단', 
    ]
    target = '이동평균_5일' #예측 목표값

    #결측치 제거
    df_model = df_kospi.dropna(subset=features + [target])

    X = df_model[features]
    Y = df_model[target]

    #훈련 / 검증 분할
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, shuffle=False)

    #모델 선택 및 훈련
    if model_type == 'XGB':
        model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=6)
    elif model_type == 'lgb':
        model = LGBMRegressor(n_estimators=100, learning_rate=0.1, max_depth=6)
    else:
        raise ValueError('[알람] 모델 타입은 XGB 또는 lgb로 설정해야 합니다.')
    
    model.fit(X_train, Y_train)

    #예측 / 평가
    preds = model.predict(X_test)
    mse = mean_squared_error(Y_test, preds)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(Y_test, preds)
    Y_test_nonzero = Y_test.replace(0, np.nan)  # 0으로 나누는 것을 방지하기 위해 0을 NaN으로 대체
    mape = (abs((Y_test_nonzero - preds) / Y_test_nonzero) * 100).mean()

    print(f'[알람] {model_type.upper()} 모델 RMSE: {rmse:.2f}')
    print(f'[알람] {model_type.upper()} 모델 MAE: {mae:.2f}')
    print(f'[알람] {model_type.upper()} 모델 MAPE: {mape:.2f} \n')

    #시각화
    '''plt.plot(Y_test.values, label='실제값')
    plt.plot(preds, label='예측값')
    plt.legend()
    plt.title(f'{model_type.upper()} 모델 예측 결과')
    plt.show()'''

    print('\n')
    
    #무한 루프로 인해 주석 처리
    print("\n [알람] XGBoost 모델 학습 및 평가")
    #df_kospi, model_xgb, X_test_xgb, Y_test_xgb, preds_xgb = kospi_model_upgrade(df_kospi, model_type='XGB')

    print("\n [알람] LightGBM 모델 학습 및 평가")
    #_, model_lgb, X_test_lgb, Y_test_lgb, preds_lgb = kospi_model_upgrade(df_kospi, model_type='lgb')

    print('\n')

    return df_kospi, {
        'model' : model,
        'X_test' : X_test,
        'Y_test' : Y_test,
        'preds' : preds,
        'rmse' : rmse,
        'mae' : mae,
        'mape' : mape
    }

def visualize_graph(df_kospi, result_xgb, result_lgb):
    df_kospi = bollinger_kospi(df_kospi)

    #시각화
    plt.figure(figsize=(14, 7))
    plt.plot(result_xgb['Y_test'].values, label='실제값 (XGB)', color='blue')
    plt.plot(result_xgb['preds'], label='예측값 (XGB)', color='orange', linestyle='--')
    plt.plot(result_lgb['preds'], label='예측값 (LGB)', color='green', linestyle=':')
    plt.title('코스피 지수 예측 비교 : XGBoost vs LightGBM')
    plt.xlabel('샘플')
    plt.ylabel('종가')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
