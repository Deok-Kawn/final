# 📊 EDA 분석 결과 폴더 구조

이 폴더는 전력 수요 예측 프로젝트의 탐색적 데이터 분석(EDA) 결과들을 카테고리별로 정리한 곳입니다.

## 📁 폴더 구조

### 🔍 `01_basic_eda/` (7개 파일)
기본적인 시계열 데이터 탐색 및 시각화 결과
- `01_timeseries_overview.png` - 전체 시계열 데이터 개요
- `02_yearly_analysis.png` - 연도별 패턴 분석
- `03_seasonal_patterns.png` - 계절성 패턴 분석
- `04_outliers_events.png` - 이상치 및 특별 이벤트 분석
- `05_decomposition.png` - 시계열 분해 (트렌드, 계절성, 잔차)
- `06_distributions.png` - 데이터 분포 분석
- `basic_statistics_overview.png` - 기본 통계량 요약

### 📈 `02_correlation_analysis/` (7개 파일)
상관관계 분석 및 피처 엔지니어링 결과
- `correlation_heatmap_full.png` - 전체 변수 상관관계 히트맵
- `correlation_heatmap_main.png` - 주요 변수 상관관계 히트맵
- `correlation_barplot.png` - 전력 수요와의 상관관계 막대그래프
- `lag_variables_scatter.png` - 래그 변수 산점도 분석
- `time_variables_scatter.png` - 시간 변수 산점도 분석
- `correlation_matrix.csv` - 상관관계 매트릭스 (CSV)
- `power_correlations.csv` - 전력 수요 상관관계 (CSV)

### ❓ `03_missing_values/` (2개 파일)
누락값 분석 및 패턴 탐지 결과
- `missing_values_analysis.png` - 누락값 시각화 분석
- `missing_values_report.txt` - 누락값 상세 보고서

### 🔬 `04_advanced_timeseries/` (4개 파일)
고급 시계열 분석 및 ARIMA 모델링 준비 결과
- `stationarity_comparison.png` - 정상성 변환 전후 비교
- `autocorrelation_analysis.png` - ACF/PACF 분석 (ARIMA 파라미터 결정용)
- `seasonal_autocorrelation.png` - 장기 계절성 자기상관 분석
- `advanced_timeseries_analysis_report.txt` - 종합 분석 보고서

## 📋 분석 순서

1. **기본 EDA** (`01_basic_eda/`) → 데이터 이해 및 패턴 탐지
2. **상관관계 분석** (`02_correlation_analysis/`) → 피처 중요도 및 관계 파악
3. **누락값 분석** (`03_missing_values/`) → 데이터 품질 확인
4. **고급 시계열 분석** (`04_advanced_timeseries/`) → 모델링 준비

## 🎯 주요 발견사항

- **강한 계절성**: 여름/겨울 피크, 요일별 패턴 확인
- **26개 누락 날짜**: 2005년 초반 집중, 주로 주말/공휴일
- **높은 예측 가능성**: 래그 변수들과 높은 상관관계 (0.9+)
- **ARIMA 권장**: d=1, 시작 모델 ARIMA(1,1,1)

---
*분석 완료: 2025년 6월 6일*  
*TaskMaster Task 2: Data Loading and Initial EDA* 