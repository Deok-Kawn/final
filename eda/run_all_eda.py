#!/usr/bin/env python3
"""
EDA 마스터 실행 스크립트
======================
모든 EDA 분석을 순차적으로 실행하는 통합 스크립트입니다.

Author: Time Series Forecasting Team
Date: 2025-06-06
Python Version: 3.10+
TaskMaster Tasks: 2.1-2.7
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def print_header(title):
    """섹션 헤더 출력"""
    print("\n" + "="*70)
    print(f"🎯 {title}")
    print("="*70)

def run_script(script_path, script_name):
    """스크립트 실행 및 결과 모니터링"""
    print(f"\n▶️ {script_name} 실행 중...")
    start_time = time.time()
    
    try:
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
    print_header("전체 EDA 통합 분석 시작 🚀")
    
    # 현재 디렉토리 확인
    current_dir = Path.cwd()
    print(f"현재 작업 디렉토리: {current_dir}")
    
    # 전체 EDA 스크립트 순서 (업데이트된 목록)
    eda_scripts = [
        ("01_data_loading_and_validation.py", "1️⃣ 데이터 로딩 및 검증"),
        ("02_basic_statistical_summary.py", "2️⃣ 기본 통계 분석"),
        ("03_time_series_visualization.py", "3️⃣ 시계열 시각화"),
        ("04_correlation_analysis.py", "4️⃣ 상관관계 분석 & 피처 엔지니어링"),
        ("05_missing_values_analysis.py", "5️⃣ 누락값 상세 분석"),
        ("05b_check_missing_dates.py", "5️⃣b 누락된 날짜 확인"),
        ("06_advanced_timeseries_analysis.py", "6️⃣ 고급 시계열 분석 (정상성/자기상관)"),
        ("07_external_factors_analysis.py", "7️⃣ 외부 요인 & 특별 이벤트 분석")
    ]
    
    # 결과 추적
    results = {}
    total_start_time = time.time()
    
    print(f"\n📋 실행 예정 스크립트: {len(eda_scripts)}개")
    for i, (script_file, script_desc) in enumerate(eda_scripts, 1):
        print(f"   {i}. {script_desc}")
    
    # 순차 실행
    for i, (script_file, script_desc) in enumerate(eda_scripts, 1):
        print_header(f"단계 {i}/{len(eda_scripts)}: {script_desc}")
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
    
    print_header("🎯 EDA 분석 완료 요약 보고서")
    
    success_count = sum(results.values())
    total_count = len(results)
    
    print(f"⏱️ 전체 실행 시간: {total_elapsed_time:.2f}초 ({total_elapsed_time/60:.1f}분)")
    print(f"📊 성공률: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    print(f"\n📋 각 단계별 실행 결과:")
    for i, (script_desc, success) in enumerate(results.items(), 1):
        status = "✅ 성공" if success else "❌ 실패"
        print(f"   {i:2d}. {script_desc}: {status}")
    
    # 결과 파일 확인
    results_dir = current_dir.parent / "results" / "eda"
    if results_dir.exists():
        print(f"\n📁 생성된 결과 파일 요약:")
        
        # 각 카테고리별 파일 수 확인
        categories = {
            "01_basic_eda": "기본 EDA 시각화",
            "02_correlation_analysis": "상관관계 분석",
            "03_missing_values": "누락값 분석",
            "04_advanced_timeseries": "고급 시계열 분석",
            "05_external_factors": "외부 요인 분석"
        }
        
        total_files = 0
        for category, description in categories.items():
            category_dir = results_dir / category
            if category_dir.exists():
                files = list(category_dir.glob("*"))
                file_count = len(files)
                total_files += file_count
                print(f"   📊 {description}: {file_count}개 파일")
        
        print(f"\n🎯 총 생성 파일: {total_files}개")
        print(f"📂 결과 위치: {results_dir}")
    
    # 최종 메시지
    if success_count == total_count:
        print(f"\n🎉 모든 EDA 분석이 성공적으로 완료되었습니다!")
        print(f"📊 results/eda/ 디렉토리에서 결과를 확인하세요.")
        print(f"📈 다음 단계: Task 3 (데이터 전처리 파이프라인)")
    else:
        failed_count = total_count - success_count
        print(f"\n⚠️ {failed_count}개 분석에서 오류가 발생했습니다.")
        print(f"❓ 개별 스크립트를 직접 실행하여 문제를 확인해보세요.")
        print(f"💡 가상환경 활성화 및 패키지 설치를 확인하세요:")
        print(f"   source venv/bin/activate")
        print(f"   pip install -r requirements.txt")
    
    return success_count == total_count

if __name__ == "__main__":
    # 스크립트 정보
    print("="*70)
    print("🎯 EDA 마스터 실행 스크립트 v2.0")
    print("📅 시계열 전력수급 데이터 탐색적 분석")
    print("👥 Time Series Forecasting Team - Deep Learning Competition")
    print("="*70)
    print("🐍 Python 버전:", sys.version.split()[0])
    print("⏰ 실행 시작:", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    # 메인 실행
    success = main()
    
    print(f"\n⏰ 실행 종료: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # 종료 코드
    sys.exit(0 if success else 1) 