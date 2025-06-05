# 🤖 Models 폴더

이 폴더는 **딥러닝 모델 클래스 정의 전용**입니다.

## 📁 파일 구성

```
base_model.py        # 모든 모델의 기본 클래스
lstm_model.py        # LSTM 기반 시계열 예측 모델
__init__.py          # 패키지 초기화 파일
```

## 🎯 각 파일의 역할

### base_model.py
- **목적**: 모든 모델의 공통 기능을 정의하는 추상 기본 클래스
- **주요 기능**:
  - 모델 초기화 템플릿
  - 공통 훈련/검증 로직
  - 성능 평가 메서드
  - 모델 저장/로딩 인터페이스

### lstm_model.py  
- **목적**: LSTM 기반 시계열 예측 모델 구현
- **주요 기능**:
  - LSTM 아키텍처 정의
  - 시계열 특화 전처리
  - 배치 데이터 처리
  - 예측 및 후처리

### __init__.py
- **목적**: 패키지 모듈로 인식 및 편리한 import 제공
- **기능**: 주요 클래스들을 외부에서 쉽게 import 가능

## 🚀 사용 방법

### 모델 import 및 사용
```python
from src.models import LSTMModel, BaseModel

# LSTM 모델 초기화
model = LSTMModel(
    input_size=10,
    hidden_size=50,
    num_layers=2,
    output_size=1
)

# 모델 훈련
model.fit(X_train, y_train)

# 예측
predictions = model.predict(X_test)
```

### 새로운 모델 추가 규칙
1. **BaseModel을 상속받아 구현**
2. **파일명**: `[모델명]_model.py` (예: `transformer_model.py`)
3. **클래스명**: `[모델명]Model` (예: `TransformerModel`)
4. **__init__.py에 import 추가**

## 📂 연관 폴더
- **훈련된 모델 저장**: `models/leader/`, `models/member/`
- **모델 실험 노트북**: `notebooks/leader/`, `notebooks/member/`
- **모델 성능 결과**: `results/leader/`, `results/member/`

## ⚠️ 주의사항
- 이 폴더는 **모델 클래스 정의만** 포함합니다
- 실제 훈련 코드는 `notebooks/` 폴더에 작성하세요
- 훈련된 모델 가중치는 `models/` 폴더에 저장하세요
- 새 모델 추가 시 반드시 BaseModel을 상속받으세요 