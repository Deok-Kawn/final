# 📊 EDA (Exploratory Data Analysis) 

시계열 전력수급 데이터의 탐색적 데이터 분석을 위한 전용 디렉토리입니다.

## 🎯 목적

- 시계열 전력수급 데이터의 구조와 특성 파악
- 데이터 품질 검증 및 전처리 방향 결정
- 패턴 및 트렌드 분석을 통한 모델링 인사이트 도출
- 시각화를 통한 데이터 이해도 향상
- 외부 요인 및 특별 이벤트가 전력 수요에 미치는 영향 분석

## 📁 파일 구조

### 🔍 데이터 검증 단계
- **`01_data_loading_and_validation.py`** - 데이터 로딩 및 기본 검증
  - CSV 데이터 로딩 및 인코딩 처리
  - 기본 데이터 구조 확인
  - 누락값, 중복값 검사
  - 날짜 컬럼 식별 및 검증
  - 환경 호환성 확인

### 📈 통계 분석 단계
- **`02_basic_statistical_summary.py`** - 기본 통계 요약 생성
  - 기술통계량 계산 (평균, 표준편차, 분위수 등)
  - 연도별/월별/요일별 패턴 분석
  - 계절성 분석 (봄, 여름, 가을, 겨울)
  - 이상값 탐지 (IQR, Z-score 방법)
  - 시계열 연속성 확인

### 📊 시각화 단계
- **`03_time_series_visualization.py`** - 시계열 시각화 차트 생성
  - 전체 시계열 개요 플롯
  - 연도별 상세 분석 차트
  - 계절성 및 주기적 패턴 시각화
  - 이상값 및 특별 이벤트 하이라이트
  - 시계열 분해 분석 (추세, 계절성, 잔차)
  - 분포 및 확률밀도 분석

### 📈 상관관계 분석 단계
- **`04_correlation_analysis.py`** - 상관관계 분석 및 피처 엔지니어링
  - 30개 파생 변수 생성 (시간 기반, 래그, 이동평균, 변화율 등)
  - 전체 및 주요 변수 상관관계 히트맵
  - 전력 수요와의 상관관계 막대그래프
  - 시간/래그 변수 산점도 분석
  - 상관관계 매트릭스 CSV 저장

### ❓ 누락값 분석 단계
- **`05_missing_values_analysis.py`** - 누락값 상세 분석
  - 26개 누락값 패턴 분석
  - 연도별/월별/요일별 누락값 분포
  - 누락값 시각화 및 권장 처리 방법
- **`05b_check_missing_dates.py`** - 누락된 날짜 확인
  - 완전히 빠진 날짜 식별
  - 2005년 초반 집중된 16개 누락일 분석

### 🔬 고급 시계열 분석 단계
- **`06_advanced_timeseries_analysis.py`** - 정상성 검정 & 자기상관 분석
  - ADF Test & KPSS Test (정상성 검정)
  - ACF/PACF 분석 (ARIMA 파라미터 결정용)
  - 1차/2차/계절 차분 비교 분석
  - 장기 계절성 자기상관 분석
  - ARIMA 모델 파라미터 권장

### 🌟 외부 요인 분석 단계
- **`07_external_factors_analysis.py`** - 외부 요인 및 특별 이벤트 분석
  - 291개 한국 공휴일 정보 생성 (2005-2023)
  - 공휴일별 전력 수요 영향 분석 (추석 -29.1% 최대)
  - 특별 이벤트 분석 (올림픽, 대선, 경제위기 등)
  - 계절별 전력 수요 패턴 분석
  - 경제 지표 프록시 변수 생성

### 🚀 실행 도구
- **`run_all_eda.py`** - 전체 EDA 스크립트 일괄 실행
  - 순차적 실행 및 오류 처리
  - 진행상황 모니터링
  - 결과 요약 리포트

## 🚀 실행 순서

### 1. 환경 설정
```bash
# 가상환경 활성화 (권장)
source venv/bin/activate  # Linux/Mac
# 또는 
venv\Scripts\activate  # Windows

# 필요한 라이브러리 설치
pip install -r requirements.txt
```

### 2. 개별 실행
```bash
# 순차적으로 실행
python 01_data_loading_and_validation.py
python 02_basic_statistical_summary.py
python 03_time_series_visualization.py
python 04_correlation_analysis.py
python 05_missing_values_analysis.py
python 05b_check_missing_dates.py
python 06_advanced_timeseries_analysis.py
python 07_external_factors_analysis.py
```

### 3. 일괄 실행
```bash
# 모든 EDA 스크립트를 한 번에 실행
python run_all_eda.py
```

### 4. 코랩 환경에서 실행
```python
# 각 파일을 순차적으로 실행
%run 01_data_loading_and_validation.py
%run 02_basic_statistical_summary.py
%run 03_time_series_visualization.py
%run 04_correlation_analysis.py
%run 05_missing_values_analysis.py
%run 06_advanced_timeseries_analysis.py
%run 07_external_factors_analysis.py
```

## 📋 출력 결과

### 카테고리별 결과 폴더 (`results/eda/`)
- **`01_basic_eda/`** (7개 파일) - 기본 EDA 시각화
- **`02_correlation_analysis/`** (7개 파일) - 상관관계 분석 결과
- **`03_missing_values/`** (2개 파일) - 누락값 분석 결과
- **`04_advanced_timeseries/`** (4개 파일) - 고급 시계열 분석 결과
- **`05_external_factors/`** (3개 파일) - 외부 요인 분석 결과

### 주요 생성 파일들
```
results/eda/
├── 01_basic_eda/
│   ├── 01_timeseries_overview.png
│   ├── 02_yearly_analysis.png
│   ├── 03_seasonal_patterns.png
│   ├── 04_outliers_events.png
│   ├── 05_decomposition.png
│   ├── 06_distributions.png
│   └── basic_statistics_overview.png
├── 02_correlation_analysis/
│   ├── correlation_heatmap_full.png
│   ├── correlation_heatmap_main.png
│   ├── correlation_barplot.png
│   ├── lag_variables_scatter.png
│   ├── time_variables_scatter.png
│   ├── correlation_matrix.csv
│   └── power_correlations.csv
├── 03_missing_values/
│   ├── missing_values_analysis.png
│   └── missing_values_report.txt
├── 04_advanced_timeseries/
│   ├── stationarity_comparison.png
│   ├── autocorrelation_analysis.png
│   ├── seasonal_autocorrelation.png
│   └── advanced_timeseries_analysis_report.txt
└── 05_external_factors/
    ├── external_factors_analysis.png
    ├── special_events_impact.png
    └── external_factors_analysis_report.txt
```

## 📊 주요 발견사항

### 📈 데이터 기본 특성
- **기간**: 2005-2023년 (19년간, 6,926일)
- **누락값**: 26개 (완전히 빠진 날짜)
- **평균 전력수요**: 62,337 MW
- **최대 전력수요**: 91,747 MW (2022-12-21)

### 🕒 시간적 패턴
- **계절성**: 겨울(67,438MW) > 여름(65,204MW) > 가을(60,351MW) > 봄(58,782MW)
- **요일 패턴**: 평일(65,925MW) > 주말(56,638MW) > 공휴일(54,335MW)
- **공휴일 영향**: 추석(-29.1%), 어린이날(-20.7%) 등 공휴일별 차별화

### 📊 상관관계 분석
- **높은 상관관계**: 래그 변수들 (lag_1: 0.98, lag_7: 0.92)
- **계절성 변수**: cos_day_of_year(0.18), 계절 더미 변수들
- **시간 변수**: 연도(0.41), 월별 패턴 확인

### 🔬 시계열 특성
- **정상성**: 1차 차분 후 완전 정상성 확보 (d=1)
- **ARIMA 권장**: 초기 모델 ARIMA(1,1,1)
- **계절성**: 강한 연간 주기 패턴 확인

### 🌟 외부 요인
- **공휴일 효과**: 평일 대비 17.6% 감소
- **특별 이벤트**: 2020 도쿄 올림픽(+18.1%) 최대 증가
- **경제 주기**: 2010년(+9.0%) 최고 성장, 2020년(-2.6%) 코로나19 영향

## 🎯 다음 단계 권장사항

### 1. 데이터 전처리 (Task 3)
- 26개 누락값 보간 (선형보간 또는 계절성 고려)
- 외부 요인 변수 생성 (공휴일, 특별이벤트 더미)
- 피처 엔지니어링 (래그, 이동평균, 계절성 변수)

### 2. 모델링 전략
- **ARIMA/SARIMA**: d=1, 초기 파라미터 (1,1,1)
- **머신러닝**: 30개 파생변수 활용
- **외부 회귀변수**: 공휴일, 계절, 경제지표 포함

### 3. 평가 전략
- 시계열 교차검증 적용
- 계절성 고려한 평가 지표
- 외부 요인 효과 검증

## 🔧 문제 해결

### 일반적인 이슈들

**1. 가상환경 활성화**
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

**2. 패키지 설치 오류**
```bash
# requirements.txt 설치
pip install -r requirements.txt

# 개별 설치
pip install pandas numpy matplotlib seaborn statsmodels scipy
```

**3. 한글 폰트 이슈 (Mac)**
```python
# matplotlib 한글 폰트 설정
plt.rcParams['font.family'] = ['Arial Unicode MS', 'AppleGothic']
```

**4. 메모리 최적화**
```python
# 데이터 타입 최적화
df = df.astype({'최대전력(MW)': 'float32'})
```

## 📞 지원

- **TaskMaster**: 작업 진행상황 추적
- **Issues**: 문제 발생 시 팀 리더에게 보고
- **문서**: `docs/TEAM_LEADER_SETUP.md` 참조

---
*Last Updated: 2025-06-06*
*Python Version: 3.10+*
*Team: Time Series Forecasting Team - Deep Learning Competition*
*TaskMaster Tasks: 2.1-2.7 완료* 