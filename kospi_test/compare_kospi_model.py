from kospi_XGBClassifier import kospi_model_upgrade
import matplotlib.pyplot as plt

def compare_kospi_model(df_kospi):
    #XGBoost 모델 학습 및 평가
    print("\n [알람] XGBoost 모델 학습 및 평가")
    model_xgb, X_test_xgb, Y_test_xgb, preds_xgb = kospi_model_upgrade(df_kospi, model_type='XGB')

    #LightGBM 모델 학습 및 평가
    print("\n [알람] LightGBM 모델 학습 및 평가")
    model_lgb, X_test_lgb, Y_test_lgb, preds_lgb = kospi_model_upgrade(df_kospi, model_type='lgb')

    #모델 성능 비교
    plt.figure(figsize=(12, 6))
    plt.plot(Y_test_xgb.values, label='실제 종가 (5일 후)', color='blue', linewidth=2)
    plt.plot(preds_xgb, label='XGBoost 예측', color='orange', linestyle='--')
    plt.plot(preds_lgb, label='LightGBM 예측', color='green', linestyle=':')
    plt.title('코스피 지수 예측 비교 : XGBoost와 LightGBM')
    plt.xlabel('샘플 순서')
    plt.ylabel('시간')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print('\n')

    return {
        'XGBoost': {
            'model': model_xgb,
            'X_test': X_test_xgb,
            'Y_test': Y_test_xgb,
            'preds': preds_xgb
        },
        'LightGBM': {
            'model': model_lgb,
            'X_test': X_test_lgb,
            'Y_test': Y_test_lgb,
            'preds': preds_lgb
        }
    }