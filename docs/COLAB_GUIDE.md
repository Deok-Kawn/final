# 🚀 팀원용 구글 코랩 시작 가이드

> **소요 시간**: 1-2분 | **난이도**: ⭐☆☆☆☆

## 📱 빠른 시작 (1분)

### 1️⃣ 구글 코랩 접속
- [https://colab.research.google.com/](https://colab.research.google.com/) 접속
- 새 노트북 생성 (`파일` → `새 노트북`)

### 2️⃣ 원클릭 셋업 (권장)
새 셀에 아래 코드를 **복사 붙여넣기** 후 실행:

```python
# 🚀 원클릭 프로젝트 셋업
!wget -q https://raw.githubusercontent.com/Deok-Kawn/final/main/notebooks/colab_complete_setup.py
exec(open('colab_complete_setup.py').read())
```

### 3️⃣ 완료 확인
다음과 같은 메시지가 나오면 성공:
```
✅ 셋업 완료!
🎉 이제 다음 단계를 진행하세요:
```

## 🔄 매일 작업할 때

### 작업 시작 전
```python
%cd /content/final
!git pull origin main  # 최신 코드 받기
```

### 작업 완료 후
```python
# 내 작업 저장하기
!git add notebooks/member/
!git commit -m "오늘 작업 내용 간단 설명"
!git push origin main
```

## 📁 내 작업 저장 위치

- **노트북 파일**: `notebooks/member/내이름_실험명.ipynb`
- **결과 이미지**: `results/member/`
- **모델 파일**: Google Drive (크기 때문)

## 📊 일일 보고 방법

1. GitHub 저장소 → **Issues** 탭
2. **New issue** 클릭
3. **"📊 일일 보고서"** 템플릿 선택
4. 오늘 한 작업 간단히 작성

## 🆘 문제 해결

### 자주 있는 문제들

**Q: "fatal: could not read Username" 오류**  
**A:** 위의 원클릭 셋업 사용 (git clone 대신 wget 사용)

**Q: 라이브러리 설치 오류**  
**A:** `!pip install --upgrade pip` 후 재시도

**Q: GPU 메모리 부족**  
**A:** 런타임 → 런타임 유형 변경 → GPU 선택

**Q: 파일이 사라짐**  
**A:** 코랩은 12시간 후 초기화됨 → 꼭 GitHub에 저장!

### 도움 요청 방법

1. [코랩 가이드 이슈](https://github.com/Deok-Kawn/final/issues/2)에 댓글
2. 새 이슈 생성해서 스크린샷과 함께 문의
3. 팀 리더 @Deok-Kawn 멘션

## ✅ 체크리스트

작업 시작 전 확인:
- [ ] 구글 코랩 접속 완료
- [ ] 프로젝트 셋업 완료 
- [ ] Git 설정 완료 (본인 이름/이메일)
- [ ] 최신 코드 받기 완료

작업 완료 후 확인:
- [ ] 노트북 파일 저장
- [ ] GitHub에 변경사항 푸시
- [ ] 일일 보고서 작성
- [ ] 결과 파일 정리

## 🎯 다음 단계

1. `notebooks/00_quick_start_guide.ipynb` 실행
2. 데이터 EDA 시작
3. 첫 번째 모델 실험

**팀원 여러분 화이팅! 🔥**

---
*이 가이드에 추가할 내용이나 수정사항이 있으면 언제든 말씀해주세요!* 