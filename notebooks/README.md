# 📓 Notebooks 폴더 - 전체 구조 안내

이 폴더는 **프로젝트의 모든 노트북과 실험 관련 파일**을 체계적으로 관리합니다.

## 📁 폴더 구조

```
📁 notebooks/
├── 📁 leader/                 # 팀 리더 전용 모델 실험
├── 📁 member/                 # 팀원 전용 모델 실험  
├── 📁 setup/                  # 환경 설정 스크립트
├── 📄 00_quick_start_guide.ipynb  # 프로젝트 빠른 시작 가이드
└── 📄 README.md               # 이 파일
```

## 🎯 각 폴더의 역할

### 📊 ../eda/ - 데이터 탐색 및 분석 (상위 폴더)
- **목적**: 데이터 이해 및 전처리를 위한 탐색적 분석
- **대상**: 모든 팀원 (모델 작업 전 필수 실행)
- **파일**: Python 스크립트 형태 (순차 실행)
- **위치**: 프로젝트 루트의 `eda/` 폴더
- **결과물**: `outputs/` 폴더에 저장

### 👨‍💼 leader/ - 팀 리더 전용 실험
- **목적**: 팀 리더가 담당하는 모델 개발 및 실험
- **대상**: 팀 리더만 사용
- **파일**: Jupyter 노트북 (.ipynb)
- **결과물**: `results/leader/`에 저장, 완성된 모델은 `trained_models/leader/`에 이동

### 👥 member/ - 팀원 전용 실험  
- **목적**: 팀원이 담당하는 모델 개발 및 실험
- **대상**: 팀원만 사용 (구글 코랩 연동)
- **파일**: Jupyter 노트북 (.ipynb)
- **결과물**: `results/member/`에 저장, 완성된 모델은 `trained_models/member/`에 이동

## 🚀 작업 순서 (권장)

### 1️⃣ 프로젝트 시작
```bash
# 빠른 시작 가이드 확인
jupyter notebook 00_quick_start_guide.ipynb
```

### 2️⃣ 데이터 탐색 (필수)
```bash
cd ../eda/
python 01_data_loading_and_validation.py
python 02_basic_statistical_summary.py  
python 03_time_series_visualization.py
```

### 3️⃣ 모델 개발 (역할 분담)
- **팀 리더**: `leader/` 폴더에서 모델 실험
- **팀원**: `member/` 폴더에서 모델 실험 (구글 코랩)

## 📋 파일 명명 규칙

### 모델 실험 노트북
```
model_[모델명]_v[버전].ipynb
analysis_[분석주제]_v[버전].ipynb

예시:
- model_lstm_v1.ipynb
- model_transformer_v2.ipynb  
- analysis_hyperparameter_tuning_v1.ipynb
```

### 실험 결과 파일
```
[YYYY-MM-DD]_[모델명]_results.csv
[YYYY-MM-DD]_[모델명]_predictions.csv

예시:
- 2024-01-15_lstm_results.csv
- 2024-01-15_transformer_predictions.csv
```

## 🔄 협업 워크플로우

### 일일 작업
1. **최신 코드 동기화** (`git pull`)
2. **담당 폴더에서 작업** (`leader/` 또는 `member/`)
3. **결과 저장 및 업로드** (`git push`)
4. **GitHub Issues에 진행상황 보고**

### 주간 리뷰
1. **EDA 결과 공유 및 토론**
2. **모델 성능 비교 및 분석**
3. **다음 주 실험 계획 수립**
4. **베스트 모델 선정**

## ⚠️ 주의사항

- **EDA는 모든 팀원이 완료한 후** 모델 작업을 시작하세요
- **자신의 담당 폴더에서만** 작업하여 충돌을 방지하세요
- **결과물은 지정된 폴더에** 저장하여 체계적으로 관리하세요
- **정기적으로 GitHub에 업로드**하여 진행상황을 공유하세요 