#!/usr/bin/env python
"""
딥러닝 대회 팀 프로젝트 환경 설정 자동화 스크립트

사용법:
    python setup_environment.py

기능:
- 필수 디렉토리 생성
- 환경 확인
- Git hooks 설정 (선택사항)
- 설정 파일 생성
"""

import os
import sys
import subprocess
from pathlib import Path
import platform


class EnvironmentSetup:
    """환경 설정 자동화 클래스"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        
    def print_banner(self):
        """환영 메시지 출력"""
        print("🚀" * 50)
        print("   딥러닝 대회 팀 프로젝트 환경 설정")
        print("🚀" * 50)
        print(f"📍 프로젝트 루트: {self.project_root}")
        print(f"🐍 Python 버전: {self.python_version}")
        print(f"💻 운영체제: {platform.system()} {platform.release()}")
        print()
    
    def create_directories(self):
        """필수 디렉토리 생성"""
        print("📁 필수 디렉토리 생성 중...")
        
        required_dirs = [
            'experiments',
            'logs',
            'outputs',
            'models/baseline',
            'models/lstm', 
            'models/ensemble',
            'data/processed',
            'data/external',
            'notebooks/experiments'
        ]
        
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {dir_path}")
        
        # .gitkeep 파일 생성 (빈 디렉토리를 git에서 추적하기 위해)
        gitkeep_dirs = ['experiments', 'logs', 'outputs']
        for dir_name in gitkeep_dirs:
            gitkeep_file = self.project_root / dir_name / '.gitkeep'
            gitkeep_file.touch()
        
        print("✅ 디렉토리 생성 완료!\n")
    
    def check_dependencies(self):
        """의존성 확인"""
        print("📦 의존성 라이브러리 확인 중...")
        
        required_packages = [
            'pandas', 'numpy', 'matplotlib', 'seaborn', 
            'scikit-learn', 'torch', 'jupyter'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"  ✓ {package}")
            except ImportError:
                print(f"  ❌ {package} - 설치 필요")
                missing_packages.append(package)
        
        if missing_packages:
            print(f"\n⚠️  누락된 패키지: {', '.join(missing_packages)}")
            print("다음 명령어로 설치하세요:")
            print(f"pip install -r requirements_python36.txt")
        else:
            print("✅ 모든 필수 패키지가 설치되어 있습니다!\n")
        
        return len(missing_packages) == 0
    
    def setup_git_config(self):
        """Git 설정 (선택사항)"""
        print("🔧 Git 설정...")
        
        try:
            # Git이 설치되어 있는지 확인
            subprocess.run(['git', '--version'], capture_output=True, check=True)
            
            # 기본 브랜치가 main인지 확인
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True)
            current_branch = result.stdout.strip()
            
            if current_branch != 'main' and current_branch != '':
                print(f"  📌 현재 브랜치: {current_branch}")
            
            print("  ✓ Git 설정 확인 완료")
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("  ⚠️ Git이 설치되어 있지 않거나 Git 저장소가 초기화되지 않았습니다.")
        
        print()
    
    def create_config_files(self):
        """설정 파일 생성"""
        print("⚙️ 설정 파일 생성 중...")
        
        # Jupyter 설정 생성
        jupyter_config = """
# Jupyter 노트북 설정
c.NotebookApp.open_browser = False
c.NotebookApp.port = 8888
c.NotebookApp.notebook_dir = 'notebooks'
"""
        
        config_dir = self.project_root / '.jupyter'
        config_dir.mkdir(exist_ok=True)
        
        # VS Code 설정
        vscode_settings = {
            "python.defaultInterpreterPath": "python",
            "python.linting.enabled": True,
            "python.linting.pylintEnabled": True,
            "python.formatting.provider": "black",
            "files.exclude": {
                "**/__pycache__": True,
                "**/*.pyc": True,
                ".pytest_cache": True,
                "**/.ipynb_checkpoints": True
            },
            "jupyter.askForKernelRestart": False
        }
        
        vscode_dir = self.project_root / '.vscode'
        vscode_dir.mkdir(exist_ok=True)
        
        import json
        with open(vscode_dir / 'settings.json', 'w') as f:
            json.dump(vscode_settings, f, indent=2)
        
        print("  ✓ VS Code 설정 파일 생성")
        print("  ✓ Jupyter 설정 준비")
        print("✅ 설정 파일 생성 완료!\n")
    
    def run_environment_test(self):
        """환경 테스트 실행"""
        print("🧪 환경 테스트 실행 중...")
        
        test_file = self.project_root / 'test_environment.py'
        if test_file.exists():
            try:
                result = subprocess.run([sys.executable, str(test_file)], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print("  ✅ 환경 테스트 통과!")
                else:
                    print("  ⚠️ 환경 테스트에서 일부 문제 발견:")
                    print(result.stdout)
            except Exception as e:
                print(f"  ❌ 환경 테스트 실행 중 오류: {e}")
        else:
            print("  ⚠️ test_environment.py 파일을 찾을 수 없습니다.")
        
        print()
    
    def show_next_steps(self):
        """다음 단계 안내"""
        print("🎯 다음 단계:")
        print("1. notebooks/00_quick_start_guide.ipynb 실행")
        print("2. docs/TEAM_GUIDELINES.md 문서 읽기")
        print("3. 개별 브랜치 생성하여 작업 시작")
        print("4. 실험 결과는 ExperimentTracker로 기록")
        print()
        print("📚 주요 명령어:")
        print("  - 노트북 시작: jupyter notebook")
        print("  - 환경 테스트: python test_environment.py")
        print("  - 새 브랜치: git checkout -b feature/your-feature")
        print()
        print("❓ 문제가 있으면 GitHub Issues에 등록하거나 팀에 문의하세요!")
        print("🚀" * 50)
    
    def run_setup(self):
        """전체 설정 프로세스 실행"""
        self.print_banner()
        
        # 1. 디렉토리 생성
        self.create_directories()
        
        # 2. 의존성 확인
        deps_ok = self.check_dependencies()
        
        # 3. Git 설정
        self.setup_git_config()
        
        # 4. 설정 파일 생성
        self.create_config_files()
        
        # 5. 환경 테스트 (의존성이 OK인 경우에만)
        if deps_ok:
            self.run_environment_test()
        
        # 6. 다음 단계 안내
        self.show_next_steps()


if __name__ == "__main__":
    setup = EnvironmentSetup()
    setup.run_setup() 