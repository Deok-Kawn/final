# %%
"""
Task 2.1: Load and Validate CSV Data
=====================================
시계열 전력수급 데이터를 로딩하고 기본 검증을 수행합니다.

Author: Time Series Forecasting Team
Date: 2024-01-01
Python Version: 3.6.9
"""

# %%
# =============================================================================
# 1. 라이브러리 임포트
# =============================================================================

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# 데이터 타입 및 메모리 체크를 위한 라이브러리
import warnings
warnings.filterwarnings('ignore')

print("Python 버전:", sys.version)
print("Pandas 버전:", pd.__version__)
print("NumPy 버전:", np.__version__)

# %%
# =============================================================================
# 2. 데이터 파일 경로 설정 및 확인
# =============================================================================

# 프로젝트 루트 디렉토리 설정
project_root = Path.cwd()
print(f"현재 작업 디렉토리: {project_root}")

# 데이터 파일명
data_filename = "data.csv"
submission_filename = "submission_sample.csv"

# 여러 경로에서 데이터 파일을 찾는 함수
def find_data_files(filename):
    """여러 가능한 경로에서 데이터 파일을 찾습니다."""
    possible_paths = [
        project_root / filename,                    # 현재 디렉토리
        project_root / "data" / filename,           # 현재/data/
        project_root.parent / filename,             # 상위 디렉토리
        project_root.parent / "data" / filename,    # 상위/data/
        Path("/timeseries/data") / filename,        # 절대경로1
        Path("/data/timeseries/data") / filename,   # 절대경로2
    ]
    
    for path in possible_paths:
        if path.exists():
            print(f"✅ 파일 발견: {path}")
            return path
    
    print(f"❌ 파일을 찾을 수 없음: {filename}")
    print("시도한 경로들:")
    for path in possible_paths:
        print(f"  - {path}")
    return None

# 데이터 파일 위치 찾기
print("\n=== 데이터 파일 탐색 ===")
data_file = find_data_files(data_filename)
submission_file = find_data_files(submission_filename)

if data_file:
    data_dir = data_file.parent
    print(f"\n📁 데이터 디렉토리 확정: {data_dir}")
    print(f"📄 주요 데이터 파일: {data_file}")
    print(f"📄 제출 샘플 파일: {submission_file}")
    
    # 파일 크기 확인
    file_size = data_file.stat().st_size / 1024  # KB 단위
    print(f"📊 파일 크기: {file_size:.1f} KB")
else:
    print("❌ 데이터 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
    # 현재 디렉토리의 파일 목록 출력
    print(f"\n현재 디렉토리 ({project_root}) 파일 목록:")
    try:
        for item in project_root.iterdir():
            print(f"  {item.name} {'(디렉토리)' if item.is_dir() else ''}")
    except:
        print("  디렉토리를 읽을 수 없습니다.")

# %%
# =============================================================================
# 3. CSV 데이터 로딩
# =============================================================================

print("\n=== 데이터 로딩 중... ===")

# 데이터 파일이 존재하지 않으면 스크립트 종료
if not data_file or not data_file.exists():
    print("❌ 데이터 파일을 찾을 수 없어 로딩을 중단합니다.")
    print("파일 경로를 확인하고 다시 실행해주세요.")
    sys.exit(1)

try:
    # 인코딩 자동 감지를 위한 여러 시도
    encodings = ['utf-8', 'euc-kr', 'cp949', 'utf-8-sig']
    df = None
    
    for encoding in encodings:
        try:
            print(f"인코딩 '{encoding}' 시도 중...")
            df = pd.read_csv(data_file, encoding=encoding)
            print(f"✅ 인코딩 '{encoding}'으로 성공적으로 로딩!")
            break
        except UnicodeDecodeError:
            print(f"❌ 인코딩 '{encoding}' 실패")
            continue
    
    if df is None:
        raise ValueError("모든 인코딩 시도 실패")
        
    print(f"\n데이터 로딩 완료!")
    print(f"총 행 수: {len(df):,}")
    print(f"총 열 수: {df.shape[1]}")
    
except Exception as e:
    print(f"❌ 데이터 로딩 실패: {e}")
    sys.exit(1)

# %%
# =============================================================================
# 4. 기본 데이터 구조 확인
# =============================================================================

print("=== 기본 데이터 구조 확인 ===")

# 데이터프레임 기본 정보
print(f"데이터 형태 (행, 열): {df.shape}")
print(f"메모리 사용량: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")

print("\n=== 컬럼 정보 ===")
print(f"컬럼 수: {len(df.columns)}")
print("컬럼 목록:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

print("\n=== 데이터 타입 ===")
print(df.dtypes)

# %%
# =============================================================================
# 5. 첫 몇 행 데이터 확인
# =============================================================================

print("=== 첫 5행 데이터 ===")
print(df.head())

print("\n=== 마지막 5행 데이터 ===")
print(df.tail())

# 데이터 샘플링 (중간 부분)
print(f"\n=== 중간 부분 데이터 (행 {len(df)//2-2} ~ {len(df)//2+2}) ===")
mid_idx = len(df) // 2
print(df.iloc[mid_idx-2:mid_idx+3])

# %%
# =============================================================================
# 6. 날짜 컬럼 식별 및 검증
# =============================================================================

print("=== 날짜 컬럼 식별 ===")

# 날짜로 추정되는 컬럼 찾기
date_columns = []
for col in df.columns:
    if any(keyword in col.lower() for keyword in ['date', '날짜', '일자', '년', '월', '일']):
        date_columns.append(col)
        
print(f"날짜 관련 컬럼: {date_columns}")

# 첫 번째 컬럼이 날짜일 가능성이 높음
if len(df.columns) > 0:
    first_col = df.columns[0]
    print(f"\n첫 번째 컬럼 '{first_col}' 샘플:")
    print(df[first_col].head(10).values)
    
    # 날짜 변환 시도
    try:
        date_sample = pd.to_datetime(df[first_col].head())
        print(f"✅ 날짜 변환 성공!")
        print(f"변환된 날짜 샘플:\n{date_sample}")
    except:
        print(f"❌ 날짜 변환 실패 - 수동 처리 필요")

# %%
# =============================================================================
# 7. 누락값 검사
# =============================================================================

print("=== 누락값 검사 ===")

# 전체 누락값 통계
total_missing = df.isnull().sum().sum()
total_cells = df.shape[0] * df.shape[1]
missing_percentage = (total_missing / total_cells) * 100

print(f"전체 누락값: {total_missing:,} / {total_cells:,} ({missing_percentage:.2f}%)")

# 컬럼별 누락값
print("\n=== 컬럼별 누락값 ===")
missing_by_col = df.isnull().sum()
missing_by_col = missing_by_col[missing_by_col > 0].sort_values(ascending=False)

if len(missing_by_col) > 0:
    print("누락값이 있는 컬럼:")
    for col, count in missing_by_col.items():
        percentage = (count / len(df)) * 100
        print(f"  {col}: {count:,} ({percentage:.2f}%)")
else:
    print("✅ 누락값이 없습니다!")

# %%
# =============================================================================
# 8. 중복값 검사
# =============================================================================

print("=== 중복값 검사 ===")

# 전체 행 중복 검사
duplicate_rows = df.duplicated().sum()
print(f"완전 중복 행: {duplicate_rows:,}")

# 날짜 중복 검사 (첫 번째 컬럼이 날짜라고 가정)
if len(df.columns) > 0:
    first_col = df.columns[0]
    duplicate_dates = df[first_col].duplicated().sum()
    print(f"첫 번째 컬럼 '{first_col}' 중복값: {duplicate_dates:,}")

# %%
# =============================================================================
# 9. 숫자형 컬럼 식별 및 기본 통계
# =============================================================================

print("=== 숫자형 컬럼 식별 ===")

# 숫자형 컬럼 추출
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
print(f"숫자형 컬럼 ({len(numeric_columns)}개): {numeric_columns}")

# 비숫자형 컬럼
non_numeric_columns = df.select_dtypes(exclude=[np.number]).columns.tolist()
print(f"비숫자형 컬럼 ({len(non_numeric_columns)}개): {non_numeric_columns}")

if len(numeric_columns) > 0:
    print(f"\n=== 숫자형 컬럼 기본 통계 ===")
    print(df[numeric_columns].describe())

# %%
# =============================================================================
# 10. 데이터 범위 및 이상값 초기 검사
# =============================================================================

print("=== 데이터 범위 검사 ===")

if len(numeric_columns) > 0:
    for col in numeric_columns:
        series = df[col].dropna()
        if len(series) > 0:
            print(f"\n컬럼: {col}")
            print(f"  최솟값: {series.min():,.2f}")
            print(f"  최댓값: {series.max():,.2f}")
            print(f"  평균: {series.mean():,.2f}")
            print(f"  중앙값: {series.median():,.2f}")
            print(f"  표준편차: {series.std():,.2f}")
            
            # 음수값 검사 (전력 데이터에서는 일반적으로 양수)
            negative_count = (series < 0).sum()
            if negative_count > 0:
                print(f"  ⚠️ 음수값 발견: {negative_count}개")
            
            # 0값 검사
            zero_count = (series == 0).sum()
            if zero_count > 0:
                print(f"  ⚠️ 0값 발견: {zero_count}개")

# %%
# =============================================================================
# 11. 제출 샘플 파일 확인
# =============================================================================

print("=== 제출 샘플 파일 확인 ===")

if submission_file.exists():
    try:
        submission_df = pd.read_csv(submission_file, encoding='utf-8')
        print(f"제출 샘플 형태: {submission_df.shape}")
        print(f"제출 샘플 컬럼: {submission_df.columns.tolist()}")
        print(f"\n제출 샘플 첫 5행:")
        print(submission_df.head())
        print(f"\n제출 샘플 마지막 5행:")
        print(submission_df.tail())
    except Exception as e:
        print(f"❌ 제출 샘플 파일 로딩 실패: {e}")
else:
    print("❌ 제출 샘플 파일이 존재하지 않습니다.")

# %%
# =============================================================================
# 12. 데이터 검증 요약 및 다음 단계 제언
# =============================================================================

print("=" * 60)
print("🎯 데이터 로딩 및 검증 완료 요약")
print("=" * 60)

print(f"✅ 데이터 성공적으로 로딩: {df.shape[0]:,}행 × {df.shape[1]}열")
print(f"✅ 메모리 사용량: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
print(f"✅ 누락값 비율: {missing_percentage:.2f}%")
print(f"✅ 중복 행: {duplicate_rows:,}개")
print(f"✅ 숫자형 컬럼: {len(numeric_columns)}개")

print(f"\n📋 다음 단계 제언:")
print(f"1. 날짜 컬럼 정확한 파싱 및 인덱스 설정")
print(f"2. 시계열 데이터 연속성 확인")
print(f"3. 계절성 및 트렌드 패턴 분석")
print(f"4. 이상값 탐지 및 처리 방안 수립")

# 전역 변수로 저장하여 다음 스크립트에서 사용 가능하게 함
print(f"\n💾 데이터 전역 변수 'df'로 저장 완료")
print(f"   사용법: df.head(), df.info(), df.describe() 등")

# %%
# =============================================================================
# 13. 환경 검증 및 호환성 확인
# =============================================================================

print("\n=== 환경 검증 ===")

# Python 3.6.9 호환성 확인
python_version = sys.version_info
print(f"Python 버전: {python_version.major}.{python_version.minor}.{python_version.micro}")

if python_version >= (3, 6) and python_version < (3, 7):
    print("✅ Python 3.6.x 환경 확인됨")
elif python_version >= (3, 7):
    print("⚠️ Python 3.7+ 환경 - 일부 기능 차이 가능")
else:
    print("❌ Python 3.6 미만 - 업그레이드 권장")

# 필수 패키지 버전 확인
required_packages = {
    'pandas': '1.1.5',
    'numpy': '1.19.5'
}

print(f"\n=== 패키지 버전 호환성 ===")
for package, required_version in required_packages.items():
    if package == 'pandas':
        current_version = pd.__version__
    elif package == 'numpy':
        current_version = np.__version__
    
    print(f"{package}: {current_version} (권장: {required_version})")

print(f"\n🎉 Task 2.1 완료!")
print(f"다음 단계: Task 2.2 - Generate Basic Statistical Summary") 