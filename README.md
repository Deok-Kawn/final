# 🔮 시계열 예측 프로젝트 - 일별 최대 전력 수요 예측

[![GitHub stars](https://img.shields.io/github/stars/Deok-Kawn/final?style=flat-square)](https://github.com/Deok-Kawn/final/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/Deok-Kawn/final?style=flat-square)](https://github.com/Deok-Kawn/final/issues)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-Latest-orange?style=flat-square)](https://pytorch.org/)
[![TaskMaster](https://img.shields.io/badge/TaskMaster-AI%20Powered-green?style=flat-square)](https://github.com/task-master-ai)

> **2005-2023년 일별 최대 전력 데이터를 기반으로 2024-2025년 527일간의 전력 수요를 예측하는 딥러닝 경진대회 프로젝트**

## 🎯 프로젝트 미션

**AI 기반 전력 수요 예측으로 효율적인 에너지 관리 시스템 구축**

- 📊 **데이터**: 19년간(2005-2023) 일별 최대 전력 수급 데이터 (6,926개 데이터 포인트)
- 🎯 **목표**: 527일간(2024.01.01-2025.06.10) 전력 수요 예측  
- 📈 **평가**: RMSE (Root Mean Square Error) 최소화
- 🏆 **목표 성능**: RMSE < 600 달성

## 👥 팀 구성 

### 🤝 **팀 협업 시스템**
- **일일 보고**: GitHub Issues 템플릿 활용
- **코드 공유**: Git을 통한 버전 관리
- **역할 분리**: `notebooks/member/` vs `notebooks/leader/`
- **AI 지원**: 실시간 코드 리뷰 및 최적화 제안

## 🏗️ 프로젝트 아키텍처

### 📂 **체계적인 폴더 구조**
```
📦 프로젝트 구조
├── 📁 eda/                    # 📊 탐색적 데이터 분석 (완료 ✅)
│   ├── 01_data_loading_and_validation.py      # 데이터 로딩 & 검증
│   ├── 02_basic_statistical_summary.py        # 기본 통계 분석
│   ├── 03_time_series_visualization.py        # 시계열 시각화
│   ├── 04_correlation_analysis.py             # 상관관계 분석
│   ├── 05_missing_values_analysis.py          # 누락값 분석
│   ├── 05b_check_missing_dates.py             # 누락 날짜 확인
│   ├── 06_advanced_timeseries_analysis.py     # 정상성 & 자기상관 분석
│   ├── 07_external_factors_analysis.py        # 외부 요인 분석
│   └── run_all_eda.py                         # EDA 통합 실행 스크립트
├── 📁 results/                 # 모든 실험 결과물 통합
│   └── 📊 eda/                 # EDA 결과 (카테고리별 정리)
│       ├── 01_basic_eda/       # 기본 EDA 시각화 (7개 파일)
│       ├── 02_correlation_analysis/  # 상관관계 분석 (7개 파일)
│       ├── 03_missing_values/  # 누락값 분석 (2개 파일)
│       ├── 04_advanced_timeseries/   # 고급 시계열 분석 (4개 파일)
│       └── 05_external_factors/      # 외부 요인 분석 (3개 파일)
├── 📁 notebooks/              # 개발 노트북
│   ├── 👥 member/             # 팀원 전용 실험 공간
│   └── 👑 leader/             # 리더 전용 관리 공간
├── 📁 trained_models/         # 훈련 완료된 모델 파일
│   ├── 👥 member/             # 팀원 훈련 모델
│   └── 👑 leader/             # 리더 훈련 모델
├── 📁 src/models/             # 모델 클래스 정의
├── 📁 tools/                  # 설정 및 도구 스크립트
├── 📁 data/shared/            # 공유 데이터셋
└── 📁 .taskmaster/            # TaskMaster AI 구성 파일
    ├── config.json            # AI 모델 설정
    └── tasks/                 # 작업 관리 파일
```

### 🛠️ **기술 스택**
- **AI 개발**: TaskMaster + Claude Sonnet 4 (메인), Perplexity Sonar Pro (리서치)
- **딥러닝**: PyTorch (LSTM, GRU, Transformer, Attention Models)
- **시계열 분석**: Statsmodels (ARIMA/SARIMA), Prophet, 정상성 검정
- **머신러닝**: Scikit-learn (앙상블, 회귀), XGBoost, LightGBM
- **최적화**: Optuna (하이퍼파라미터 튜닝), Ray Tune
- **데이터**: Pandas, NumPy, Polars (고성능 데이터프레임)
- **시각화**: Matplotlib, Seaborn, Plotly, Bokeh

## 🚀 빠른 시작

### 🌟 **개발 환경**
```bash
# 1. 저장소 클론
git clone https://github.com/Deok-Kawn/final.git
cd final

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows

# 3. EDA 패키지 설치
cd eda
pip install -r requirements.txt

# 4. 전체 EDA 실행 (한 번에!)
python run_all_eda.py
```

### 💻 **코랩 환경**
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

## 📈 개발 진행 상황 (TaskMaster 추적)

### ✅ **완료된 단계 (Tasks 1-2)**
- [x] **Task 1**: 프로젝트 초기화 - 환경 구축, 팀 협업 시스템
- [x] **Task 2**: 데이터 로딩 및 EDA 완료
  - [x] **Task 2.1**: 데이터 로딩 및 기본 검증
  - [x] **Task 2.2**: 기본 통계 요약 및 시각화
  - [x] **Task 2.3**: 시계열 패턴 시각화
  - [x] **Task 2.4**: 상관관계 분석 (30개 파생변수 생성)
  - [x] **Task 2.5**: 누락값 분석 (26개 누락일 식별)
  - [x] **Task 2.6**: 고급 시계열 분석 (정상성 검정, ARIMA 파라미터 도출)
  - [x] **Task 2.7**: 외부 요인 분석 (공휴일, 특별 이벤트 영향)

### 🔄 **진행 중인 단계 (Task 3)**
- [ ] **Task 3**: 데이터 전처리 파이프라인 (HIGH 우선순위)
  - [ ] 26개 누락값 보간 처리
  - [ ] 외부 요인 변수 생성 (공휴일, 특별이벤트 더미)
  - [ ] 피처 엔지니어링 (래그, 이동평균, 계절성 변수)
  - [ ] 정규화 및 스케일링
  - [ ] 훈련/검증/테스트 데이터 분할

### 🎯 **향후 계획 (Tasks 4+)**
- [ ] **Task 4**: 베이스라인 모델 구현 (ARIMA, 선형회귀)
- [ ] **Task 5**: 딥러닝 모델 개발 (LSTM, GRU)
- [ ] **Task 6**: 고급 모델 구현 (Transformer, Attention)
- [ ] **Task 7**: 하이퍼파라미터 최적화 (Optuna)
- [ ] **Task 8**: 앙상블 및 최종 모델
- [ ] **Task 9**: 모델 평가 및 검증
- [ ] **Task 10**: 최종 제출 및 문서화

## 🏆 성과 목표 & 현재 성과

### 📊 **모델 성능 로드맵**
| 단계 | 모델 | 목표 RMSE | 현재 상태 |
|------|------|-----------|-----------|
| 1단계 | 베이스라인 (ARIMA) | < 1000 | ⏳ Task 4 |
| 2단계 | LSTM/GRU | < 800 | ⏳ Task 5 |
| 3단계 | Transformer | < 700 | ⏳ Task 6 |
| 4단계 | 앙상블 | **< 600** | ⏳ Task 8 |

### 🎖️ **현재까지의 성과**
- ✅ **완전한 EDA 분석**: 7개 주요 분석 완료, 23개 시각화 파일 생성
- ✅ **AI 기반 개발 시스템**: TaskMaster + Claude Sonnet 4 활용
- ✅ **체계적인 데이터 이해**: 계절성, 트렌드, 외부 요인 영향 파악
- ✅ **모델링 준비**: ARIMA(1,1,1) 파라미터 도출, 30개 파생변수 생성
- ✅ **자동화된 워크플로우**: 원클릭 EDA 실행 시스템

## 📊 데이터 분석 결과

### 📈 **핵심 데이터 특성 (EDA 완료)**
- **기간**: 2005.01.01 ~ 2023.12.31 (19년간, 6,926일)
- **누락값**: 26개 완전 누락일 (주로 2005년 초반)
- **평균 전력수요**: 62,337 MW
- **최대 전력수요**: 91,747 MW (2022-12-21)

### 🕒 **발견된 패턴**
- **계절성**: 겨울(67,438MW) > 여름(65,204MW) > 가을(60,351MW) > 봄(58,782MW)
- **요일 패턴**: 평일(65,925MW) > 주말(56,638MW) > 공휴일(54,335MW)
- **공휴일 영향**: 추석(-29.1%), 어린이날(-20.7%) 등 공휴일별 차별화
- **특별 이벤트**: 2020 도쿄 올림픽(+18.1%) 최대 증가

### 🔬 **시계열 특성 분석**
- **정상성**: 1차 차분 후 완전 정상성 확보 (ARIMA d=1)
- **자기상관**: 강한 일간 및 주간 패턴 확인
- **ARIMA 권장**: 초기 모델 ARIMA(1,1,1)
- **외부 회귀변수**: 공휴일, 계절, 경제지표 유의미

### 🎯 **모델링 인사이트**
- **핵심 변수**: lag_1(0.98), lag_7(0.92), 계절성 변수들
- **전처리 방향**: 누락값 계절성 보간, 공휴일 더미변수 생성
- **모델 전략**: ARIMA + 회귀변수, LSTM 장기의존성 활용
- **평가 전략**: 시계열 교차검증, 계절성 고려 평가

## 💡 핵심 기술 및 접근법

### 🧠 **딥러닝 모델**
- **LSTM**: 장기 의존성 학습 (계절성 패턴 캡처)
- **GRU**: 효율적인 순환 신경망 (메모리 효율성)
- **Transformer**: 어텐션 메커니즘 (복잡한 패턴 학습)
- **CNN-LSTM**: 1D 컨볼루션 + LSTM 하이브리드

### 📊 **통계 모델**
- **ARIMA/SARIMA**: EDA 결과 기반 파라미터 (1,1,1)
- **Prophet**: 공휴일 효과 및 계절성 자동 처리
- **지수 평활법**: Holt-Winters 삼중 지수 평활
- **VAR**: 벡터 자기회귀 (다변량 시계열)

### 🔧 **고급 특성 엔지니어링**
- **시간 특성**: 요일, 월, 계절, 공휴일 더미 (291개 공휴일 DB)
- **래그 특성**: 1일, 7일, 30일, 365일 래그 변수
- **롤링 통계**: 다양한 윈도우 이동평균, 표준편차
- **외부 변수**: 특별 이벤트, 경제 위기, 팬데믹 더미
- **상호작용**: 계절×요일, 공휴일×계절 상호작용 항

### 🤖 **AI 기반 개발**
- **자동 피처 생성**: AI 지원 변수 생성 및 선택
- **하이퍼파라미터 최적화**: Optuna + AI 추천
- **모델 아키텍처 탐색**: Neural Architecture Search
- **실험 추적**: MLflow + TaskMaster 통합

## 🤝 기여 및 참여

### 👨‍💻 **팀원으로 참여**
1. **환경 설정**: 상단 빠른 시작 가이드 따라하기
2. **EDA 결과 확인**: `results/eda/` 폴더에서 분석 결과 검토
3. **작업 공간**: `notebooks/member/` 폴더에서 실험
4. **TaskMaster 활용**: AI 기반 작업 관리 시스템 활용
5. **일일 보고**: GitHub Issues를 통한 진행상황 공유

### 🌟 **기여 방법**
- **새로운 모델 아이디어** 제안 및 구현
- **EDA 인사이트 활용** 모델 개발
- **외부 데이터** 통합 아이디어
- **성능 개선** 실험 및 최적화
- **AI 기반 자동화** 도구 개발

### 💬 **소통 채널**
- **GitHub Issues**: 버그 리포트, 기능 요청
- **TaskMaster**: AI 기반 작업 관리 및 추적
- **Team Discussion**: 프로젝트 관련 논의
- **EDA Results**: `results/eda/README.md` 참조

### 🆘 **지원 요청**
문제가 발생하면 GitHub Issues에 문의하세요!
- **EDA 관련**: `eda/README.md` 문제해결 섹션 참조
- **환경 설정**: 가상환경 및 패키지 설치 문제
- **TaskMaster**: AI 모델 설정 및 API 키 문제
- **데이터 분석**: EDA 결과 해석 및 활용

---

## 📄 라이센스

이 프로젝트는 딥러닝 경진대회 및 시계열 예측 연구 목적으로 개발되었습니다.

**🤖 Powered by TaskMaster AI + Claude Sonnet 4**

