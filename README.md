# 🔮 시계열 예측 대회 - 일별 최대 전력 수요 예측

> 2005-2023년 일별 최대 전력 데이터를 기반으로 2024년 1월 1일부터 2025년 6월 10일까지 527일간의 전력 수요를 예측하는 머신러닝 프로젝트

## 📋 프로젝트 개요

- **목표**: 일별 최대 전력 수요 예측 (527일)
- **평가 지표**: RMSE (Root Mean Square Error)
- **개발 환경**: Python 3.6.9
- **실행 환경**: 서버 Python 3.6.9 (default, Jan 26 2021, 15:33:00) [GCC 8.4.0]

## 🗂️ 프로젝트 구조

```
📦 시계열 예측 프로젝트
├── 📁 data/                      # 데이터 파일
│   ├── 일별최대전력수급(2005-2023).csv
│   └── submission_sample.csv
├── 📁 notebooks/                 # Jupyter 노트북
│   ├── 00_quick_start_guide.ipynb    # 🚀 팀원용 빠른 시작 가이드
│   ├── 01_data_loading_and_validation.py
│   ├── 02_basic_statistical_summary.py
│   └── 03_time_series_visualization.py
├── 📁 src/                       # 소스 코드 모듈
│   ├── 📁 data/                  # 데이터 처리
│   │   ├── __init__.py
│   │   └── loader.py            # 데이터 로딩 유틸리티
│   ├── 📁 features/              # 특성 엔지니어링
│   │   ├── __init__.py
│   │   └── engineering.py       # 시계열 특성 생성
│   ├── 📁 models/                # 머신러닝 모델
│   │   ├── __init__.py
│   │   ├── base_model.py        # 베이스 모델 클래스
│   │   └── lstm_model.py        # LSTM 구현
│   └── 📁 utils/                 # 유틸리티
│       ├── __init__.py
│       └── experiment_tracker.py # 실험 추적 시스템
├── 📁 models/                    # 학습된 모델 저장
├── 📁 experiments/               # 실험 로그 및 결과
├── 📁 docs/                      # 프로젝트 문서
│   └── TEAM_GUIDELINES.md       # 팀 협업 가이드라인
├── 📁 .github/                   # GitHub 템플릿
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md
├── 📄 requirements_python36.txt  # 라이브러리 요구사항
├── 📄 test_environment.py       # 환경 테스트 스크립트
├── 📄 .gitignore                # Git 무시 파일 (딥러닝 최적화)
└── 📄 README.md
```

## 🔧 환경 설정

### 1. 환경 테스트
```bash
# 현재 환경에서 라이브러리 확인
python test_environment.py
```

### 2. 라이브러리 설치 (Python 3.6.9용)
```bash
# requirements 파일로 일괄 설치
pip install -r requirements_python36.txt

# 또는 개별 설치
pip install pandas==1.1.5 numpy==1.19.5
pip install scikit-learn==0.23.2
pip install torch==1.7.1 torchvision==0.8.2
pip install matplotlib==3.3.4 seaborn==0.11.2 plotly==4.14.3
pip install statsmodels==0.12.2 fbprophet==0.7.1
pip install optuna==2.10.1
```

### 3. GPU 설정 (선택사항)
```python
import torch
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
```

## 🌟 구글 코랩에서 시작하기

### ⚡ 원클릭 셋업 (권장)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

**📋 [전체 가이드는 여기 클릭!](https://github.com/Deok-Kawn/final/issues/2)**

구글 코랩에서 새 노트북 → 첫 번째 셀에 복사-붙여넣기 → 실행(1-2분):

```python
# 🚀 시계열 예측 프로젝트 - 원클릭 셋업
import os, subprocess, sys, requests

def run_cmd(cmd, desc=""):
    if desc: print(f"📋 {desc}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ 성공: {desc or cmd}")
            return True
        else:
            print(f"❌ 실패: {desc or cmd}")
            return False
    except Exception as e:
        print(f"❌ 예외: {e}")
        return False

print("🚀 시계열 예측 프로젝트 셋업 시작")

# 환경 정리 → 다운로드 → 압축해제 → Git 설정 → 라이브러리 설치 → 완료!
# (전체 코드는 위 링크에서 확인)
```

### 📅 일일 작업 루틴

**🌅 작업 시작:**
```python
%cd /content/final
!git pull origin main
```

**🌙 작업 완료:**
```python
!git add notebooks/member/본인이름_*.ipynb
!git commit -m "본인이름: 오늘 작업 설명"
!git push origin main
```

> 📊 **일일 보고**: [Daily Report 템플릿](https://github.com/Deok-Kawn/final/issues/new/choose) 사용  
> 🆘 **문제 해결**: [원클릭 셋업 가이드](https://github.com/Deok-Kawn/final/issues/2) 참조

## 📊 데이터 정보

- **학습 데이터**: 일별최대전력수급(2005-2023).csv
- **기간**: 2005-01-01 ~ 2023-12-31 (약 6,940일, 누락 가능)
- **예측 기간**: 2024-01-01 ~ 2025-06-10 (527일)
- **특징**: 일부 일자 누락 가능성 있음

## 🚀 개발 로드맵

### Phase 1: 환경 설정 및 팀 협업 📋
- [x] 개발 환경 설정
- [x] Git 워크플로우 및 가이드라인 구축
- [x] 프로젝트 구조 완성
- [x] 실험 추적 시스템 구축
- [ ] 팀원 온보딩 완료

### Phase 2: 데이터 분석 및 전처리 📊
- [ ] 데이터 로딩 및 EDA
- [ ] 누락 데이터 처리
- [ ] 기본 전처리 파이프라인
- [ ] 특성 엔지니어링 (시간, 래그, 롤링)

### Phase 3: 베이스라인 모델 개발 🎯
- [ ] 이동평균 베이스라인
- [ ] 선형회귀 모델
- [ ] 기본 LSTM 모델
- [ ] 모델 평가 시스템 구축

### Phase 4: 고급 모델 구현 🧠
- [ ] 개선된 LSTM/GRU 모델
- [ ] Transformer 기반 모델
- [ ] 통계 모델 (ARIMA, Prophet)
- [ ] 하이퍼파라미터 최적화

### Phase 5: 앙상블 및 최적화 🔧
- [ ] 모델 앙상블 전략
- [ ] 교차 검증 시스템
- [ ] 성능 최적화
- [ ] 최종 모델 선정

### Phase 6: 제출 준비 📤
- [ ] 최종 예측 생성
- [ ] 성능 분석 리포트
- [ ] 코드 정리 및 문서화
- [ ] 팀 발표 준비

## 🧪 모델 성능 목표

| 모델 유형 | 예상 RMSE | 설명 |
|---------|----------|------|
| 베이스라인 | > 1000 | 이동평균, 선형회귀 |
| LSTM | 800-1000 | 기본 딥러닝 모델 |
| 고급 모델 | 600-800 | GRU, Transformer |
| 앙상블 | < 600 | 최적화된 다중 모델 |

## 📈 핵심 라이브러리 버전

- **Python**: 3.6.9 (2021년 1월)
- **PyTorch**: 1.7.1 (딥러닝)
- **Pandas**: 1.1.5 (데이터 처리)
- **NumPy**: 1.19.5 (수치 계산)
- **Scikit-learn**: 0.23.2 (머신러닝)
- **Prophet**: 0.7.1 (시계열 예측)
- **Optuna**: 2.10.1 (하이퍼파라미터 최적화)

## ⚠️ 중요 주의사항

1. **Python 3.6 제한**: Python 3.6은 2021년 12월 지원 종료
2. **버전 호환성**: 명시된 라이브러리 버전 사용 권장
3. **메모리 관리**: 시계열 데이터 크기 고려한 배치 처리
4. **GPU 메모리**: 모델 크기에 따른 배치 크기 조정

## 🔗 참고 자료

- [PyTorch 1.7.1 Documentation](https://pytorch.org/docs/1.7.1/)
- [Prophet Documentation](https://facebook.github.io/prophet/)
- [Optuna Documentation](https://optuna.readthedocs.io/en/v2.10.1/)

## 📝 라이센스

이 프로젝트는 시계열 예측 대회용으로 개발되었습니다. 