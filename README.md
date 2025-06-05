# 🔮 시계열 예측 프로젝트 - 일별 최대 전력 수요 예측

[![GitHub stars](https://img.shields.io/github/stars/Deok-Kawn/final?style=flat-square)](https://github.com/Deok-Kawn/final/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/Deok-Kawn/final?style=flat-square)](https://github.com/Deok-Kawn/final/issues)
[![Python](https://img.shields.io/badge/Python-3.6.9-blue?style=flat-square)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-1.7.1-orange?style=flat-square)](https://pytorch.org/)

> **2005-2023년 일별 최대 전력 데이터를 기반으로 2024-2025년 527일간의 전력 수요를 예측하는 머신러닝 프로젝트**

## 🎯 프로젝트 미션

**전력 수요 예측의 정확도를 높여 효율적인 전력 공급 계획에 기여하는 것**

- 📊 **데이터**: 19년간(2005-2023) 일별 최대 전력 수급 데이터
- 🎯 **목표**: 527일간(2024.01.01-2025.06.10) 전력 수요 예측  
- 📈 **평가**: RMSE (Root Mean Square Error) 최소화
- 🏆 **목표 성능**: RMSE < 600 달성

## 👥 팀 구성

### 🧭 **프로젝트 리더**
- **역할**: 전체 프로젝트 관리, 최종 모델 결정, 팀 조율
- **책임**: 코드 품질 관리, 성능 최적화, 제출 관리

### 👨‍💻 **팀 멤버들**
- **역할**: 개별 모델 실험, 특성 엔지니어링, 데이터 분석
- **기여**: 다양한 접근법 시도, 창의적 아이디어 제안
- **협업**: GitHub Issues를 통한 일일 보고 및 결과 공유

### 🤝 **협업 방식**
- **일일 보고**: GitHub Issues 템플릿 활용
- **코드 공유**: Git을 통한 버전 관리
- **역할 분리**: `notebooks/member/` vs `notebooks/leader/`
- **지식 공유**: 실험 결과 및 인사이트 공유

## 🏗️ 프로젝트 아키텍처

### 📂 **팀별 작업 공간**
```
📦 프로젝트 구조
├── 📁 notebooks/
│   ├── 👥 member/          # 팀원 전용 실험 공간
│   └── 👑 leader/          # 리더 전용 관리 공간
├── 📁 results/
│   ├── 👥 member/          # 팀원 실험 결과
│   └── 👑 leader/          # 최종 결과 및 분석
├── 📁 models/
│   ├── 👥 member/          # 팀원 개발 모델
│   └── 👑 leader/          # 최종 선정 모델
└── 📁 data/shared/         # 공유 데이터셋
```

### 🛠️ **기술 스택**
- **딥러닝**: PyTorch 1.7.1 (LSTM, GRU, Transformer)
- **머신러닝**: Scikit-learn 0.23.2 (앙상블, 회귀)
- **시계열**: Prophet 0.7.1, Statsmodels 0.12.2
- **최적화**: Optuna 2.10.1 (하이퍼파라미터 튜닝)
- **데이터**: Pandas 1.1.5, NumPy 1.19.5
- **시각화**: Matplotlib, Seaborn, Plotly

## 🚀 빠른 시작

### 🌟 **팀원용 원클릭 셋업**
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

**👉 [구글 코랩 셋업 가이드](https://github.com/Deok-Kawn/final/issues/2)**

구글 코랩에서 30초 만에 프로젝트 환경 구축이 가능합니다!

### 💻 **로컬 환경 설정**
```bash
# 1. 저장소 클론
git clone https://github.com/Deok-Kawn/final.git
cd final

# 2. 환경 테스트
python test_environment.py

# 3. 라이브러리 설치
pip install -r requirements_python36.txt
```

## 📈 개발 진행 상황

### ✅ **완료된 단계**
- [x] **프로젝트 환경 구축**: Git 워크플로우, 폴더 구조
- [x] **팀 협업 시스템**: Issues 템플릿, 보고서 양식
- [x] **구글 코랩 연동**: 원클릭 셋업 시스템
- [x] **코드베이스 기반**: 데이터 로더, 모델 베이스 클래스

### 🔄 **진행 중인 단계**
- [ ] **데이터 분석**: EDA, 전처리 파이프라인
- [ ] **베이스라인 모델**: 이동평균, 선형회귀
- [ ] **딥러닝 모델**: LSTM, GRU 기본 구현
- [ ] **성능 평가 시스템**: 교차 검증, 메트릭 추적

### 🎯 **향후 계획**
- [ ] **고급 모델**: Transformer, 앙상블
- [ ] **하이퍼파라미터 최적화**: Optuna 활용
- [ ] **모델 최적화**: 성능 튜닝, 추론 속도 개선
- [ ] **최종 제출**: 결과 분석, 문서화

## 🏆 성과 목표

### 📊 **모델 성능 로드맵**
| 단계 | 모델 | 목표 RMSE | 현재 상태 |
|------|------|-----------|-----------|
| 1단계 | 베이스라인 | < 1000 | 🔄 진행중 |
| 2단계 | LSTM/GRU | < 800 | ⏳ 대기중 |
| 3단계 | Transformer | < 700 | ⏳ 대기중 |
| 4단계 | 앙상블 | **< 600** | ⏳ 대기중 |

### 🎖️ **프로젝트 성과**
- **팀 협업 시스템**: 체계적인 역할 분담 및 소통
- **자동화된 환경**: 구글 코랩 원클릭 셋업
- **확장 가능한 구조**: 모듈화된 코드베이스
- **실험 추적**: 체계적인 모델 관리 시스템

## 📊 데이터 개요

### 📈 **데이터 특성**
- **기간**: 2005.01.01 ~ 2023.12.31 (19년간)
- **특징**: 일별 최대 전력 수급량
- **크기**: 약 6,940개 데이터 포인트
- **예측 목표**: 2024.01.01 ~ 2025.06.10 (527일)

### 🔍 **데이터 도전 과제**
- **계절성**: 여름/겨울 전력 수요 패턴
- **트렌드**: 장기적 전력 수요 증가 추세
- **불규칙성**: 휴일, 특이사항으로 인한 변동
- **누락 데이터**: 일부 기간 데이터 부재 가능성

## 💡 핵심 기술 및 접근법

### 🧠 **딥러닝 모델**
- **LSTM**: 장기 의존성 학습
- **GRU**: 효율적인 순환 신경망
- **Transformer**: 어텐션 메커니즘 활용

### 📊 **통계 모델**
- **ARIMA**: 자기회귀 통합 이동평균
- **Prophet**: Facebook의 시계열 예측 라이브러리
- **지수 평활법**: 트렌드 및 계절성 모델링

### 🔧 **특성 엔지니어링**
- **시간 특성**: 요일, 월, 계절, 휴일
- **래그 특성**: 과거 N일 전력 수요
- **롤링 통계**: 이동평균, 표준편차
- **외부 변수**: 기온, 경제지표 (가능한 경우)

## 🤝 기여 및 참여

### 👨‍💻 **팀원으로 참여**
1. **환경 설정**: [구글 코랩 가이드](https://github.com/Deok-Kawn/final/issues/2) 따라하기
2. **작업 공간**: `notebooks/member/` 폴더에서 실험
3. **일일 보고**: [Daily Report](https://github.com/Deok-Kawn/final/issues/new?template=daily_report.md) 작성
4. **결과 공유**: Git을 통한 코드 및 결과 공유

### 🌟 **기여 방법**
- **새로운 모델 아이디어** 제안 및 구현
- **데이터 전처리** 기법 개발
- **성능 개선** 아이디어 및 실험
- **버그 리포트** 및 코드 개선

## 📞 문의 및 지원

### 💬 **소통 채널**
- **GitHub Issues**: 버그 리포트, 기능 요청
- **Daily Report**: 일일 진행상황 공유
- **Team Discussion**: 프로젝트 관련 논의

### 🆘 **지원 요청**
문제가 발생하면 [여기](https://github.com/Deok-Kawn/final/issues/2)에 댓글로 문의하세요!
- 오류 메시지 전체 첨부
- 발생 단계 명시
- 스크린샷 첨부 (가능한 경우)

**⚡ 24시간 내 답변 보장!**

---

## 📄 라이센스

이 프로젝트는 시계열 예측 연구 및 교육 목적으로 개발되었습니다.

**🚀 함께 미래의 전력 수요를 예측해봅시다!** 