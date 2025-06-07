# Time Series Data Preprocessing Scripts

한국 전력 수요 시계열 데이터(2005-2023) 전처리를 위한 Python 스크립트 모음입니다.

## 📁 폴더 구성

```
preprocessing/                          # Python 스크립트만 저장
├── advanced_imputation.py              # 결측값 보간 (5가지 알고리즘 앙상블)
├── imputation_comparison_fixed.py      # 시각화 및 분석 도구
└── README.md                           # 이 파일
```

**결과물 저장 위치**: 모든 실행 결과는 `/results/preprocessing/` 폴더에 저장됩니다.

## 🔧 스크립트 설명

### 1. `advanced_imputation.py`
- **목적**: 결측값 보간 (26개 결측 날짜)
- **방법**: 5가지 알고리즘 가중 앙상블
  - 선형 보간 (10%), 스플라인 보간 (25%)
  - 계절 분해 보간 (30%), ARIMA 예측 (25%)
  - KNN 시간 특성 보간 (10%)
- **출력**: `results/preprocessing/final_imputed_dataset.csv`

### 2. `imputation_comparison_fixed.py`
- **목적**: 보간 결과 시각화 및 분석
- **기능**: 한글 폰트 자동 설정, 다중 패널 분석
- **출력**:
  - `results/preprocessing/imputation_comparison_korean.png`
  - `results/preprocessing/detailed_imputation_analysis.png`
  - `results/preprocessing/imputation_summary_report.txt`

## 🚀 실행 방법

### 1. 결측값 보간 실행
```bash
cd preprocessing/
python advanced_imputation.py
```

### 2. 시각화 및 보고서 생성
```bash
cd preprocessing/
python imputation_comparison_fixed.py
```

### 3. 전체 파이프라인 실행
```bash
cd preprocessing/
python advanced_imputation.py
python imputation_comparison_fixed.py
```

## 📊 데이터 흐름

```
원본 데이터 (data/shared/data.csv)
    ↓
advanced_imputation.py
    ↓
완전 데이터 (results/preprocessing/final_imputed_dataset.csv)
    ↓
imputation_comparison_fixed.py
    ↓
시각화 & 보고서 (results/preprocessing/)
```

## 📋 필요 라이브러리

```bash
pip install pandas numpy matplotlib scipy statsmodels scikit-learn
```

## 📈 결과 확인

실행 완료 후 결과 확인:
```bash
ls -la ../results/preprocessing/
```

**예상 결과물**:
- `final_imputed_dataset.csv` - 최종 데이터셋 (6,939행, 결측값 0개)
- `imputation_comparison_korean.png` - 한글 비교 차트
- `detailed_imputation_analysis.png` - 4패널 상세 분석
- `imputation_summary_report.txt` - 요약 보고서

---
*Time Series Preprocessing Pipeline - Python Scripts* 