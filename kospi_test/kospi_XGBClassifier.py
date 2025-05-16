from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from kospi_bollinger_bands import bollinger_kospi

#코스피 지수 예측 – XGBoost / LightGBM
def kospi_model_upgrade(df_kospi, model_type='XGB'):
    #데이터 전처리
    df_kospi = bollinger_kospi(df_kospi)

    #특정 변수
    features = [
        '종가', '거래량', 
        '종가_3일후', '종가_5일후', 
        '이동평균_3일', '이동평균_5일', 
        '전일대비등락율', 
        '볼린저밴드_상단', '볼린저밴드_하단', 
        '요일'
    ]
    target = '종가_5일후' #예측 목표값

    #결측치 제거
    df_model = df_kospi.dropna(subset=features + [target])

    X = df_model[features]
    Y = df_model[target]

    #훈련 / 검증 분할
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, shuffle=False)

    #모델 선택 및 훈련
    if model_type == 'XGB':
        model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=42)
    elif model_type == 'lgb':
        model = LGBMRegressor(n_estimators=100, learning_rate=0.1, max_depth=42)
    else:
        raise ValueError('[알람] 모델 타입은 XGB 또는 lgb로 설정해야 합니다.')
    
    model.fit(X_train, Y_train)

    #예측 / 평가
    preds = model.predict(X_test)
    mse = mean_squared_error(Y_test, preds)
    rmse = mean_squared_error(Y_test, preds, squared=False)

    print(f'[알람] {model_type.upper()} 모델 RMSE: {rmse:.2f} \n')

    return model, X_test, Y_test, preds
