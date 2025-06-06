#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
고급 시계열 분석: 정상성 검정 & 자기상관 분석
TaskMaster 작업 2.6: Advanced Time Series Analysis - Stationarity and Autocorrelation

ARIMA 모델 파라미터 결정을 위한 시계열 특성 분석
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = ['Arial Unicode MS', 'AppleGothic', 'Malgun Gothic']
plt.rcParams['axes.unicode_minus'] = False

def load_and_prepare_data():
    """데이터 로딩 및 전처리"""
    print("📊 데이터 로딩 및 전처리...")
    
    # 데이터 로딩
    df = pd.read_csv('data/shared/data.csv')
    
    # 날짜 변환 및 정렬
    df['date'] = pd.to_datetime(df['date'], format='%Y.%m.%d')
    df = df.sort_values('date').reset_index(drop=True)
    
    # 인덱스를 날짜로 설정
    df.set_index('date', inplace=True)
    
    # 시계열 데이터 추출
    ts = df['최대전력(MW)']
    
    print(f"✅ 데이터 준비 완료: {len(ts)}개 데이터 포인트")
    print(f"📅 기간: {ts.index[0].strftime('%Y-%m-%d')} ~ {ts.index[-1].strftime('%Y-%m-%d')}")
    
    return ts

def adf_test(timeseries, title='ADF Test'):
    """Augmented Dickey-Fuller Test 수행"""
    print(f"\n🔍 {title} 수행 중...")
    
    # ADF 테스트 실행
    result = adfuller(timeseries.dropna(), autolag='AIC')
    
    # 결과 출력
    print('📈 ADF Statistic:', f"{result[0]:.6f}")
    print('📊 p-value:', f"{result[1]:.6f}")
    print('🔢 Critical Values:')
    for key, value in result[4].items():
        print(f'\t{key}: {value:.3f}')
    
    # 해석
    if result[1] <= 0.05:
        conclusion = "✅ 시계열이 정상적(stationary)입니다 (귀무가설 기각)"
        is_stationary = True
    else:
        conclusion = "❌ 시계열이 비정상적(non-stationary)입니다 (귀무가설 채택)"
        is_stationary = False
    
    print(f"💡 결론: {conclusion}")
    
    return {
        'statistic': result[0],
        'pvalue': result[1],
        'critical_values': result[4],
        'is_stationary': is_stationary,
        'conclusion': conclusion
    }

def kpss_test(timeseries, title='KPSS Test'):
    """KPSS Test 수행"""
    print(f"\n🔍 {title} 수행 중...")
    
    # KPSS 테스트 실행
    result = kpss(timeseries.dropna(), regression='c', nlags='auto')
    
    # 결과 출력
    print('📈 KPSS Statistic:', f"{result[0]:.6f}")
    print('📊 p-value:', f"{result[1]:.6f}")
    print('🔢 Critical Values:')
    for key, value in result[3].items():
        print(f'\t{key}: {value:.3f}')
    
    # 해석 (KPSS는 ADF와 반대)
    if result[1] <= 0.05:
        conclusion = "❌ 시계열이 비정상적(non-stationary)입니다 (귀무가설 기각)"
        is_stationary = False
    else:
        conclusion = "✅ 시계열이 정상적(stationary)입니다 (귀무가설 채택)"
        is_stationary = True
    
    print(f"💡 결론: {conclusion}")
    
    return {
        'statistic': result[0],
        'pvalue': result[1],
        'critical_values': result[3],
        'is_stationary': is_stationary,
        'conclusion': conclusion
    }

def analyze_stationarity(ts):
    """정상성 종합 분석"""
    print("\n" + "="*50)
    print("🔬 시계열 정상성 종합 분석")
    print("="*50)
    
    # 원본 데이터 테스트
    print("\n📊 원본 데이터 정상성 검정:")
    adf_original = adf_test(ts, "원본 데이터 ADF Test")
    kpss_original = kpss_test(ts, "원본 데이터 KPSS Test")
    
    # 1차 차분 데이터 테스트
    diff1 = ts.diff().dropna()
    print("\n📊 1차 차분 데이터 정상성 검정:")
    adf_diff1 = adf_test(diff1, "1차 차분 ADF Test")
    kpss_diff1 = kpss_test(diff1, "1차 차분 KPSS Test")
    
    # 2차 차분 데이터 테스트
    diff2 = diff1.diff().dropna()
    print("\n📊 2차 차분 데이터 정상성 검정:")
    adf_diff2 = adf_test(diff2, "2차 차분 ADF Test")
    kpss_diff2 = kpss_test(diff2, "2차 차분 KPSS Test")
    
    # 계절 차분 (365일) 테스트
    seasonal_diff = ts.diff(365).dropna()
    print("\n📊 계절 차분 (365일) 데이터 정상성 검정:")
    adf_seasonal = adf_test(seasonal_diff, "계절 차분 ADF Test")
    kpss_seasonal = kpss_test(seasonal_diff, "계절 차분 KPSS Test")
    
    return {
        'original': {'adf': adf_original, 'kpss': kpss_original},
        'diff1': {'adf': adf_diff1, 'kpss': kpss_diff1},
        'diff2': {'adf': adf_diff2, 'kpss': kpss_diff2},
        'seasonal_diff': {'adf': adf_seasonal, 'kpss': kpss_seasonal}
    }

def plot_stationarity_comparison(ts):
    """정상성 변환 전후 비교 시각화"""
    print("\n📊 정상성 변환 시각화 생성 중...")
    
    # 차분 데이터 계산
    diff1 = ts.diff().dropna()
    diff2 = diff1.diff().dropna()
    seasonal_diff = ts.diff(365).dropna()
    
    # 시각화 생성
    fig, axes = plt.subplots(4, 2, figsize=(20, 16))
    
    # 원본 데이터
    axes[0, 0].plot(ts.index, ts.values, linewidth=1, color='blue')
    axes[0, 0].set_title('원본 시계열 데이터', fontsize=14, fontweight='bold')
    axes[0, 0].set_ylabel('전력 수요 (MW)')
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].hist(ts.values, bins=50, alpha=0.7, color='blue', edgecolor='black')
    axes[0, 1].set_title('원본 데이터 분포', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('전력 수요 (MW)')
    axes[0, 1].set_ylabel('빈도')
    axes[0, 1].grid(True, alpha=0.3)
    
    # 1차 차분
    axes[1, 0].plot(diff1.index, diff1.values, linewidth=1, color='green')
    axes[1, 0].set_title('1차 차분 데이터', fontsize=14, fontweight='bold')
    axes[1, 0].set_ylabel('전력 수요 변화량 (MW)')
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].hist(diff1.values, bins=50, alpha=0.7, color='green', edgecolor='black')
    axes[1, 1].set_title('1차 차분 분포', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('전력 수요 변화량 (MW)')
    axes[1, 1].set_ylabel('빈도')
    axes[1, 1].grid(True, alpha=0.3)
    
    # 2차 차분
    axes[2, 0].plot(diff2.index, diff2.values, linewidth=1, color='red')
    axes[2, 0].set_title('2차 차분 데이터', fontsize=14, fontweight='bold')
    axes[2, 0].set_ylabel('전력 수요 변화량 (MW)')
    axes[2, 0].grid(True, alpha=0.3)
    
    axes[2, 1].hist(diff2.values, bins=50, alpha=0.7, color='red', edgecolor='black')
    axes[2, 1].set_title('2차 차분 분포', fontsize=14, fontweight='bold')
    axes[2, 1].set_xlabel('전력 수요 변화량 (MW)')
    axes[2, 1].set_ylabel('빈도')
    axes[2, 1].grid(True, alpha=0.3)
    
    # 계절 차분
    axes[3, 0].plot(seasonal_diff.index, seasonal_diff.values, linewidth=1, color='purple')
    axes[3, 0].set_title('계절 차분 (365일) 데이터', fontsize=14, fontweight='bold')
    axes[3, 0].set_ylabel('전력 수요 변화량 (MW)')
    axes[3, 0].set_xlabel('날짜')
    axes[3, 0].grid(True, alpha=0.3)
    
    axes[3, 1].hist(seasonal_diff.values, bins=50, alpha=0.7, color='purple', edgecolor='black')
    axes[3, 1].set_title('계절 차분 분포', fontsize=14, fontweight='bold')
    axes[3, 1].set_xlabel('전력 수요 변화량 (MW)')
    axes[3, 1].set_ylabel('빈도')
    axes[3, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/eda/stationarity_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ 정상성 비교 시각화 저장: stationarity_comparison.png")

def analyze_autocorrelation(ts):
    """자기상관 분석 (ACF/PACF)"""
    print("\n" + "="*50)
    print("📈 자기상관 함수 (ACF/PACF) 분석")
    print("="*50)
    
    # 1차 차분 데이터로 분석 (대부분의 경우 정상성 확보)
    diff1 = ts.diff().dropna()
    
    # ACF/PACF 시각화
    fig, axes = plt.subplots(3, 2, figsize=(20, 15))
    
    # 원본 데이터 ACF/PACF
    plot_acf(ts.dropna(), ax=axes[0, 0], lags=40, title='원본 데이터 ACF')
    plot_pacf(ts.dropna(), ax=axes[0, 1], lags=40, title='원본 데이터 PACF')
    
    # 1차 차분 ACF/PACF
    plot_acf(diff1, ax=axes[1, 0], lags=40, title='1차 차분 ACF')
    plot_pacf(diff1, ax=axes[1, 1], lags=40, title='1차 차분 PACF')
    
    # 계절 차분 ACF/PACF (처음 365일 이후부터)
    seasonal_diff = ts.diff(365).dropna()
    if len(seasonal_diff) > 40:
        plot_acf(seasonal_diff, ax=axes[2, 0], lags=40, title='계절 차분 ACF')
        plot_pacf(seasonal_diff, ax=axes[2, 1], lags=40, title='계절 차분 PACF')
    else:
        axes[2, 0].text(0.5, 0.5, '계절 차분 데이터 부족', ha='center', va='center', 
                        transform=axes[2, 0].transAxes, fontsize=14)
        axes[2, 1].text(0.5, 0.5, '계절 차분 데이터 부족', ha='center', va='center', 
                        transform=axes[2, 1].transAxes, fontsize=14)
    
    plt.tight_layout()
    plt.savefig('results/eda/autocorrelation_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ 자기상관 분석 시각화 저장: autocorrelation_analysis.png")

def seasonal_autocorrelation_analysis(ts):
    """계절성 자기상관 분석"""
    print("\n📊 계절성 자기상관 분석...")
    
    # 계절성 분석을 위한 긴 래그 ACF
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))
    
    # 원본 데이터의 긴 래그 ACF (최대 2년)
    plot_acf(ts.dropna(), ax=axes[0], lags=min(730, len(ts)//4), 
             title='장기 자기상관 함수 (ACF) - 계절성 패턴 확인')
    
    # 1차 차분 데이터의 긴 래그 ACF
    diff1 = ts.diff().dropna()
    plot_acf(diff1, ax=axes[1], lags=min(730, len(diff1)//4), 
             title='1차 차분 장기 자기상관 함수 (ACF)')
    
    plt.tight_layout()
    plt.savefig('results/eda/seasonal_autocorrelation.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ 계절성 자기상관 분석 저장: seasonal_autocorrelation.png")

def recommend_arima_parameters(stationarity_results):
    """ARIMA 파라미터 권장사항 도출"""
    print("\n" + "="*50)
    print("🎯 ARIMA 모델 파라미터 권장사항")
    print("="*50)
    
    # 차분 차수 (d) 결정
    if stationarity_results['original']['adf']['is_stationary'] and stationarity_results['original']['kpss']['is_stationary']:
        d_recommendation = 0
        print("📌 차분 차수 (d): 0 - 원본 데이터가 이미 정상적")
    elif stationarity_results['diff1']['adf']['is_stationary'] and stationarity_results['diff1']['kpss']['is_stationary']:
        d_recommendation = 1
        print("📌 차분 차수 (d): 1 - 1차 차분 후 정상성 확보")
    elif stationarity_results['diff2']['adf']['is_stationary'] and stationarity_results['diff2']['kpss']['is_stationary']:
        d_recommendation = 2
        print("📌 차분 차수 (d): 2 - 2차 차분 후 정상성 확보")
    else:
        d_recommendation = 1
        print("📌 차분 차수 (d): 1 - 일반적인 권장사항 (추가 검토 필요)")
    
    # 계절 차분 권장사항
    if stationarity_results['seasonal_diff']['adf']['is_stationary'] and stationarity_results['seasonal_diff']['kpss']['is_stationary']:
        seasonal_recommendation = "계절 차분 고려 (D=1, s=365)"
        print("📌 계절성 차분: 권장 - 계절 차분 후 정상성 확보")
    else:
        seasonal_recommendation = "계절 차분 불필요하거나 추가 검토 필요"
        print("📌 계절성 차분: 불필요하거나 추가 검토 필요")
    
    # ACF/PACF 분석 가이드라인
    print("\n📊 ACF/PACF 분석 가이드라인:")
    print("🔹 ACF가 천천히 감소하면 → AR 성분 필요 (p > 0)")
    print("🔹 ACF가 특정 래그에서 급격히 끊어지면 → MA 성분 (q 결정)")
    print("🔹 PACF가 천천히 감소하면 → MA 성분 필요 (q > 0)")
    print("🔹 PACF가 특정 래그에서 급격히 끊어지면 → AR 성분 (p 결정)")
    
    # 일반적인 시작점 권장
    print(f"\n🎯 권장 시작 파라미터:")
    print(f"   ARIMA(p={1}, d={d_recommendation}, q={1}) 부터 시작")
    print(f"   계절성: {seasonal_recommendation}")
    print(f"   추가 고려사항: SARIMA(p,d,q)(P,D,Q,s) 모델 검토")
    
    return {
        'd_recommendation': d_recommendation,
        'seasonal_recommendation': seasonal_recommendation,
        'suggested_start': f"ARIMA(1,{d_recommendation},1)"
    }

def generate_analysis_report(ts, stationarity_results, arima_recommendations):
    """종합 분석 보고서 생성"""
    print("\n📝 종합 분석 보고서 생성 중...")
    
    report = f"""
=== 🔬 고급 시계열 분석 보고서 ===

📊 데이터 개요:
- 분석 기간: {ts.index[0].strftime('%Y년 %m월 %d일')} ~ {ts.index[-1].strftime('%Y년 %m월 %d일')}
- 총 데이터 포인트: {len(ts):,}개
- 평균 전력 수요: {ts.mean():,.0f} MW
- 표준편차: {ts.std():,.0f} MW

🔍 정상성 검정 결과:

1. 원본 데이터:
   - ADF Test: p-value = {stationarity_results['original']['adf']['pvalue']:.6f}
     → {'정상적' if stationarity_results['original']['adf']['is_stationary'] else '비정상적'}
   - KPSS Test: p-value = {stationarity_results['original']['kpss']['pvalue']:.6f}
     → {'정상적' if stationarity_results['original']['kpss']['is_stationary'] else '비정상적'}

2. 1차 차분 데이터:
   - ADF Test: p-value = {stationarity_results['diff1']['adf']['pvalue']:.6f}
     → {'정상적' if stationarity_results['diff1']['adf']['is_stationary'] else '비정상적'}
   - KPSS Test: p-value = {stationarity_results['diff1']['kpss']['pvalue']:.6f}
     → {'정상적' if stationarity_results['diff1']['kpss']['is_stationary'] else '비정상적'}

3. 2차 차분 데이터:
   - ADF Test: p-value = {stationarity_results['diff2']['adf']['pvalue']:.6f}
     → {'정상적' if stationarity_results['diff2']['adf']['is_stationary'] else '비정상적'}
   - KPSS Test: p-value = {stationarity_results['diff2']['kpss']['pvalue']:.6f}
     → {'정상적' if stationarity_results['diff2']['kpss']['is_stationary'] else '비정상적'}

4. 계절 차분 데이터:
   - ADF Test: p-value = {stationarity_results['seasonal_diff']['adf']['pvalue']:.6f}
     → {'정상적' if stationarity_results['seasonal_diff']['adf']['is_stationary'] else '비정상적'}
   - KPSS Test: p-value = {stationarity_results['seasonal_diff']['kpss']['pvalue']:.6f}
     → {'정상적' if stationarity_results['seasonal_diff']['kpss']['is_stationary'] else '비정상적'}

🎯 ARIMA 모델링 권장사항:

1. 차분 차수 (d): {arima_recommendations['d_recommendation']}
2. 계절성 처리: {arima_recommendations['seasonal_recommendation']}
3. 권장 시작 모델: {arima_recommendations['suggested_start']}

📈 ACF/PACF 분석 지침:
- autocorrelation_analysis.png 파일에서 ACF/PACF 패턴을 확인하여 p, q 값을 결정
- 1차 차분 데이터의 ACF/PACF가 모델 파라미터 결정에 가장 중요
- 계절성이 강한 경우 SARIMA 모델 고려

💡 추가 권장사항:
1. 모델 선택 시 AIC, BIC 기준으로 여러 파라미터 조합 비교
2. 잔차 분석을 통한 모델 적합성 검증 필수
3. 외부 변수(공휴일, 기온 등) 추가 고려 시 ARIMAX 모델 검토
4. 장기 예측 시 계절성 패턴의 안정성 확인

📁 생성된 시각화 파일:
- stationarity_comparison.png: 정상성 변환 전후 비교
- autocorrelation_analysis.png: ACF/PACF 분석
- seasonal_autocorrelation.png: 장기 계절성 자기상관 분석

분석 완료 시간: {pd.Timestamp.now().strftime('%Y년 %m월 %d일 %H시 %M분')}
"""
    
    # 보고서 저장
    with open('results/eda/advanced_timeseries_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("✅ 종합 분석 보고서 저장: advanced_timeseries_analysis_report.txt")
    print(report)

def main():
    """메인 실행 함수"""
    print("🚀 고급 시계열 분석 시작")
    print("=" * 70)
    
    try:
        # 1. 데이터 로딩
        ts = load_and_prepare_data()
        
        # 2. 정상성 분석
        stationarity_results = analyze_stationarity(ts)
        
        # 3. 정상성 시각화
        plot_stationarity_comparison(ts)
        
        # 4. 자기상관 분석
        analyze_autocorrelation(ts)
        
        # 5. 계절성 자기상관 분석
        seasonal_autocorrelation_analysis(ts)
        
        # 6. ARIMA 파라미터 권장사항
        arima_recommendations = recommend_arima_parameters(stationarity_results)
        
        # 7. 종합 보고서 생성
        generate_analysis_report(ts, stationarity_results, arima_recommendations)
        
        print("\n" + "=" * 70)
        print("🎉 고급 시계열 분석 완료!")
        print("📁 모든 결과가 'results/eda/' 폴더에 저장되었습니다.")
        print("🎯 ARIMA 모델링에 활용할 파라미터 권장사항이 준비되었습니다.")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        raise

if __name__ == "__main__":
    main() 