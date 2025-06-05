# 팀원 전용 노트북 폴더

이 폴더는 **팀원 전용**입니다.

## 🚀 구글 코랩 사용자를 위한 가이드

### 코랩에서 GitHub 연동 (첫 실행 시)
```python
# 1. GitHub 저장소 클론
!git clone https://github.com/YOUR-USERNAME/timeseries-competition.git
%cd timeseries-competition

# 2. Git 사용자 정보 설정
!git config --global user.name "팀원이름"
!git config --global user.email "팀원이메일@example.com"
```

### 일일 작업 루틴
```python
# 1. 최신 코드 가져오기
!git pull origin main

# 2. 작업 진행 후 저장
!git add notebooks/member/
!git commit -m "feat: 새로운 모델 실험 결과 추가"
!git push origin main
```

### 파일 명명 규칙
```
model_[모델명]_v[버전].ipynb
analysis_[분석주제]_v[버전].ipynb

예시:
- model_transformer_v1.ipynb
- model_cnn_lstm_v2.ipynb
- analysis_seasonal_patterns_v1.ipynb
```

### 공유 데이터 접근
```python
# 공유 데이터 로딩
import pandas as pd
train_df = pd.read_csv('/content/timeseries-competition/data/shared/data.csv')
full_df = pd.read_csv('/content/timeseries-competition/data/shared/full_data.csv')
```

### 결과 저장 위치
- 훈련된 모델: 구글 드라이브 + GitHub에 모델 정보 기록
- 시각화 결과: `results/member/`
- 예측 결과: `results/member/predictions/`

### 작업 완료 후 체크리스트
- [ ] 노트북을 `notebooks/member/` 폴더에 저장
- [ ] 결과 이미지/파일을 `results/member/` 폴더에 저장
- [ ] GitHub Issues에 일일 보고서 작성
- [ ] 실험 결과를 팀 리더와 공유 