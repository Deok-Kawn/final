# Task Master - Python 3.8.20 환경 설정 가이드

## 개요

Task Master 프로젝트가 Python 3.8.20 환경에서 실행되도록 설정되었습니다.

## 설정된 환경 정보

- **Python 버전**: 3.8.20
- **Conda 환경명**: `taskmaster_py38`
- **환경 위치**: `/opt/anaconda3/envs/taskmaster_py38`

## 주요 설치된 패키지

| 패키지 | 버전 | 용도 |
|--------|------|------|
| pandas | 1.5.3 | 데이터 처리 |
| numpy | 1.24.4 | 수치 계산 |
| torch | 1.13.1 | 딥러닝 |
| torchvision | 0.14.1 | 컴퓨터 비전 |
| scikit-learn | 1.2.2 | 머신러닝 |
| matplotlib | 3.7.5 | 시각화 |
| seaborn | 0.12.2 | 통계 시각화 |
| plotly | 5.24.1 | 인터랙티브 시각화 |
| statsmodels | 0.14.1 | 통계 분석 |
| optuna | 3.6.2 | 하이퍼파라미터 최적화 |
| prophet | 1.1.7 | 시계열 예측 |
| jupyter | 1.1.1 | 노트북 환경 |

## 환경 사용 방법

### 1. 자동 환경 활성화

```bash
# 환경 설정 스크립트 실행
./python38_environment.sh
```

### 2. 수동 환경 활성화

```bash
# Conda 환경 활성화
conda activate taskmaster_py38

# Python 버전 확인
python --version
```

### 3. 환경 비활성화

```bash
conda deactivate
```

## 패키지 관리

### 새로운 패키지 설치

```bash
# 환경 활성화 후
conda activate taskmaster_py38

# pip를 사용하여 패키지 설치
/opt/anaconda3/envs/taskmaster_py38/bin/pip install <package_name>
```

### 설치된 패키지 목록 확인

```bash
# 환경 활성화 후
conda activate taskmaster_py38
pip list
```

## Task Master에서 Python 3.8 사용

Task Master에서 Python 3.8 환경을 사용하려면:

1. 터미널에서 `conda activate taskmaster_py38` 실행
2. 활성화된 환경에서 Task Master 관련 작업 수행
3. Python 스크립트나 Jupyter 노트북이 자동으로 Python 3.8.20을 사용

## 문제 해결

### 환경이 활성화되지 않는 경우

```bash
# Conda 초기화
conda init zsh  # 또는 bash

# 터미널 재시작 후 다시 시도
conda activate taskmaster_py38
```

### 패키지 설치 문제

```bash
# Conda 환경에서 pip 업그레이드
/opt/anaconda3/envs/taskmaster_py38/bin/pip install --upgrade pip

# 또는 conda로 패키지 설치 시도
conda install -c conda-forge <package_name>
```

### Python 버전 확인

```bash
# 현재 사용 중인 Python 경로와 버전 확인
which python
python --version

# 올바른 경로여야 함: /opt/anaconda3/envs/taskmaster_py38/bin/python
```

## 파일 구조

```
project_root/
├── requirements_python38.txt     # Python 3.8용 패키지 목록
├── python38_environment.sh       # 환경 활성화 스크립트
├── PYTHON38_SETUP.md             # 이 문서
└── .taskmaster/
    └── config.json               # Task Master 설정
```

## 주의사항

1. **환경 분리**: Python 3.8 환경은 시스템 Python과 완전히 분리되어 있습니다.
2. **패키지 호환성**: 모든 패키지는 Python 3.8과 호환되는 버전으로 설치되었습니다.
3. **프로젝트 일관성**: 팀 전체가 동일한 Python 환경을 사용하는 것을 권장합니다.

## 추가 정보

Python 3.8은 2024년 10월까지 지원되므로, 향후 Python 3.9 이상으로 업그레이드를 고려해야 할 수 있습니다. 