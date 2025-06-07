# 01. Missing Value Imputation (결측값 보간)

한국 전력 수요 시계열 데이터의 결측값 보간 처리를 위한 스크립트입니다.

## 📋 작업 개요

- **목적**: 26개 결측 날짜의 전력 수요값 보간
- **대상 기간**: 2005-01-01 ~ 2023-12-31
- **결측값**: 26개 → 0개 (100% 해결)

## 🐍 스크립트 구성

### 1. `advanced_imputation.py`
- **기능**: 고급 결측값 보간 실행
- **방법**: 5가지 알고리즘 가중 앙상블
  - Linear Interpolation (10%)
  - Spline Interpolation (25%)
  - Seasonal Decomposition (30%) - 주요 방법
  - ARIMA Forecasting (25%)
  - Time-aware KNN (10%)

### 2. `imputation_comparison_fixed.py`
- **기능**: 보간 결과 시각화 및 분석
- **특징**: 한글 폰트 자동 설정
- **출력**: 비교 차트, 상세 분석, 요약 보고서

## 🚀 실행 방법

```bash
# 1. 결측값 보간 실행
python advanced_imputation.py

# 2. 시각화 및 분석 생성
python imputation_comparison_fixed.py
```

## 📊 결과 확인

실행 후 결과물은 `results/preprocessing/01_missing_value_imputation/`에 저장됩니다:

- `final_imputed_dataset.csv` - 최종 데이터셋
- `imputation_comparison_korean.png` - 비교 차트
- `detailed_imputation_analysis.png` - 상세 분석
- `imputation_summary_report.txt` - 요약 보고서

## 📈 품질 지표

- **완전성**: 100% (결측값 0개)
- **시간적 일관성**: 우수
- **이상값**: 0개 (검증 통과)

---
*Step 1: Missing Value Imputation* 