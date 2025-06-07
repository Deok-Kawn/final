import pandas as pd
import numpy as np
from datetime import datetime
from scipy import interpolate
from scipy.stats import zscore
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

def load_data():
    """데이터 로드 및 전처리"""
    df = pd.read_csv('data/shared/data.csv')
    df['date'] = pd.to_datetime(df['date'], format='%Y.%m.%d')
    df = df.set_index('date').sort_index()
    df = df[~df.index.duplicated(keep='last')]
    
    # 전체 날짜 범위 생성
    start_date = df.index.min()
    end_date = df.index.max()
    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    missing_dates = all_dates.difference(df.index)
    
    return df, missing_dates, all_dates

def linear_interpolation(df, all_dates):
    """선형 보간"""
    df_reindexed = df.reindex(all_dates)
    df_reindexed['최대전력(MW)'] = df_reindexed['최대전력(MW)'].interpolate(method='linear')
    return df_reindexed['최대전력(MW)'].to_dict()

def spline_interpolation(df, all_dates):
    """스플라인 보간"""
    df_reindexed = df.reindex(all_dates)
    
    # 결측값이 아닌 데이터 포인트 추출
    valid_data = df_reindexed.dropna()
    valid_dates = valid_data.index
    valid_values = valid_data['최대전력(MW)'].values
    
    # 날짜를 숫자로 변환 (days since start)
    date_nums = [(date - valid_dates[0]).days for date in valid_dates]
    all_date_nums = [(date - valid_dates[0]).days for date in all_dates]
    
    # 스플라인 보간 수행
    spline_func = interpolate.UnivariateSpline(date_nums, valid_values, s=0, k=3)
    interpolated_values = spline_func(all_date_nums)
    
    result = {}
    for date, value in zip(all_dates, interpolated_values):
        result[date] = value
    
    return result

def seasonal_decomposition_imputation(df, all_dates, missing_dates):
    """계절 분해 기반 보간"""
    # 일주일 주기로 계절 분해 수행
    df_reindexed = df.reindex(all_dates)
    
    # 초기 선형 보간으로 계절 분해를 위한 연속 데이터 생성
    temp_data = df_reindexed['최대전력(MW)'].interpolate(method='linear')
    
    # 계절 분해 (주간 주기)
    decomposition = seasonal_decompose(temp_data, model='additive', period=7)
    
    # 트렌드, 계절성, 잔차 성분 추출
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    resid = decomposition.resid
    
    result = {}
    for date in missing_dates:
        # 트렌드 + 계절성으로 보간값 계산
        imputed_value = trend.loc[date] + seasonal.loc[date]
        
        # 잔차 성분은 주변값의 평균으로 보완
        nearby_residuals = resid.dropna()
        if len(nearby_residuals) > 0:
            imputed_value += nearby_residuals.mean()
        
        result[date] = imputed_value
    
    return result

def arima_forecasting_imputation(df, missing_dates):
    """ARIMA 예측 기반 보간"""
    result = {}
    
    for date in missing_dates:
        # 해당 날짜 이전의 데이터 사용
        before_data = df[df.index < date]['최대전력(MW)'].dropna()
        
        if len(before_data) >= 30:  # 최소 30일 데이터 필요
            try:
                # ARIMA 모델 적합
                model = ARIMA(before_data, order=(1, 1, 1))
                fitted_model = model.fit()
                
                # 1일 예측
                forecast = fitted_model.forecast(steps=1)
                result[date] = forecast[0]
                
            except Exception:
                # ARIMA 실패시 이동평균 사용
                window = min(7, len(before_data))
                result[date] = before_data.tail(window).mean()
        else:
            # 데이터 부족시 평균 사용
            result[date] = before_data.mean() if len(before_data) > 0 else df['최대전력(MW)'].mean()
    
    return result

def knn_time_aware_imputation(df, all_dates, missing_dates):
    """시간 특성 기반 KNN 보간"""
    # 완전한 데이터프레임 생성
    df_full = df.reindex(all_dates)
    
    # 시간 특성 생성
    df_full['year'] = df_full.index.year
    df_full['month'] = df_full.index.month
    df_full['day'] = df_full.index.day
    df_full['weekday'] = df_full.index.weekday
    df_full['day_of_year'] = df_full.index.dayofyear
    df_full['is_weekend'] = df_full.index.weekday.isin([5, 6]).astype(int)
    
    # 순환 특성 (원형 인코딩)
    df_full['month_sin'] = np.sin(2 * np.pi * df_full['month'] / 12)
    df_full['month_cos'] = np.cos(2 * np.pi * df_full['month'] / 12)
    df_full['weekday_sin'] = np.sin(2 * np.pi * df_full['weekday'] / 7)
    df_full['weekday_cos'] = np.cos(2 * np.pi * df_full['weekday'] / 7)
    
    # 특성 컬럼 선택
    feature_cols = ['year', 'month', 'day', 'weekday', 'day_of_year', 'is_weekend',
                   'month_sin', 'month_cos', 'weekday_sin', 'weekday_cos']
    
    # KNN 보간
    X = df_full[feature_cols + ['최대전력(MW)']].values
    
    # 스케일링
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # KNN 보간 수행
    imputer = KNNImputer(n_neighbors=7, weights='distance')
    X_imputed = imputer.fit_transform(X_scaled)
    
    # 원래 스케일로 변환
    X_final = scaler.inverse_transform(X_imputed)
    
    # 결과 추출
    result = {}
    for i, date in enumerate(df_full.index):
        if date in missing_dates:
            result[date] = X_final[i, -1]
    
    return result

def advanced_ensemble_imputation(df, all_dates, missing_dates):
    """고급 앙상블 보간 (여러 방법의 가중 결합)"""
    print("=== 고급 보간 방법별 처리 ===")
    
    # 1. 선형 보간
    print("1. 선형 보간...")
    linear_values = linear_interpolation(df, all_dates)
    
    # 2. 스플라인 보간
    print("2. 스플라인 보간...")
    spline_values = spline_interpolation(df, all_dates)
    
    # 3. 계절 분해 보간
    print("3. 계절 분해 보간...")
    seasonal_values = seasonal_decomposition_imputation(df, all_dates, missing_dates)
    
    # 4. ARIMA 예측 보간
    print("4. ARIMA 예측 보간...")
    arima_values = arima_forecasting_imputation(df, missing_dates)
    
    # 5. KNN 시간 특성 보간
    print("5. KNN 시간 특성 보간...")
    knn_values = knn_time_aware_imputation(df, all_dates, missing_dates)
    
    # 앙상블 결합 (가중 평균)
    print("6. 앙상블 결합...")
    final_values = {}
    
    for date in missing_dates:
        values = []
        weights = []
        
        # 각 방법의 결과 수집
        if date in linear_values and not np.isnan(linear_values[date]):
            values.append(linear_values[date])
            weights.append(0.1)  # 선형 보간 (낮은 가중치)
        
        if date in spline_values and not np.isnan(spline_values[date]):
            values.append(spline_values[date])
            weights.append(0.25)  # 스플라인 보간
        
        if date in seasonal_values and not np.isnan(seasonal_values[date]):
            values.append(seasonal_values[date])
            weights.append(0.3)  # 계절 분해 (높은 가중치)
        
        if date in arima_values and not np.isnan(arima_values[date]):
            values.append(arima_values[date])
            weights.append(0.25)  # ARIMA 예측
        
        if date in knn_values and not np.isnan(knn_values[date]):
            values.append(knn_values[date])
            weights.append(0.1)  # KNN (낮은 가중치)
        
        if values:
            # 가중 평균 계산
            final_values[date] = np.average(values, weights=weights[:len(values)])
        else:
            # 모든 방법 실패시 전체 평균
            final_values[date] = df['최대전력(MW)'].mean()
    
    return final_values, {
        'linear': linear_values,
        'spline': spline_values, 
        'seasonal': seasonal_values,
        'arima': arima_values,
        'knn': knn_values
    }

def evaluate_imputation_quality(df, imputed_values, missing_dates):
    """보간 품질 평가"""
    print("\n=== 보간 품질 평가 ===")
    
    # 1. 통계적 일관성 확인
    original_stats = df['최대전력(MW)'].describe()
    imputed_list = list(imputed_values.values())
    
    print(f"원본 데이터 평균: {original_stats['mean']:.1f} MW")
    print(f"보간값 평균: {np.mean(imputed_list):.1f} MW")
    print(f"원본 데이터 표준편차: {original_stats['std']:.1f} MW")
    print(f"보간값 표준편차: {np.std(imputed_list):.1f} MW")
    
    # 2. 이상값 탐지
    z_scores = np.abs(zscore(imputed_list))
    outliers = np.sum(z_scores > 3)
    print(f"이상값 개수 (|z-score| > 3): {outliers}")
    
    # 3. 주변값과의 일관성 확인
    consistency_scores = []
    for date in missing_dates:
        imputed_val = imputed_values[date]
        
        # 전후 일주일 데이터 확인
        week_before = df[df.index < date].tail(7)['최대전력(MW)']
        week_after = df[df.index > date].head(7)['최대전력(MW)']
        
        nearby_values = pd.concat([week_before, week_after])
        if len(nearby_values) > 0:
            nearby_mean = nearby_values.mean()
            nearby_std = nearby_values.std()
            
            # 정규화된 차이 계산
            if nearby_std > 0:
                consistency = abs(imputed_val - nearby_mean) / nearby_std
                consistency_scores.append(consistency)
    
    if consistency_scores:
        avg_consistency = np.mean(consistency_scores)
        print(f"주변값과의 일관성 점수: {avg_consistency:.2f} (낮을수록 좋음)")
    
    return {
        'original_mean': original_stats['mean'],
        'imputed_mean': np.mean(imputed_list),
        'original_std': original_stats['std'],
        'imputed_std': np.std(imputed_list),
        'outlier_count': outliers,
        'consistency_score': np.mean(consistency_scores) if consistency_scores else None
    }

def main():
    """메인 실행 함수"""
    print("=== 고급 시계열 결측값 보간 ===\n")
    
    # 1. 데이터 로드
    df, missing_dates, all_dates = load_data()
    
    print(f"원본 데이터: {len(df)} 행")
    print(f"결측 날짜: {len(missing_dates)} 개")
    print(f"\n결측 날짜 목록:")
    for date in sorted(missing_dates):
        print(f"  {date.strftime('%Y-%m-%d')}")
    
    # 2. 고급 앙상블 보간 수행
    final_values, method_results = advanced_ensemble_imputation(df, all_dates, missing_dates)
    
    # 3. 최종 데이터셋 생성
    print("\n=== 최종 데이터셋 생성 ===")
    df_complete = df.reindex(all_dates)
    
    for date, value in final_values.items():
        df_complete.loc[date, '최대전력(MW)'] = value
    
    print(f"최종 데이터 크기: {len(df_complete)} 행")
    print(f"결측값 개수: {df_complete['최대전력(MW)'].isnull().sum()}")
    
    # 4. 보간 품질 평가
    quality_metrics = evaluate_imputation_quality(df, final_values, missing_dates)
    
    # 5. 결과 상세 출력
    print(f"\n=== 보간 결과 상세 ===")
    for date in sorted(missing_dates):
        print(f"{date.strftime('%Y-%m-%d')}: {final_values[date]:.1f} MW")
    
    # 6. 파일 저장
    output_file = 'data/shared/electricity_data_advanced_imputed.csv'
    df_complete.reset_index().to_csv(output_file, index=False)
    print(f"\n고급 보간 데이터 저장: {output_file}")
    
    # 7. 통계 요약
    print(f"\n=== 최종 통계 ===")
    stats = df_complete['최대전력(MW)'].describe()
    print(f"평균: {stats['mean']:.1f} MW")
    print(f"최소: {stats['min']:.1f} MW")
    print(f"최대: {stats['max']:.1f} MW")
    print(f"표준편차: {stats['std']:.1f} MW")
    
    return df_complete, quality_metrics

if __name__ == "__main__":
    result, metrics = main()
    print("\n=== 고급 보간 작업 완료 ===") 