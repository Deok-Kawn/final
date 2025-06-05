# 📊 EDA (Exploratory Data Analysis) 

시계열 전력수급 데이터의 탐색적 데이터 분석을 위한 전용 디렉토리입니다.

## 🎯 목적

- 시계열 전력수급 데이터의 구조와 특성 파악
- 데이터 품질 검증 및 전처리 방향 결정
- 패턴 및 트렌드 분석을 통한 모델링 인사이트 도출
- 시각화를 통한 데이터 이해도 향상

## 📁 파일 구조

### 🔍 데이터 검증 단계
- **`01_data_loading_and_validation.py`** - 데이터 로딩 및 기본 검증
  - CSV 데이터 로딩 및 인코딩 처리
  - 기본 데이터 구조 확인
  - 누락값, 중복값 검사
  - 날짜 컬럼 식별 및 검증
  - 환경 호환성 확인 (Python 3.6.9)

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

## 🚀 실행 순서

### 1. 환경 설정
```bash
# Python 3.6.9 환경에서 실행 권장
python --version

# 필요한 라이브러리 설치
pip install pandas numpy matplotlib seaborn scipy
```

### 2. 순차 실행
```bash
# 1단계: 데이터 로딩 및 검증
python 01_data_loading_and_validation.py

# 2단계: 기본 통계 분석
python 02_basic_statistical_summary.py

# 3단계: 시각화 생성
python 03_time_series_visualization.py
```

### 3. 코랩 환경에서 실행
```python
# 각 파일을 .py에서 .ipynb로 변환하거나
# 코드 블록별로 셀에 복사하여 실행
%run 01_data_loading_and_validation.py
%run 02_basic_statistical_summary.py
%run 03_time_series_visualization.py
```

## 📋 출력 결과

### 생성되는 파일들
- **`outputs/01_timeseries_overview.png`** - 전체 시계열 개요
- **`outputs/02_yearly_analysis.png`** - 연도별 분석
- **`outputs/03_seasonal_patterns.png`** - 계절성 패턴
- **`outputs/04_outliers_events.png`** - 이상값 분석
- **`outputs/05_decomposition.png`** - 시계열 분해
- **`outputs/06_distributions.png`** - 분포 분석

### 주요 인사이트
- **데이터 기간**: 2005-2023년 (약 19년간)
- **계절성**: 겨울 > 여름 > 가을 > 봄 순 전력수요
- **요일 패턴**: 평일 > 주말 전력수요
- **장기 트렌드**: 지속적인 상승 패턴
- **이상값**: IQR 방법으로 극값 탐지

## 🎯 다음 단계

EDA 완료 후 다음 분석 단계로 진행:

1. **Feature Engineering** (`notebooks/preprocessing/`)
   - 시간 기반 파생변수 생성
   - 계절성 변수 추가
   - 라그 변수 및 이동평균 생성

2. **시계열 모델링** (`notebooks/modeling/`)
   - ARIMA, SARIMA 모델
   - 머신러닝 기반 예측 모델
   - 딥러닝 시계열 모델 (LSTM, GRU)

3. **모델 평가** (`notebooks/evaluation/`)
   - 예측 성능 평가
   - 잔차 분석
   - 교차검증

## 🔧 문제 해결

### 일반적인 이슈들

**1. 데이터 파일을 찾을 수 없음**
```python
# 데이터 파일 경로 확인
import os
print("현재 경로:", os.getcwd())
print("파일 목록:", os.listdir('.'))
```

**2. 인코딩 오류**
```python
# 여러 인코딩 시도
encodings = ['utf-8', 'euc-kr', 'cp949', 'utf-8-sig']
```

**3. 한글 폰트 이슈**
```python
# matplotlib 한글 폰트 설정
plt.rcParams['font.family'] = ['Arial Unicode MS', 'DejaVu Sans']
```

**4. 메모리 부족**
```python
# 데이터 타입 최적화
df = df.astype({'컬럼명': 'float32'})  # float64 → float32
```

## 📞 지원

- **Issues**: GitHub Issues에 문제 보고
- **문서**: `docs/COLAB_GUIDE.md` 참조
- **팀 규칙**: 팀원은 `member/` 폴더에서 작업, EDA 결과는 참조용으로 활용

---
*Last Updated: 2024-01-01*
*Python Version: 3.6.9*
*Team: Time Series Forecasting Team* 