#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🧪 시계열 예측 프로젝트 환경 테스트 스크립트
Target: Python 3.6.9 (default, Jan 26 2021, 15:33:00) [GCC 8.4.0]
"""

import sys
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 색상 출력을 위한 상수
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


class EnvironmentTester:
    """환경 테스트 클래스"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.tests_passed = 0
        self.tests_failed = 0
        self.warnings_count = 0
    
    def print_header(self):
        """테스트 헤더 출력"""
        print(f"{Colors.BLUE}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}🧪 딥러닝 팀 프로젝트 환경 테스트{Colors.END}")
        print(f"{Colors.BLUE}{'='*60}{Colors.END}")
        print(f"📍 프로젝트 루트: {self.project_root}")
        print(f"🐍 Python 버전: {sys.version}")
        print()
    
    def test_package(self, package_name, test_name=None):
        """패키지 임포트 테스트"""
        test_name = test_name or package_name
        try:
            __import__(package_name)
            self.print_success(f"{test_name} 임포트")
            return True
        except ImportError as e:
            self.print_error(f"{test_name} 임포트", str(e))
            return False
    
    def test_required_packages(self):
        """필수 패키지 테스트"""
        print(f"{Colors.BOLD}📦 필수 패키지 테스트{Colors.END}")
        
        packages = [
            ('pandas', 'Pandas'),
            ('numpy', 'NumPy'),
            ('matplotlib', 'Matplotlib'),
            ('seaborn', 'Seaborn'),
            ('sklearn', 'Scikit-learn'),
            ('torch', 'PyTorch'),
            ('jupyter', 'Jupyter')
        ]
        
        all_passed = True
        for package, name in packages:
            if not self.test_package(package, name):
                all_passed = False
        
        print()
        return all_passed
    
    def test_optional_packages(self):
        """선택적 패키지 테스트"""
        print(f"{Colors.BOLD}📦 선택적 패키지 테스트{Colors.END}")
        
        optional_packages = [
            ('statsmodels', 'Statsmodels'),
            ('scipy', 'SciPy'),
            ('plotly', 'Plotly'),
            ('tensorboard', 'TensorBoard')
        ]
        
        for package, name in optional_packages:
            if not self.test_package(package, name):
                self.print_warning(f"{name}이 설치되지 않음 (선택사항)")
        
        print()
    
    def test_project_structure(self):
        """프로젝트 구조 테스트"""
        print(f"{Colors.BOLD}📁 프로젝트 구조 테스트{Colors.END}")
        
        required_dirs = [
            'src',
            'src/data',
            'src/features', 
            'src/models',
            'src/utils',
            'data',
            'notebooks',
            'docs'
        ]
        
        required_files = [
            'README.md',
            'requirements_python36.txt',
            'src/__init__.py',
            'src/data/__init__.py',
            'src/features/__init__.py',
            'src/models/__init__.py',
            'src/utils/__init__.py'
        ]
        
        all_passed = True
        
        # 디렉토리 확인
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if full_path.exists() and full_path.is_dir():
                self.print_success(f"디렉토리 {dir_path}")
            else:
                self.print_error(f"디렉토리 {dir_path}", "존재하지 않음")
                all_passed = False
        
        # 파일 확인
        for file_path in required_files:
            full_path = self.project_root / file_path
            if full_path.exists() and full_path.is_file():
                self.print_success(f"파일 {file_path}")
            else:
                self.print_error(f"파일 {file_path}", "존재하지 않음")
                all_passed = False
        
        print()
        return all_passed
    
    def test_module_imports(self):
        """프로젝트 모듈 임포트 테스트"""
        print(f"{Colors.BOLD}🔧 프로젝트 모듈 임포트 테스트{Colors.END}")
        
        # sys.path에 src 추가
        src_path = str(self.project_root / 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        modules_to_test = [
            ('data.loader', 'DataLoader'),
            ('features.engineering', 'TimeSeriesFeatureEngine'),
            ('models.base_model', 'BaseModel'),
            ('models.lstm_model', 'LSTMModel'),
            ('utils.experiment_tracker', 'ExperimentTracker'),
            ('utils.visualization', 'TimeSeriesVisualizer')
        ]
        
        all_passed = True
        for module_name, class_name in modules_to_test:
            try:
                module = __import__(module_name, fromlist=[class_name])
                getattr(module, class_name)
                self.print_success(f"{module_name}.{class_name}")
            except Exception as e:
                self.print_error(f"{module_name}.{class_name}", str(e))
                all_passed = False
        
        print()
        return all_passed
    
    def test_data_loading(self):
        """데이터 로딩 테스트"""
        print(f"{Colors.BOLD}📊 데이터 로딩 테스트{Colors.END}")
        
        try:
            # sys.path에 src 추가
            src_path = str(self.project_root / 'src')
            if src_path not in sys.path:
                sys.path.insert(0, src_path)
            
            from data.loader import DataLoader
            
            # 데이터 로더 초기화
            data_loader = DataLoader(data_dir=self.project_root / 'data')
            
            # 데이터 파일 존재 확인
            if (self.project_root / 'data' / 'power_consumption.csv').exists():
                data = data_loader.load_train_data()
                self.print_success(f"데이터 로딩 성공 (shape: {data.shape})")
                
                # 기본 정보 확인
                info = data_loader.get_basic_info()
                self.print_success("데이터 기본 정보 출력")
                
            else:
                self.print_warning("데이터 파일 없음 - 실제 데이터로 테스트 불가")
            
        except Exception as e:
            self.print_error("데이터 로딩", str(e))
            return False
        
        print()
        return True
    
    def test_pytorch_functionality(self):
        """PyTorch 기능 테스트"""
        print(f"{Colors.BOLD}🔥 PyTorch 기능 테스트{Colors.END}")
        
        try:
            import torch
            import torch.nn as nn
            
            # GPU 사용 가능 여부
            if torch.cuda.is_available():
                device = torch.device('cuda')
                gpu_name = torch.cuda.get_device_name(0)
                self.print_success(f"GPU 사용 가능: {gpu_name}")
            else:
                device = torch.device('cpu')
                self.print_warning("GPU 사용 불가 - CPU 모드")
            
            # 간단한 텐서 연산 테스트
            x = torch.randn(2, 3).to(device)
            y = torch.randn(3, 2).to(device)
            z = torch.mm(x, y)
            self.print_success(f"텐서 연산 테스트 ({device})")
            
            # 간단한 모델 테스트
            model = nn.Linear(10, 1).to(device)
            test_input = torch.randn(5, 10).to(device)
            output = model(test_input)
            self.print_success("신경망 모델 테스트")
            
        except Exception as e:
            self.print_error("PyTorch 기능", str(e))
            return False
        
        print()
        return True
    
    def test_visualization(self):
        """시각화 기능 테스트"""
        print(f"{Colors.BOLD}📈 시각화 기능 테스트{Colors.END}")
        
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            import numpy as np
            
            # 간단한 플롯 생성 (화면에 표시하지 않음)
            plt.ioff()  # 인터랙티브 모드 끄기
            
            fig, ax = plt.subplots(figsize=(8, 6))
            x = np.linspace(0, 10, 100)
            y = np.sin(x)
            ax.plot(x, y)
            ax.set_title('Test Plot')
            plt.close(fig)
            
            self.print_success("Matplotlib 플롯 생성")
            
            # Seaborn 테스트
            fig, ax = plt.subplots(figsize=(6, 4))
            data = np.random.randn(100)
            sns.histplot(data, ax=ax)
            plt.close(fig)
            
            self.print_success("Seaborn 시각화")
            
        except Exception as e:
            self.print_error("시각화", str(e))
            return False
        
        print()
        return True
    
    def print_success(self, test_name):
        """성공 메시지 출력"""
        print(f"  {Colors.GREEN}✓{Colors.END} {test_name}")
        self.tests_passed += 1
    
    def print_error(self, test_name, error_msg):
        """에러 메시지 출력"""
        print(f"  {Colors.RED}✗{Colors.END} {test_name}: {error_msg}")
        self.tests_failed += 1
    
    def print_warning(self, message):
        """경고 메시지 출력"""
        print(f"  {Colors.YELLOW}⚠{Colors.END} {message}")
        self.warnings_count += 1
    
    def print_summary(self):
        """테스트 요약 출력"""
        print(f"{Colors.BLUE}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}📋 테스트 요약{Colors.END}")
        print(f"{Colors.BLUE}{'='*60}{Colors.END}")
        
        total_tests = self.tests_passed + self.tests_failed
        
        print(f"총 테스트: {total_tests}")
        print(f"{Colors.GREEN}통과: {self.tests_passed}{Colors.END}")
        print(f"{Colors.RED}실패: {self.tests_failed}{Colors.END}")
        print(f"{Colors.YELLOW}경고: {self.warnings_count}{Colors.END}")
        
        if self.tests_failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 모든 테스트가 통과했습니다!{Colors.END}")
            print("딥러닝 팀 프로젝트를 시작할 준비가 되었습니다.")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}⚠️ 일부 테스트가 실패했습니다.{Colors.END}")
            print("실패한 항목들을 확인하고 해결해 주세요.")
        
        print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    
    def run_all_tests(self):
        """모든 테스트 실행"""
        self.print_header()
        
        # 1. 필수 패키지 테스트
        self.test_required_packages()
        
        # 2. 선택적 패키지 테스트
        self.test_optional_packages()
        
        # 3. 프로젝트 구조 테스트
        self.test_project_structure()
        
        # 4. 모듈 임포트 테스트
        self.test_module_imports()
        
        # 5. 데이터 로딩 테스트
        self.test_data_loading()
        
        # 6. PyTorch 기능 테스트
        self.test_pytorch_functionality()
        
        # 7. 시각화 기능 테스트
        self.test_visualization()
        
        # 8. 요약 출력
        self.print_summary()
        
        return self.tests_failed == 0


if __name__ == "__main__":
    tester = EnvironmentTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1) 