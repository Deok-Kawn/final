#!/usr/bin/env python3
"""
EDA 마스터 실행 스크립트
======================
모든 EDA 분석을 순차적으로 실행하는 통합 스크립트입니다.

Author: Time Series Forecasting Team
Date: 2024-01-01
Python Version: 3.6.9
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def print_header(title):
    """섹션 헤더 출력"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def run_script(script_path, script_name):
    """스크립트 실행 및 결과 모니터링"""
    print(f"\n▶️ {script_name} 실행 중...")
    start_time = time.time()
    
    try:
        # Python 3.6.9 호환성을 위해 subprocess.run 대신 사용
        result = subprocess.call([sys.executable, script_path])
        
        elapsed_time = time.time() - start_time
        
        if result == 0:
            print(f"✅ {script_name} 완료! (실행시간: {elapsed_time:.2f}초)")
            return True
        else:
            print(f"❌ {script_name} 실행 실패! (종료 코드: {result})")
            return False
            
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"❌ {script_name} 실행 중 오류 발생: {e}")
        print(f"   실행시간: {elapsed_time:.2f}초")
        return False

def main():
    """메인 실행 함수"""
    print_header("EDA 통합 분석 시작")
    
    # 현재 디렉토리 확인
    current_dir = Path.cwd()
    print(f"현재 작업 디렉토리: {current_dir}")
    
    # EDA 스크립트 순서
    eda_scripts = [
        ("01_data_loading_and_validation.py", "데이터 로딩 및 검증"),
        ("02_basic_statistical_summary.py", "기본 통계 분석"),
        ("03_time_series_visualization.py", "시계열 시각화")
    ]
    
    # 결과 추적
    results = {}
    total_start_time = time.time()
    
    # 순차 실행
    for script_file, script_desc in eda_scripts:
        script_path = current_dir / script_file
        
        if not script_path.exists():
            print(f"❌ 파일을 찾을 수 없음: {script_path}")
            results[script_desc] = False
            continue
            
        success = run_script(script_path, script_desc)
        results[script_desc] = success
        
        if not success:
            print(f"⚠️ {script_desc} 실패 - 계속 진행합니다...")
    
    # 최종 결과 요약
    total_elapsed_time = time.time() - total_start_time
    
    print_header("EDA 분석 완료 요약")
    
    success_count = sum(results.values())
    total_count = len(results)
    
    print(f"📊 전체 실행 시간: {total_elapsed_time:.2f}초")
    print(f"📈 성공률: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    print(f"\n📋 각 단계별 결과:")
    for script_desc, success in results.items():
        status = "✅ 성공" if success else "❌ 실패"
        print(f"  • {script_desc}: {status}")
    
    # 출력 파일 확인
    outputs_dir = current_dir.parent.parent / "outputs"
    if outputs_dir.exists():
        png_files = list(outputs_dir.glob("*.png"))
        print(f"\n📁 생성된 시각화 파일: {len(png_files)}개")
        for png_file in sorted(png_files):
            print(f"  • {png_file.name}")
    
    # 최종 메시지
    if success_count == total_count:
        print(f"\n🎉 모든 EDA 분석이 성공적으로 완료되었습니다!")
        print(f"📊 outputs/ 디렉토리에서 결과를 확인하세요.")
    else:
        print(f"\n⚠️ 일부 분석에서 오류가 발생했습니다.")
        print(f"❓ 개별 스크립트를 직접 실행하여 문제를 확인해보세요.")
    
    return success_count == total_count

if __name__ == "__main__":
    # 스크립트 정보
    print("EDA 마스터 실행 스크립트 v1.0")
    print("Python 버전:", sys.version)
    print("실행 시작:", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    # 메인 실행
    success = main()
    
    # 종료 코드
    sys.exit(0 if success else 1) 