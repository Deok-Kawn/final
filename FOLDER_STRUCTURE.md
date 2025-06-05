# 📁 프로젝트 폴더 구조 가이드

> **명확하고 직관적인 폴더 구성으로 팀 협업의 효율성을 극대화합니다**

## 🎯 **정리된 폴더 구조**

```
📦 final/
├── 📊 eda/                     # 데이터 탐색적 분석 (모든 팀원)
│   ├── 01_data_loading_and_validation.py
│   ├── 02_basic_statistical_summary.py
│   ├── 03_time_series_visualization.py
│   ├── run_all_eda.py
│   └── README.md
│
├── 💻 notebooks/               # 모델 실험 및 분석 노트북
│   ├── leader/                 # 팀 리더 전용 실험
│   ├── member/                 # 팀원 전용 실험 (코랩 연동)
│   ├── 00_quick_start_guide.ipynb
│   └── README.md
│
├── 🧠 src/                     # 소스 코드 및 라이브러리
│   ├── models/                 # 모델 클래스 정의
│   ├── utils/                  # 유틸리티 함수
│   └── __init__.py
│
├── 📊 data/                    # 데이터 관리
│   └── shared/                 # 팀 공유 데이터셋
│       ├── data.csv
│       ├── full_data.csv
│       └── submission_sample.csv
│
├── 📈 results/                 # 모든 실험 결과물
│   ├── eda/                    # EDA 시각화 결과
│   ├── leader/                 # 리더 실험 결과
│   │   └── predictions/        # 예측 결과
│   └── member/                 # 팀원 실험 결과
│       └── predictions/        # 예측 결과
│
├── 🤖 trained_models/          # 훈련 완료된 모델 파일
│   ├── leader/                 # 리더가 훈련한 모델
│   └── member/                 # 팀원이 훈련한 모델
│
├── 🛠️ tools/                   # 도구 및 설정 스크립트
│   ├── setup/                  # 환경 설정 파일들
│   ├── setup_environment.py    # 환경 자동 설정
│   └── test_environment.py     # 환경 테스트
│
└── 📋 docs/                    # 문서 및 가이드
    ├── progress_reports/       # 진행상황 보고서
    ├── GETTING_STARTED.md
    └── TEAM_LEADER_SETUP.md
```

## 🎨 **폴더별 역할과 사용법**

### 📊 **`eda/` - 데이터 탐색적 분석**
- **목적**: 데이터 이해 및 패턴 분석
- **사용자**: 모든 팀원 (필수 실행)
- **파일 형태**: Python 스크립트 (.py)
- **결과 저장**: `results/eda/`

```bash
# 실행 방법
cd eda/
python run_all_eda.py
```

### 💻 **`notebooks/` - 모델 실험**
- **목적**: 개별 모델 개발 및 실험
- **구분**: `leader/` (리더 전용), `member/` (팀원 전용)
- **파일 형태**: Jupyter 노트북 (.ipynb)
- **결과 저장**: `results/leader/`, `results/member/`

### 🧠 **`src/` - 소스 코드**
- **목적**: 재사용 가능한 코드 라이브러리
- **src/models/**: 모델 클래스 정의 (BaseModel, LSTMModel 등)
- **src/utils/**: 공통 유틸리티 함수
- **특징**: 노트북에서 `from src.models import LSTMModel`로 사용

### 📊 **`data/shared/` - 공유 데이터**
- **목적**: 팀 전체가 사용하는 원본 데이터
- **파일**: CSV 형태의 시계열 데이터
- **접근**: 모든 스크립트에서 상대경로로 접근

### 📈 **`results/` - 실험 결과 통합**
- **목적**: 모든 분석 및 실험 결과물 저장
- **구조**: 
  - `eda/`: EDA 시각화 이미지
  - `leader/`: 리더 실험 결과 (CSV, 이미지, 로그)
  - `member/`: 팀원 실험 결과 (CSV, 이미지, 로그)
  - `predictions/`: 예측 결과 전용 하위폴더

### 🤖 **`trained_models/` - 훈련된 모델**
- **목적**: 완성된 모델 가중치 및 체크포인트 저장
- **파일 형태**: .pth, .pkl, .h5 등
- **명명 규칙**: `[모델명]_[날짜]_[성능].pth`

### 🛠️ **`tools/` - 도구 및 설정**
- **목적**: 프로젝트 관리 및 환경 설정
- **포함**: 환경 설정, 테스트, 코랩 연동 스크립트
- **사용**: 프로젝트 초기 설정 시에만 사용

## 📋 **파일 명명 규칙**

### 노트북 파일
```
model_[모델명]_v[버전].ipynb
analysis_[주제]_v[버전].ipynb

예시:
- model_lstm_v1.ipynb
- model_transformer_v2.ipynb
- analysis_hyperparameter_tuning_v1.ipynb
```

### 결과 파일
```
[YYYY-MM-DD]_[모델명]_[결과타입].csv
[YYYY-MM-DD]_[실험명]_[결과타입].png

예시:
- 2024-01-15_lstm_predictions.csv
- 2024-01-15_model_comparison_chart.png
```

### 모델 파일
```
[모델명]_[YYYY-MM-DD]_rmse[성능].pth

예시:
- lstm_2024-01-15_rmse_650.pth
- transformer_2024-01-16_rmse_580.pth
```

## 🔄 **작업 워크플로우**

### 1️⃣ **프로젝트 시작**
```bash
# 1. EDA 실행 (필수)
cd eda/
python run_all_eda.py

# 2. 결과 확인
ls -la results/eda/
```

### 2️⃣ **모델 실험**
```bash
# 각자 담당 폴더에서 작업
# 리더: notebooks/leader/
# 팀원: notebooks/member/ (코랩에서)
```

### 3️⃣ **결과 관리**
```bash
# 실험 결과는 자동으로 results/ 하위에 저장
# 완성된 모델은 trained_models/에 수동 이동
```

## ⚠️ **중요 규칙**

### ✅ **DO (권장사항)**
- 자신의 담당 폴더에서만 작업
- 결과물은 지정된 폴더에 저장
- 파일 명명 규칙 준수
- 정기적인 Git 동기화

### ❌ **DON'T (금지사항)**
- 다른 팀원의 폴더에서 작업
- 임의의 위치에 파일 저장
- 공유 데이터 수정
- 대용량 파일의 Git 커밋

## 🆘 **문제 해결**

### Q: 폴더가 없다고 나옵니다
```bash
# 필요한 폴더 자동 생성
mkdir -p results/leader/predictions
mkdir -p results/member/predictions
mkdir -p trained_models/leader
mkdir -p trained_models/member
```

### Q: import 오류가 발생합니다
```python
# 프로젝트 루트에서 실행하세요
import sys
sys.path.append('.')
from src.models import LSTMModel
```

### Q: 결과 파일을 찾을 수 없습니다
```python
# 절대 경로 대신 상대 경로 사용
result_path = 'results/leader/predictions/my_results.csv'
```

---

**🎯 이 구조를 따르면 팀 협업이 훨씬 효율적이고 명확해집니다!** 