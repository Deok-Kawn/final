# 🚨 GitHub 초보자 응급처치 치트시트

> 2명 팀을 위한 꼭 필요한 Git 명령어만 모음

## 📋 매일 사용하는 기본 명령어

### 🔄 작업 시작할 때마다 (필수!)
```bash
# 1. 최신 코드 받기
git pull origin main

# 2. 새 브랜치 만들기
git checkout -b feature/내실험이름
```

### 📝 작업 완료 후 저장
```bash
# 1. 변경된 파일 확인
git status

# 2. 모든 변경사항 추가
git add .

# 3. 커밋 (저장) - 메시지는 한글도 OK!
git commit -m "LSTM 모델 하이퍼파라미터 튜닝 완료"

# 4. GitHub에 업로드
git push origin feature/내실험이름
```

### 🔀 Pull Request 만들기
1. **GitHub 웹사이트 접속**
2. **노란색 "Compare & pull request" 버튼** 클릭
3. **제목과 설명 작성** 후 **Create pull request**
4. **팀원에게 리뷰 요청** (오른쪽 Reviewers에서 선택)

---

## 🆘 문제 상황별 해결법

### ❌ "Permission denied" 에러
```bash
# HTTPS 방식으로 클론 (가장 쉬움)
git clone https://github.com/USERNAME/REPO_NAME.git
```

### ❌ "Merge conflict" (충돌) 발생
```bash
# 1. 충돌 파일 열어서 직접 수정
# 2. 충돌 해결 후:
git add .
git commit -m "충돌 해결"
git push origin 브랜치이름
```

### ❌ 실수로 main 브랜치에 커밋
```bash
# 새 브랜치 만들어서 옮기기
git checkout -b feature/실수수정
git push origin feature/실수수정
# 그 다음 PR 만들기
```

### ❌ 브랜치를 잘못 만들었을 때
```bash
# 브랜치 삭제
git branch -d 잘못된브랜치이름

# 다시 올바른 브랜치 만들기
git checkout -b feature/올바른이름
```

---

## 🔍 상황 확인 명령어

### 📊 현재 상태 보기
```bash
# 현재 브랜치와 변경사항 확인
git status

# 브랜치 목록 보기
git branch -a

# 커밋 히스토리 보기
git log --oneline

# 어떤 브랜치에 있는지 확인
git branch
```

### 💾 임시 저장 (급할 때 유용!)
```bash
# 작업 중인 내용 임시 저장
git stash

# 다른 작업 후 임시 저장한 것 복구
git stash pop
```

---

## 🎯 2명 팀 워크플로우

### 📅 매일 루틴
```bash
# 🌅 작업 시작
git checkout main
git pull origin main
git checkout -b feature/오늘할실험

# 🔬 실험 진행...

# 🌙 작업 종료
git add .
git commit -m "오늘 실험 결과"
git push origin feature/오늘할실험
# GitHub에서 PR 생성
```

### 🤝 코드 리뷰 과정
1. **A가 실험 완료** → PR 생성
2. **B가 코드 리뷰** → 승인 또는 수정 요청
3. **문제없으면 Merge** → main 브랜치에 합쳐짐
4. **B가 새 실험 시작** → 최신 코드 받고 새 브랜치

---

## 📱 응급상황 연락처

### 🚨 막혔을 때
1. **GitHub Desktop 사용** (GUI 도구, 더 쉬움)
2. **팀원에게 화면공유로 도움 요청**
3. **Stack Overflow 검색**: "git [에러메시지]"

### 💡 유용한 도구들
- **GitHub Desktop**: GUI 환경에서 Git 사용
- **VS Code Git 기능**: 에디터에서 바로 Git 조작
- **SourceTree**: 또 다른 Git GUI 도구

---

## 🎉 첫 성공 체크리스트

- [ ] GitHub 저장소 만들기 ✅
- [ ] 팀원 초대하기 ✅
- [ ] 각자 프로젝트 클론하기 ✅
- [ ] 브랜치 만들어서 간단한 수정 후 PR 테스트 ✅
- [ ] 서로 코드 리뷰해보기 ✅

**🚀 이것만 되면 이제 GitHub 마스터!**

---

## 📞 도움말

막히면 언제든지:
1. **팀원과 화면공유**로 함께 해결
2. **구글링**: "git 초보자 [문제상황]"
3. **YouTube**: "Git 사용법" 검색

**💪 화이팅! 처음엔 어렵지만 금방 익숙해질 거예요!** 