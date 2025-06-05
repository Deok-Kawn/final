# 🚀 딥러닝 대회 팀 프로젝트 시작 가이드

> 딥러닝 대회를 위한 시계열 예측 팀 프로젝트에 오신 것을 환영합니다!

## 📋 목차

1. [빠른 시작](#-빠른-시작)
2. [환경 설정](#-환경-설정)
3. [프로젝트 구조 이해](#-프로젝트-구조-이해)
4. [첫 번째 실험](#-첫-번째-실험)
5. [팀 협업 워크플로우](#-팀-협업-워크플로우)
6. [도움말 및 리소스](#-도움말-및-리소스)

## 🎯 빠른 시작

### 1단계: 저장소 클론 및 환경 확인

```bash
# 1. 저장소 클론 (이미 완료된 상태)
git clone <repository-url>
cd <project-directory>

# 2. Python 환경 확인
python --version  # Python 3.6.9 확인

# 3. 자동 환경 설정 실행
python setup_environment.py

# 4. 환경 테스트
python test_environment.py
```

### 2단계: 의존성 설치

```bash
# 필수 라이브러리 설치
pip install -r requirements_python36.txt

# 설치 확인
python test_environment.py
```

### 3단계: 빠른 시작 노트북 실행

```bash
# Jupyter 노트북 시작
jupyter notebook notebooks/00_quick_start_guide.ipynb
```

## ⚙️ 환경 설정

### 필수 요구사항

- **Python**: 3.6.9
- **운영체제**: Linux/macOS/Windows 10+
- **메모리**: 최소 8GB RAM 권장
- **디스크**: 최소 5GB 여유공간

### GPU 설정 (선택사항)

```bash
# CUDA 설치 확인
nvidia-smi

# PyTorch GPU 버전 설치 (CUDA 10.1 기준)
pip install torch==1.7.1+cu101 torchvision==0.8.2+cu101 -f https://download.pytorch.org/whl/torch_stable.html
```

### IDE 설정

**VSCode 권장 확장:**
- Python
- Jupyter
- GitLens
- Python Docstring Generator

## 🏗️ 프로젝트 구조 이해

```
프로젝트/
├── 📁 src/                     # 핵심 소스 코드
│   ├── 📁 data/               # 데이터 처리 모듈
│   ├── 📁 features/           # 특성 엔지니어링
│   ├── 📁 models/             # 모델 구현
│   └── 📁 utils/              # 유틸리티 함수
├── 📁 data/                   # 데이터 저장소
├── 📁 notebooks/              # Jupyter 노트북
├── 📁 experiments/            # 실험 결과
├── 📁 docs/                   # 문서
└── 📁 outputs/                # 최종 결과물
```

### 핵심 모듈 소개

#### 🔧 데이터 처리 (`src/data/`)
- `DataLoader`: 데이터 로딩 및 전처리
- 일관된 데이터 형식 제공

#### 🎯 특성 엔지니어링 (`src/features/`)
- `TimeSeriesFeatureEngine`: 시계열 특성 생성
- 자동 특성 추출 및 변환

#### 🧠 모델 (`src/models/`)
- `BaseModel`: 모든 모델의 베이스 클래스
- `LSTMModel`: LSTM 기반 시계열 예측 모델
- 확장 가능한 모델 아키텍처

#### 📊 유틸리티 (`src/utils/`)
- `ExperimentTracker`: 실험 추적 및 결과 비교
- `TimeSeriesVisualizer`: 전문적인 시각화 도구

## 🧪 첫 번째 실험

### 1. 기본 베이스라인 실행

```python
# notebooks/00_quick_start_guide.ipynb에서 실행
import sys
sys.path.append('../src')

from data.loader import DataLoader
from models.lstm_model import LSTMModel
from utils.experiment_tracker import ExperimentTracker

# 데이터 로딩
data_loader = DataLoader(data_dir='../data')
train_data = data_loader.load_train_data()

# 모델 학습
model = LSTMModel(
    input_size=1,
    hidden_size=64,
    num_layers=2
)

# 실험 추적
tracker = ExperimentTracker(experiment_dir='../experiments')
tracker.start_experiment('baseline_lstm', {
    'model': 'LSTM',
    'hidden_size': 64,
    'num_layers': 2
})

# 학습 및 평가 코드...
```

### 2. 결과 확인

```python
# 실험 결과 비교
tracker.compare_experiments(['baseline_lstm', 'improved_lstm'])
```

## 👥 팀 협업 워크플로우

### Git 브랜치 전략

```bash
# 1. 새 기능 작업 시작
git checkout main
git pull origin main
git checkout -b feature/your-feature-name

# 2. 작업 후 커밋
git add .
git commit -m "feat: 새로운 모델 아키텍처 추가"

# 3. 원격 브랜치에 푸시
git push origin feature/your-feature-name

# 4. Pull Request 생성
# GitHub에서 PR 생성 및 리뷰 요청
```

### 실험 관리 원칙

1. **고유한 실험명 사용**
   ```python
   experiment_name = f"{your_name}_{model_type}_{date}"
   ```

2. **상세한 파라미터 기록**
   ```python
   config = {
       'model_type': 'LSTM',
       'sequence_length': 30,
       'hidden_size': 128,
       'learning_rate': 0.001,
       'batch_size': 32,
       'author': 'your_name'
   }
   ```

3. **결과 공유**
   - 주요 실험 결과는 팀 채널에 공유
   - `experiments/` 폴더의 결과 파일 커밋

### 코드 리뷰 체크리스트

- [ ] 코드가 PEP 8 스타일 가이드를 따르는가?
- [ ] 함수와 클래스에 적절한 docstring이 있는가?
- [ ] 실험 결과가 재현 가능한가?
- [ ] 성능 개선이 있는가?
- [ ] 테스트가 통과하는가?

## 📚 도움말 및 리소스

### 자주 사용하는 명령어

```bash
# 환경 테스트
python test_environment.py

# 자동 환경 설정
python setup_environment.py

# Jupyter 노트북 시작
jupyter notebook

# 새 브랜치 생성
git checkout -b feature/your-feature

# 실험 스크립트 실행
python scripts/train_model.py --config configs/lstm_config.yaml
```

### 문서 및 가이드

- 📖 [팀 협업 가이드라인](TEAM_GUIDELINES.md)
- 🔧 [모델 개발 가이드](MODEL_DEVELOPMENT.md)
- 📊 [실험 추적 가이드](EXPERIMENT_TRACKING.md)
- 🐛 [문제 해결 가이드](TROUBLESHOOTING.md)

### 도움 요청

1. **기술적 문제**: GitHub Issues 생성
2. **팀 협업 문제**: 팀 채널에서 논의
3. **긴급 문제**: 팀 리더에게 직접 연락

### 유용한 자료

- [PyTorch 공식 문서](https://pytorch.org/docs/)
- [시계열 예측 베스트 프랙티스](https://otexts.com/fpp3/)
- [딥러닝 하이퍼파라미터 튜닝](https://www.deeplearningbook.org/)

## 🎉 첫 기여 가이드

### 1. 간단한 실험으로 시작

```python
# 1. 기존 모델의 하이퍼파라미터 조정
model = LSTMModel(hidden_size=128)  # 기본값 64에서 변경

# 2. 새로운 특성 추가
feature_engine.add_moving_average(window=7)

# 3. 결과 비교 및 공유
tracker.save_results()
```

### 2. 점진적 개선

- 작은 변경사항부터 시작
- 실험 결과 문서화
- 팀원들과 결과 공유
- 피드백 반영

### 3. 기여 영역 예시

- 🔍 새로운 특성 엔지니어링 기법
- 🧠 다른 모델 아키텍처 (GRU, Transformer 등)
- 📊 시각화 개선
- ⚡ 성능 최적화
- 📖 문서 개선

---

## 🚀 지금 시작하세요!

1. `python setup_environment.py` 실행
2. `notebooks/00_quick_start_guide.ipynb` 열기
3. 첫 번째 실험 실행
4. 결과를 팀에 공유

**질문이 있으시면 언제든지 GitHub Issues에 등록하거나 팀 채널에서 문의하세요!**

---

*Happy Coding! 🎯* 