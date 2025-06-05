# 🚀 구글 코랩 완전 셋업 스크립트
# 이 셀을 코랩에서 실행하면 모든 설정이 자동으로 완료됩니다.

import os
import subprocess
import sys

def run_command(command, description=""):
    """명령어 실행 및 결과 출력"""
    if description:
        print(f"📋 {description}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ 성공: {command}")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ 실패: {command}")
            print(f"오류: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 예외 발생: {e}")
        return False

def setup_project():
    """프로젝트 셋업 메인 함수"""
    print("🚀 시계열 예측 프로젝트 셋업 시작")
    print("=" * 50)
    
    # 1. 기존 디렉토리 정리
    if os.path.exists('final'):
        print("🧹 기존 final 디렉토리 제거")
        run_command("rm -rf final")
    
    if os.path.exists('final-main'):
        print("🧹 기존 final-main 디렉토리 제거")
        run_command("rm -rf final-main")
    
    # 2. ZIP 파일로 다운로드 (가장 안정적)
    print("\n📥 GitHub에서 프로젝트 다운로드")
    success = run_command(
        "wget -q https://github.com/Deok-Kawn/final/archive/refs/heads/main.zip",
        "ZIP 파일 다운로드"
    )
    
    if not success:
        print("❌ 다운로드 실패. 다른 방법 시도...")
        # 대안: curl 사용
        success = run_command(
            "curl -L -o main.zip https://github.com/Deok-Kawn/final/archive/refs/heads/main.zip",
            "curl로 다운로드 재시도"
        )
    
    if not success:
        print("❌ 모든 다운로드 방법 실패")
        return False
    
    # 3. 압축 해제
    print("\n📦 압축 해제")
    if not run_command("unzip -q main.zip", "ZIP 파일 압축 해제"):
        return False
    
    # 4. 디렉토리명 변경
    print("\n📁 디렉토리 설정")
    if not run_command("mv final-main final", "디렉토리명 변경"):
        return False
    
    # 5. 디렉토리 이동
    os.chdir('final')
    print(f"📍 현재 위치: {os.getcwd()}")
    
    # 6. Git 설정
    print("\n🔧 Git 설정")
    run_command('git config --global user.name "Deok-Kwan"', "Git 사용자명 설정")
    run_command('git config --global user.email "your.email@example.com"', "Git 이메일 설정")
    
    # 7. Git 저장소 초기화 (선택사항)
    print("\n🔗 Git 저장소 연결")
    run_command("git init", "Git 초기화")
    run_command("git remote add origin https://github.com/Deok-Kawn/final.git", "원격 저장소 연결")
    
    # 8. 프로젝트 구조 확인
    print("\n📋 프로젝트 구조 확인")
    run_command("ls -la", "파일 목록 확인")
    
    # 9. Python 환경 확인
    print("\n🐍 Python 환경 확인")
    print(f"Python 버전: {sys.version}")
    print(f"현재 작업 디렉토리: {os.getcwd()}")
    
    # 10. 필수 라이브러리 설치
    print("\n📚 필수 라이브러리 설치")
    
    # requirements.txt 확인
    if os.path.exists('requirements_python36.txt'):
        print("📄 requirements_python36.txt 발견")
        run_command("pip install -r requirements_python36.txt", "requirements 설치")
    else:
        print("📄 requirements 파일 없음. 기본 라이브러리 설치")
        libraries = [
            "pandas", "numpy", "matplotlib", "seaborn", 
            "scikit-learn", "torch", "plotly"
        ]
        for lib in libraries:
            run_command(f"pip install {lib}", f"{lib} 설치")
    
    # 11. 데이터 디렉토리 확인
    print("\n📊 데이터 확인")
    if os.path.exists('data'):
        run_command("ls -la data/", "데이터 파일 확인")
    else:
        print("⚠️ data 디렉토리가 없습니다.")
    
    # 12. 최종 확인
    print("\n✅ 셋업 완료!")
    print("=" * 50)
    print("🎉 이제 다음 단계를 진행하세요:")
    print("1. notebooks/00_quick_start_guide.ipynb 실행")
    print("2. 데이터 로딩 및 EDA 시작")
    print("3. 모델 개발 진행")
    
    return True

# 셋업 실행
if __name__ == "__main__":
    setup_project() 