# 🤝 팀 협업 가이드라인

## 📋 목차
- [Git 워크플로우](#git-워크플로우)
- [브랜치 전략](#브랜치-전략)
- [커밋 컨벤션](#커밋-컨벤션)
- [코드 리뷰 프로세스](#코드-리뷰-프로세스)
- [실험 관리](#실험-관리)
- [이슈 트래킹](#이슈-트래킹)

## 🌳 Git 워크플로우

### 기본 원칙
1. **main 브랜치는 항상 안정 상태 유지**
2. **새로운 기능은 별도 브랜치에서 개발**
3. **Pull Request를 통한 코드 리뷰 필수**
4. **충돌 발생 시 팀원과 협의 후 해결**

### 작업 순서
```bash
# 1. 최신 main 브랜치로 업데이트
git checkout main
git pull origin main

# 2. 새 기능 브랜치 생성
git checkout -b feature/model-optimization

# 3. 작업 후 커밋
git add .
git commit -m "feat(model): LSTM 하이퍼파라미터 최적화"

# 4. 원격 저장소에 푸시
git push origin feature/model-optimization

# 5. GitHub에서 Pull Request 생성
```

## 🌿 브랜치 전략

### 브랜치 명명 규칙
- `feature/기능명`: 새로운 기능 개발
- `fix/버그명`: 버그 수정
- `experiment/실험명`: 실험적 기능
- `data/데이터명`: 데이터 처리 관련
- `model/모델명`: 모델 관련 작업

### 예시
```
feature/lstm-implementation
fix/data-loading-error
experiment/transformer-model
data/feature-engineering
model/ensemble-method
```

## 📝 커밋 컨벤션

### 커밋 메시지 형식
```
타입(범위): 제목

상세 설명 (선택사항)

관련 이슈: #이슈번호
```

### 커밋 타입
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 스타일 변경
- `refactor`: 코드 리팩토링
- `test`: 테스트 코드
- `chore`: 빌드, 설정 변경

### 범위 예시
- `data`: 데이터 처리
- `model`: 모델 관련
- `feature`: 특성 엔지니어링
- `experiment`: 실험 코드
- `utils`: 유틸리티

### 커밋 메시지 예시
```bash
feat(model): LSTM 모델 구현

- 시계열 데이터용 LSTM 네트워크 구조 설계
- 하이퍼파라미터 설정 가능한 클래스 구현
- 조기 종료 기능 추가

관련 이슈: #12
```

## 👀 코드 리뷰 프로세스

### Pull Request 작성 가이드
1. **명확한 제목과 설명**
2. **변경 사항 요약**
3. **테스트 결과 포함**
4. **스크린샷 또는 결과 이미지**

### 리뷰어 체크리스트
- [ ] 코드 스타일 일관성
- [ ] 함수/변수명의 명확성
- [ ] 주석 및 문서화
- [ ] 성능 영향도
- [ ] 테스트 코드 존재
- [ ] 실험 결과 기록

### PR 템플릿
```markdown
## 변경 사항
- 주요 변경 내용 요약

## 테스트 결과
- 실행된 테스트 및 결과
- 성능 메트릭 (RMSE, MAE 등)

## 체크리스트
- [ ] 코드 테스트 완료
- [ ] 문서 업데이트
- [ ] 실험 결과 기록
```

## 🧪 실험 관리

### 실험 기록 원칙
1. **모든 실험은 ExperimentTracker 사용**
2. **하이퍼파라미터와 결과 상세 기록**
3. **재현 가능한 코드 작성**
4. **실험 노트 작성 (notebooks/ 디렉토리)**

### 실험 명명 규칙
```
YYYYMMDD_모델명_실험목적.ipynb
20241201_LSTM_hyperparameter_tuning.ipynb
20241202_ensemble_methods_comparison.ipynb
```

### 모델 저장 규칙
```
models/
├── baseline/
├── lstm/
│   ├── v1_20241201.pth
│   ├── v2_20241202.pth
│   └── best_model.pth
└── ensemble/
```

## 🎯 이슈 트래킹

### 이슈 라벨
- `bug`: 버그 수정
- `feature`: 새로운 기능
- `enhancement`: 기능 개선
- `documentation`: 문서 작업
- `experiment`: 실험 관련
- `priority-high`: 높은 우선순위
- `help-wanted`: 도움 필요

### 이슈 템플릿

#### 버그 리포트
```markdown
## 버그 설명
간단한 버그 설명

## 재현 방법
1. 
2. 
3. 

## 예상 결과
무엇이 일어나야 하는지

## 실제 결과
실제로 무엇이 일어났는지

## 환경
- OS: 
- Python 버전: 
- 라이브러리 버전: 
```

#### 기능 요청
```markdown
## 기능 설명
추가하고 싶은 기능에 대한 설명

## 필요성
왜 이 기능이 필요한지

## 구현 아이디어
구현 방법에 대한 아이디어 (선택사항)
```

## 📊 성능 모니터링

### 주요 메트릭
- **RMSE**: 주요 평가 지표
- **MAE**: 보조 지표
- **학습 시간**: 효율성 측정
- **메모리 사용량**: 리소스 모니터링

### 베이스라인 성능
```python
# 현재 베스트 성능 (업데이트 필요)
BASELINE_RMSE = 1000.0
TARGET_RMSE = 600.0
```

## 🔧 개발 환경 설정

### 필수 확인사항
1. Python 3.6.9 사용
2. requirements_python36.txt 설치
3. GPU 설정 (선택사항)
4. 환경 테스트 실행: `python test_environment.py`

### 추천 도구
- **IDE**: VSCode, PyCharm
- **Git GUI**: GitHub Desktop, SourceTree
- **Jupyter**: Lab 또는 Notebook
- **시각화**: matplotlib, seaborn, plotly

## 🚨 주의사항

### 데이터 보안
- 민감한 데이터는 절대 커밋하지 않기
- .gitignore 규칙 준수
- 대용량 파일은 Git LFS 사용 고려

### 성능 최적화
- 메모리 사용량 모니터링
- 배치 크기 조정으로 OOM 방지
- 불필요한 라이브러리 import 방지

### 협업 에티켓
- 타인의 브랜치 강제 push 금지
- 큰 변경사항은 사전 논의
- 코드 리뷰는 건설적으로
- 실험 결과는 정확하게 기록

---

**질문이나 제안사항이 있으면 언제든 이슈를 생성하거나 팀 채팅에 공유해 주세요! 🙌** 