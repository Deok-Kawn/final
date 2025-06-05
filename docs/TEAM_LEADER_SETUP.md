# 👑 GitHub 초보 팀 리더 설정 가이드

> 2명 팀을 위한 GitHub 저장소 설정 및 관리 가이드

## 📋 체크리스트

- [ ] GitHub 저장소 생성
- [ ] 프로젝트 코드 업로드  
- [ ] 팀원 초대
- [ ] 기본 설정 완료
- [ ] 팀원 교육

## 🚀 1단계: GitHub 저장소 생성

### 1.1 GitHub에서 새 저장소 만들기

1. **GitHub.com 접속** → 로그인
2. **우측 상단 `+` 버튼** → `New repository` 클릭
3. **저장소 정보 입력:**
   ```
   Repository name: timeseries-team-project
   Description: 딥러닝 시계열 예측 대회 팀 프로젝트
   
   ✅ Private (대회 코드는 비공개 권장)
   ❌ Add a README file (이미 있으니까 체크 해제)
   ❌ Add .gitignore (이미 있으니까 None 선택)
   ❌ Choose a license (None 선택)
   ```
4. **`Create repository` 클릭**

### 1.2 현재 프로젝트 업로드

```bash
# 현재 프로젝트 폴더에서 실행 (터미널/명령프롬프트)

# 1. Git 저장소 초기화
git init

# 2. 모든 파일 추가
git add .

# 3. 첫 번째 커밋
git commit -m "feat: 딥러닝 팀 프로젝트 초기 설정 완료

- 완전한 src/ 모듈 구조 구축
- 자동화 도구 (setup_environment.py, test_environment.py)
- 팀 협업 문서 및 템플릿
- 실험 추적 시스템
- 시각화 유틸리티"

# 4. GitHub 저장소와 연결 (⚠️ 여기서 YOUR_USERNAME과 YOUR_REPO_NAME을 실제로 바꿔주세요!)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 5. 기본 브랜치를 main으로 설정
git branch -M main

# 6. 코드 업로드
git push -u origin main
```

## 👥 2단계: 팀원 초대

### 2.1 Collaborator 추가
1. **GitHub 저장소 페이지** → `Settings` 탭 클릭
2. **왼쪽 메뉴** → `Collaborators` 클릭  
3. **`Add people` 버튼** 클릭
4. **팀원의 GitHub 아이디** 입력 후 초대

### 2.2 팀원에게 안내 메시지

```
안녕하세요! 딥러닝 대회 팀 프로젝트에 초대합니다 🎉

GitHub 저장소: https://github.com/YOUR_USERNAME/YOUR_REPO_NAME

시작 방법:
1. 저장소 클론: git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
2. 폴더 이동: cd YOUR_REPO_NAME  
3. 환경 설정: python setup_environment.py
4. 환경 테스트: python test_environment.py
5. 시작 가이드: docs/GETTING_STARTED.md 읽기

질문 있으면 언제든 연락주세요! 📱
```

## ⚙️ 3단계: 기본 설정 (2명 팀용 간소화)

### 3.1 브랜치 보호 설정 (선택사항)
1. **Settings** → **Branches** → **Add rule**
2. **Branch name pattern:** `main`
3. **설정 (2명 팀용 권장):**
   ```
   ✅ Require pull request reviews before merging
   ✅ Require review from CODEOWNERS  
   ❌ Require status checks (아직은 복잡함)
   ❌ Require branches to be up to date (너무 엄격함)
   ```

### 3.2 이슈 템플릿 확인
- 이미 생성된 이슈 템플릿들이 잘 작동하는지 확인
- **Issues** 탭 → **New issue** → 템플릿이 보이는지 확인

## 📚 4단계: 팀원 교육 (간단버전)

### 4.1 Git 기본 명령어 (팀원과 공유)

```bash
# 📥 프로젝트 가져오기 (처음 한번만)
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# 🔄 최신 코드 받기 (매번 작업 전)
git pull origin main

# 🌿 새 브랜치 만들어서 작업
git checkout -b feature/my-experiment

# 📝 작업 후 저장
git add .
git commit -m "feat: LSTM 하이퍼파라미터 튜닝 실험"

# 📤 내 브랜치 업로드
git push origin feature/my-experiment

# 🔀 GitHub에서 Pull Request 생성
```

### 4.2 브랜치 전략 (2명용 단순화)

```
main (메인 브랜치)
├── feature/leader-baseline     (리더의 베이스라인 작업)
├── feature/member-lstm        (팀원의 LSTM 실험)
├── feature/leader-ensemble    (리더의 앙상블 시도)
└── feature/member-features    (팀원의 특성 엔지니어링)
```

**규칙:**
- 개인 실험은 `feature/이름-실험내용` 브랜치에서
- 완료되면 Pull Request로 코드 리뷰
- 서로 승인하면 main에 merge

### 4.3 실험 관리 규칙

```python
# 실험명 규칙: 이름_모델_날짜
experiment_name = "leader_lstm_1201"  # 리더가 12월 1일에 한 LSTM 실험
experiment_name = "member_gru_1202"   # 팀원이 12월 2일에 한 GRU 실험

# 실험 설정 예시
config = {
    'author': 'leader',  # 또는 'member'
    'model_type': 'LSTM',
    'sequence_length': 30,
    'hidden_size': 128,
    'learning_rate': 0.001,
    'batch_size': 32,
    'note': '하이퍼파라미터 튜닝 1차 시도'
}
```

## 🎯 5단계: 첫 실험 함께 해보기

### 5.1 각자 역할 분담 제안

**팀 리더 (당신):**
- 베이스라인 모델 구축
- 전체 파이프라인 확인
- 실험 결과 취합 및 분석

**팀원:**
- 특성 엔지니어링 실험
- 다른 모델 아키텍처 시도
- 하이퍼파라미터 최적화

### 5.2 첫 주 계획

```
Day 1-2: 환경 설정 및 데이터 탐색
Day 3-4: 각자 베이스라인 모델 실행
Day 5-6: 결과 공유 및 개선 방향 논의
Day 7: 다음 주 계획 수립
```

## 🆘 문제 해결

### 자주 발생하는 문제들

1. **"Permission denied" 에러**
   ```bash
   # SSH 키 설정 또는 HTTPS 클론 사용
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   ```

2. **Merge conflict 발생**
   ```bash
   # 충돌 파일을 직접 수정 후
   git add .
   git commit -m "fix: merge conflict 해결"
   ```

3. **실수로 main에 직접 커밋**
   ```bash
   # 새 브랜치 만들어서 옮기기
   git checkout -b feature/fix-main
   git push origin feature/fix-main
   # 그 다음 PR 생성
   ```

## 📞 팀원 지원

### GitHub 초보 팀원을 위한 지원

1. **화면 공유로 첫 설정 도와주기**
2. **간단한 치트시트 만들어서 공유**
3. **막히면 바로 물어보라고 안내**

### 치트시트 예시

```bash
# 🚨 응급처치 명령어들

# 최신 코드 받기
git pull origin main

# 내 변경사항 임시 저장
git stash

# 임시 저장한 것 복구
git stash pop

# 브랜치 목록 보기
git branch -a

# 브랜치 전환
git checkout main
git checkout feature/my-branch

# 상태 확인
git status
```

---

## 🎉 완료 체크

모든 설정이 끝나면:

- [ ] 둘 다 저장소에 접근 가능
- [ ] 각자 브랜치를 만들어서 간단한 수정 후 PR 테스트
- [ ] 실험 추적 시스템 사용법 확인
- [ ] `notebooks/00_quick_start_guide.ipynb` 함께 실행

**🚀 이제 본격적인 딥러닝 대회 도전 시작!** 