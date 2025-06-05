# 팀 리더 전용 노트북 폴더

이 폴더는 **팀 리더 전용**입니다.

## 📋 작업 가이드라인

### 파일 명명 규칙
```
model_[모델명]_v[버전].ipynb
analysis_[분석주제]_v[버전].ipynb

예시:
- model_lstm_v1.ipynb
- model_gru_v2.ipynb  
- analysis_trend_v1.ipynb
- analysis_feature_importance_v1.ipynb
```

### 노트북 구조 템플릿
1. **데이터 로딩 및 전처리**
2. **모델 정의 및 훈련**
3. **성능 평가**
4. **결과 시각화**
5. **결론 및 다음 단계**

### 결과 저장 위치
- 훈련된 모델: `models/leader/`
- 시각화 결과: `results/leader/`
- 예측 결과: `results/leader/predictions/`

### 작업 완료 후 체크리스트
- [ ] 결과를 `/results/leader/` 폴더에 저장
- [ ] README.md의 실험 결과표 업데이트
- [ ] GitHub Issues에 진행상황 업데이트
- [ ] 팀원과 결과 공유 