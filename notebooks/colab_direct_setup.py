# 🚀 구글 코랩 직접 실행 셋업 (복사-붙여넣기용)
# 이 코드를 구글 코랩 셀에 복사해서 실행하세요

import os
import subprocess
import sys
import requests
from pathlib import Path

print("🚀 시계열 예측 프로젝트 셋업 시작")
print("=" * 50)

def run_cmd(cmd, description=""):
    """명령어 실행 함수"""
    if description:
        print(f"📋 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ 성공: {description or cmd}")
            return True
        else:
            print(f"❌ 실패: {description or cmd}")
            print(f"오류: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 예외: {e}")
        return False

# 1. 기존 디렉토리 정리
print("\n🧹 환경 정리")
for dirname in ['final', 'final-main', 'main.zip']:
    if os.path.exists(dirname):
        run_cmd(f"rm -rf {dirname}", f"{dirname} 제거")

# 2. 프로젝트 다운로드 (여러 방법 시도)
print("\n📥 프로젝트 다운로드")

# 방법 1: wget
success = run_cmd(
    "wget -q https://github.com/Deok-Kawn/final/archive/refs/heads/main.zip",
    "wget으로 다운로드"
)

if not success:
    print("📥 curl로 재시도...")
    # 방법 2: curl
    success = run_cmd(
        "curl -L -o main.zip https://github.com/Deok-Kawn/final/archive/refs/heads/main.zip",
        "curl로 다운로드"
    )

if not success:
    print("📥 Python requests로 재시도...")
    # 방법 3: Python requests
    try:
        url = "https://github.com/Deok-Kawn/final/archive/refs/heads/main.zip"
        response = requests.get(url)
        if response.status_code == 200:
            with open('main.zip', 'wb') as f:
                f.write(response.content)
            print("✅ Python requests로 다운로드 성공")
            success = True
        else:
            print(f"❌ requests 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ requests 예외: {e}")

if not success:
    print("❌ 모든 다운로드 방법 실패")
    print("💡 수동 방법을 시도해주세요:")
    print("   1. https://github.com/Deok-Kawn/final 접속")
    print("   2. Code -> Download ZIP 클릭")
    print("   3. 코랩에 파일 업로드")
    sys.exit(1)

# 3. 압축 해제
print("\n📦 압축 해제")
if not run_cmd("unzip -q main.zip", "ZIP 압축 해제"):
    print("❌ 압축 해제 실패")
    sys.exit(1)

# 4. 디렉토리 설정
print("\n📁 디렉토리 설정")
if not run_cmd("mv final-main final", "디렉토리명 변경"):
    print("❌ 디렉토리 설정 실패")
    sys.exit(1)

# 5. 작업 디렉토리 변경
os.chdir('final')
print(f"📍 현재 위치: {os.getcwd()}")

# 6. Git 설정
print("\n🔧 Git 설정")
run_cmd('git config --global user.name "Team Member"', "Git 사용자명 설정")
run_cmd('git config --global user.email "member@example.com"', "Git 이메일 설정")

# 7. Git 저장소 초기화
print("\n🔗 Git 저장소 설정")
run_cmd("git init", "Git 초기화")
run_cmd("git remote add origin https://github.com/Deok-Kawn/final.git", "원격 저장소 연결")

# 8. Python 환경 확인
print("\n🐍 환경 확인")
print(f"Python: {sys.version}")
print(f"작업 디렉토리: {os.getcwd()}")

# 9. 필수 라이브러리 설치
print("\n📚 라이브러리 설치")
if os.path.exists('requirements_python36.txt'):
    run_cmd("pip install -r requirements_python36.txt", "requirements 설치")
else:
    # 기본 라이브러리 설치
    libs = ["pandas", "numpy", "matplotlib", "seaborn", "scikit-learn", "torch"]
    for lib in libs:
        run_cmd(f"pip install {lib}", f"{lib} 설치")

# 10. 프로젝트 구조 확인
print("\n📋 프로젝트 구조")
run_cmd("ls -la", "파일 목록")

# 11. 데이터 확인
print("\n📊 데이터 확인")
if os.path.exists('data'):
    run_cmd("ls -la data/", "데이터 디렉토리")
else:
    print("⚠️ data 디렉토리 없음 (정상 - 나중에 추가됨)")

# 12. 완료 메시지
print("\n" + "="*50)
print("🎉 구글 코랩 셋업 완료!")
print("="*50)
print("\n📚 다음 단계:")
print("1. 데이터 로딩 및 EDA 시작")
print("2. notebooks/member/ 폴더에 작업 저장")
print("3. GitHub Issues에서 일일 보고서 작성")
print("\n💡 매일 작업 시작 전:")
print("   %cd /content/final")
print("   !git pull origin main")
print("\n📤 작업 완료 후:")
print("   !git add notebooks/member/")
print("   !git commit -m '작업 설명'")
print("   !git push origin main")
print("\n🆘 문제 시: https://github.com/Deok-Kawn/final/issues/2")
print("\n🔥 화이팅!")

# 추가: 현재 상태 최종 확인
print("\n🔍 최종 상태 확인:")
try:
    import pandas as pd
    import numpy as np
    print("✅ pandas, numpy 사용 가능")
except ImportError as e:
    print(f"⚠️ 라이브러리 import 오류: {e}")

print(f"✅ 현재 디렉토리: {os.getcwd()}")
print(f"✅ Python 버전: {sys.version}")

# torch 확인
try:
    import torch
    print(f"✅ PyTorch: {torch.__version__}")
    print(f"✅ CUDA 사용 가능: {torch.cuda.is_available()}")
except ImportError:
    print("⚠️ PyTorch 설치 필요 (!pip install torch)") 