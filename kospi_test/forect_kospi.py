import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

from kospi_ratio import ratio_kospi

#랜덤포레스트를 이용한 예측 모델
def randomforest_kospi(df_kospi):
    #상승/하락 예측 모델 개선 (RandomForest 사용)
    #결측값 처리
    # 사용 피처 + 타깃 열 포함한 데이터프레임
    df_kospi_model_data = df_kospi[['종가', '3일_이동평균', '5일_이동평균', '3일_표준편차', '날짜', '상승여부']].dropna()

    # 피처와 타깃 분리
    #.copy() 데이터 프레임 안정성 확보
    df_kospi_x = df_kospi_model_data.drop(columns='상승여부').copy()
    df_kospi_y = df_kospi_model_data['상승여부'].copy()
    #SettingWithCopyWarring 발생 위험 방지
    #복사한 결과에 바로 스케일링, 인코딩 처리 가능

    # 수치형 피처 스케일링
    scaled_columns = ['종가', '3일_이동평균', '5일_이동평균', '3일_표준편차']
    scaler = StandardScaler()
    df_kospi_x[scaled_columns] = scaler.fit_transform(df_kospi_x[scaled_columns])

    # 범주형 요일 one-hot 인코딩
    df_kospi_x = pd.get_dummies(df_kospi_x)

    #학습 데이터를 넣을 때 datetime64 타입(날짜형 데이터)이 포함되어 있는지 확인
    if '날짜' in df_kospi_x.columns:
        df_kospi_x = df_kospi_x.drop(columns=['날짜'])
    #데이터 프레임에 날짜열이 있는 걸 알 때, 명시적으로 제거하고 싶을 때 사용

    #일반적으로 datetime64 타입 열을 모두 제거
    df_kospi_x = df_kospi_x.select_dtypes(exclude=['datetime64[ns]', 'datetime64[ns, UTC]'])
    '''
    select_dtypes() : 특정 타입의 열만 선택하거나 제외할 수 있는 함수
    exclude=['datetime64[ns]'] : 날짜형 타입 열을 전부 제외하겠다는 뜻
    날짜 열 이름을 모를 때, 전체에서 자동으로 제거하고 싶을 때 유용
    '''

    # 훈련/테스트 분할
    X_train, X_test, y_train, y_test = train_test_split(df_kospi_x, df_kospi_y, test_size=0.2, shuffle=False)

    #랜덤포레스트 모델 생성 및 학습
    df_kospi_model = RandomForestClassifier()
    df_kospi_model.fit(X_train, y_train)

    #에측 결과 리포트 출력 (정확도, 정밀도, 재현율 등)
    print(classification_report(y_test, df_kospi_model.predict(X_test)))
    #RandomForestClassifier는 여러 개의 결정 트리를 모아서 예측 정확도를 높이는 모델
    #여기서는 상승/하락 예측에 사용되며, 이동평균, 변동성, 요일 같은 변수들이 예측에 기여

    #모델 성능 로그 (정확도, feature importance)
    #정확도 확인
    y_pred = df_kospi_model.predict(X_test)
    print(f'정확도 : ', accuracy_score(y_test, y_pred))

    #어떤 변수가 예측에 많이 기여했는지 확인
    importances = df_kospi_model.feature_importances_
    feature_names = X_test.columns
    df_kospi_importances = pd.DataFrame({'특징' : feature_names, '중요도' : importances})
    print(df_kospi_importances.sort_values(by='중요도', ascending=False))

    return df_kospi
