# %%
"""
Task 2.2: Generate Basic Statistical Summary
===========================================
시계열 전력수급 데이터의 기본 통계 요약을 생성하고 분석합니다.

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
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정 (matplotlib)
plt.rcParams['font.family'] = ['Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

print("=== 기본 통계 분석 모듈 로딩 완료 ===")
print(f"Pandas: {pd.__version__}")
print(f"NumPy: {np.__version__}")
print(f"Matplotlib: {plt.matplotlib.__version__}")
print(f"Seaborn: {sns.__version__}")

# %%
# =============================================================================
# 2. 데이터 로딩 (Task 2.1에서 검증된 경로 사용)
# =============================================================================

print("=== 데이터 로딩 ===")

# 프로젝트 루트 및 데이터 파일 경로 설정
project_root = Path.cwd()
data_filename = "일별최대전력수급(2005-2023).csv"

# 데이터 파일 찾기 함수 (Task 2.1에서 검증된 로직)
def find_data_files(filename):
    """여러 가능한 경로에서 데이터 파일을 찾습니다."""
    possible_paths = [
        project_root / filename,
        project_root / "data" / filename,
        project_root.parent / filename,
        project_root.parent / "data" / filename,
        Path("/timeseries/data") / filename,
        Path("/data/timeseries/data") / filename,
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    return None

# 데이터 로딩
data_file = find_data_files(data_filename)
if not data_file:
    print("❌ 데이터 파일을 찾을 수 없습니다!")
    exit(1)

print(f"📄 데이터 파일: {data_file}")

# CSV 로딩
try:
    df = pd.read_csv(data_file, encoding='utf-8')
    print(f"✅ 데이터 로딩 완료: {df.shape[0]:,}행 × {df.shape[1]}열")
except Exception as e:
    print(f"❌ 데이터 로딩 실패: {e}")
    exit(1)

# %%
# =============================================================================
# 3. 날짜 컬럼 처리 및 인덱스 설정
# =============================================================================

print("=== 날짜 처리 ===")

# 날짜 컬럼 변환
if 'date' in df.columns:
    print("날짜 컬럼 변환 중...")
    df['date'] = pd.to_datetime(df['date'], format='%Y.%m.%d')
    df.set_index('date', inplace=True)
    print(f"✅ 날짜 인덱스 설정 완료")
    print(f"날짜 범위: {df.index.min()} ~ {df.index.max()}")
    print(f"총 기간: {(df.index.max() - df.index.min()).days + 1}일")
else:
    print("❌ 'date' 컬럼을 찾을 수 없습니다!")

# %%
# =============================================================================
# 4. 기본 통계 정보 생성
# =============================================================================

print("=== 기본 통계 정보 ===")

# 수치형 컬럼 식별
numeric_cols = df.select_dtypes(include=[np.number]).columns
print(f"분석 대상 컬럼: {list(numeric_cols)}")

if len(numeric_cols) > 0:
    target_col = numeric_cols[0]  # 주요 타겟: 최대전력(MW)
    data_series = df[target_col]
    
    print(f"\n📊 '{target_col}' 기본 통계:")
    print(f"  • 총 데이터 포인트: {len(data_series):,}개")
    print(f"  • 평균: {data_series.mean():,.2f} MW")
    print(f"  • 중앙값: {data_series.median():,.2f} MW")
    print(f"  • 표준편차: {data_series.std():,.2f} MW")
    print(f"  • 최솟값: {data_series.min():,.2f} MW")
    print(f"  • 최댓값: {data_series.max():,.2f} MW")
    print(f"  • 범위: {data_series.max() - data_series.min():,.2f} MW")
    print(f"  • 변동계수: {(data_series.std() / data_series.mean()) * 100:.2f}%")

# %%
# =============================================================================
# 5. 분위수 및 백분위수 분석
# =============================================================================

print("=== 분위수 분석 ===")

if len(numeric_cols) > 0:
    # 사분위수
    q25 = data_series.quantile(0.25)
    q50 = data_series.quantile(0.50)
    q75 = data_series.quantile(0.75)
    iqr = q75 - q25
    
    print(f"\n📈 분위수 정보:")
    print(f"  • Q1 (25%): {q25:,.2f} MW")
    print(f"  • Q2 (50%, 중앙값): {q50:,.2f} MW")
    print(f"  • Q3 (75%): {q75:,.2f} MW")
    print(f"  • IQR (Q3-Q1): {iqr:,.2f} MW")
    
    # 주요 백분위수
    percentiles = [1, 5, 10, 90, 95, 99]
    print(f"\n📊 주요 백분위수:")
    for p in percentiles:
        value = data_series.quantile(p/100)
        print(f"  • {p:2d}%: {value:,.2f} MW")

# %%
# =============================================================================
# 6. 연도별 통계 분석
# =============================================================================

print("=== 연도별 통계 분석 ===")

if 'date' in df.index.names or isinstance(df.index, pd.DatetimeIndex):
    # 연도별 그룹화
    df['year'] = df.index.year
    yearly_stats = df.groupby('year')[target_col].agg([
        'count', 'mean', 'std', 'min', 'max', 'median'
    ]).round(2)
    
    print(f"\n📅 연도별 '{target_col}' 통계:")
    print(yearly_stats)
    
    # 연도별 증가 추세 분석
    yearly_mean = df.groupby('year')[target_col].mean()
    year_diff = yearly_mean.diff().dropna()
    
    print(f"\n📈 연평균 변화량:")
    print(f"  • 전체 평균 증가량: {year_diff.mean():,.2f} MW/년")
    print(f"  • 최대 증가년: {year_diff.idxmax()} (+{year_diff.max():,.2f} MW)")
    print(f"  • 최대 감소년: {year_diff.idxmin()} ({year_diff.min():,.2f} MW)")

# %%
# =============================================================================
# 7. 월별 계절성 분석
# =============================================================================

print("=== 월별 계절성 분석 ===")

if isinstance(df.index, pd.DatetimeIndex):
    # 월별 그룹화
    df['month'] = df.index.month
    monthly_stats = df.groupby('month')[target_col].agg([
        'count', 'mean', 'std', 'min', 'max'
    ]).round(2)
    
    print(f"\n🗓️ 월별 '{target_col}' 통계:")
    monthly_stats['month_name'] = ['1월', '2월', '3월', '4월', '5월', '6월',
                                   '7월', '8월', '9월', '10월', '11월', '12월']
    print(monthly_stats[['month_name', 'mean', 'std', 'min', 'max']])
    
    # 계절별 분석
    def get_season(month):
        if month in [12, 1, 2]:
            return '겨울'
        elif month in [3, 4, 5]:
            return '봄'
        elif month in [6, 7, 8]:
            return '여름'
        else:
            return '가을'
    
    df['season'] = df['month'].apply(get_season)
    seasonal_stats = df.groupby('season')[target_col].agg([
        'count', 'mean', 'std', 'min', 'max'
    ]).round(2)
    
    print(f"\n🌸 계절별 '{target_col}' 통계:")
    print(seasonal_stats)

# %%
# =============================================================================
# 8. 요일별 패턴 분석
# =============================================================================

print("=== 요일별 패턴 분석 ===")

if isinstance(df.index, pd.DatetimeIndex):
    # 요일별 그룹화
    df['weekday'] = df.index.weekday  # 0=월요일, 6=일요일
    df['weekday_name'] = df.index.strftime('%A')
    
    weekday_stats = df.groupby('weekday')[target_col].agg([
        'count', 'mean', 'std', 'min', 'max'
    ]).round(2)
    
    weekday_names = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    weekday_stats['day_name'] = weekday_names
    
    print(f"\n📅 요일별 '{target_col}' 통계:")
    print(weekday_stats[['day_name', 'mean', 'std', 'min', 'max']])
    
    # 평일 vs 주말 비교
    df['is_weekend'] = df['weekday'].isin([5, 6])  # 토요일, 일요일
    weekend_comparison = df.groupby('is_weekend')[target_col].agg([
        'count', 'mean', 'std', 'min', 'max'
    ]).round(2)
    
    weekend_comparison.index = ['평일', '주말']
    print(f"\n🏢 평일 vs 주말 비교:")
    print(weekend_comparison)

# %%
# =============================================================================
# 9. 이상값 탐지 및 분석
# =============================================================================

print("=== 이상값 분석 ===")

if len(numeric_cols) > 0:
    # IQR 방법을 사용한 이상값 탐지
    Q1 = data_series.quantile(0.25)
    Q3 = data_series.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers_iqr = data_series[(data_series < lower_bound) | (data_series > upper_bound)]
    
    print(f"\n🎯 IQR 방법 이상값 탐지:")
    print(f"  • 하한선: {lower_bound:,.2f} MW")
    print(f"  • 상한선: {upper_bound:,.2f} MW")
    print(f"  • 이상값 개수: {len(outliers_iqr):,}개 ({len(outliers_iqr)/len(data_series)*100:.2f}%)")
    
    if len(outliers_iqr) > 0:
        print(f"  • 이상값 범위: {outliers_iqr.min():,.2f} ~ {outliers_iqr.max():,.2f} MW")
        
        # 상위 5개 이상값
        top_outliers = outliers_iqr.nlargest(5)
        print(f"  • 상위 5개 이상값:")
        for date, value in top_outliers.items():
            print(f"    - {date.strftime('%Y-%m-%d')}: {value:,.2f} MW")
    
    # Z-score 방법을 사용한 이상값 탐지
    z_scores = np.abs((data_series - data_series.mean()) / data_series.std())
    outliers_zscore = data_series[z_scores > 3]
    
    print(f"\n📊 Z-score 방법 이상값 탐지 (|z| > 3):")
    print(f"  • 이상값 개수: {len(outliers_zscore):,}개 ({len(outliers_zscore)/len(data_series)*100:.2f}%)")

# %%
# =============================================================================
# 10. 시계열 연속성 및 누락일 확인
# =============================================================================

print("=== 시계열 연속성 확인 ===")

if isinstance(df.index, pd.DatetimeIndex):
    # 전체 기간에서 예상되는 날짜 범위
    date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    missing_dates = date_range.difference(df.index)
    
    print(f"\n📅 시계열 연속성 분석:")
    print(f"  • 전체 기간: {df.index.min().strftime('%Y-%m-%d')} ~ {df.index.max().strftime('%Y-%m-%d')}")
    print(f"  • 예상 총 일수: {len(date_range):,}일")
    print(f"  • 실제 데이터 일수: {len(df):,}일")
    print(f"  • 누락된 날짜: {len(missing_dates):,}일")
    
    if len(missing_dates) > 0:
        print(f"  • 누락 비율: {len(missing_dates)/len(date_range)*100:.2f}%")
        
        # 처음 몇 개 누락 날짜 출력
        print(f"  • 누락된 날짜 예시 (처음 10개):")
        for date in missing_dates[:10]:
            print(f"    - {date.strftime('%Y-%m-%d')}")
    else:
        print("  ✅ 누락된 날짜가 없습니다!")

# %%
# =============================================================================
# 11. 기본 시각화 준비
# =============================================================================

print("=== 기본 시각화 생성 ===")

# 그래프 스타일 설정
plt.style.use('default')
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('시계열 전력수급 데이터 기본 통계 분석', fontsize=16, fontweight='bold')

if len(numeric_cols) > 0:
    # 1. 시계열 플롯
    axes[0,0].plot(df.index, df[target_col], linewidth=0.8, alpha=0.8)
    axes[0,0].set_title(f'{target_col} 시계열 변화')
    axes[0,0].set_ylabel('전력 (MW)')
    axes[0,0].grid(True, alpha=0.3)
    # x축, y축 숫자 크기 및 볼드체 설정
    axes[0,0].tick_params(axis='both', which='major', labelsize=12)
    plt.setp(axes[0,0].get_xticklabels(), fontweight='bold')
    plt.setp(axes[0,0].get_yticklabels(), fontweight='bold')
    
    # 2. 히스토그램
    axes[0,1].hist(df[target_col], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0,1].set_title(f'{target_col} 분포')
    axes[0,1].set_xlabel('전력 (MW)')
    axes[0,1].set_ylabel('빈도')
    axes[0,1].grid(True, alpha=0.3)
    # x축, y축 숫자 크기 및 볼드체 설정
    axes[0,1].tick_params(axis='both', which='major', labelsize=12)
    plt.setp(axes[0,1].get_xticklabels(), fontweight='bold')
    plt.setp(axes[0,1].get_yticklabels(), fontweight='bold')
    
    # 3. 월별 박스플롯
    if 'month' in df.columns:
        monthly_data = [df[df['month'] == month][target_col] for month in range(1, 13)]
        bp = axes[1,0].boxplot(monthly_data, labels=range(1, 13))
        axes[1,0].set_title('월별 전력 분포')
        axes[1,0].set_xlabel('월')
        axes[1,0].set_ylabel('전력 (MW)')
        axes[1,0].grid(True, alpha=0.3)
        # x축, y축 숫자 크기 및 볼드체 설정
        axes[1,0].tick_params(axis='both', which='major', labelsize=12)
        plt.setp(axes[1,0].get_xticklabels(), fontweight='bold')
        plt.setp(axes[1,0].get_yticklabels(), fontweight='bold')
    
    # 4. 연도별 평균 변화
    if 'year' in df.columns:
        yearly_mean = df.groupby('year')[target_col].mean()
        axes[1,1].plot(yearly_mean.index, yearly_mean.values, marker='o', linewidth=2)
        axes[1,1].set_title('연도별 평균 전력 변화')
        axes[1,1].set_xlabel('연도')
        axes[1,1].set_ylabel('평균 전력 (MW)')
        axes[1,1].grid(True, alpha=0.3)
        # x축, y축 숫자 크기 및 볼드체 설정
        axes[1,1].tick_params(axis='both', which='major', labelsize=12)
        plt.setp(axes[1,1].get_xticklabels(), fontweight='bold')
        plt.setp(axes[1,1].get_yticklabels(), fontweight='bold')

plt.tight_layout()

# 그래프 저장
output_dir = project_root / "outputs"
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / "basic_statistics_overview.png", dpi=300, bbox_inches='tight')
print(f"📊 기본 통계 그래프 저장: {output_dir / 'basic_statistics_overview.png'}")

plt.show()

# %%
# =============================================================================
# 12. 상관관계 분석 (추가 변수가 있는 경우)
# =============================================================================

print("=== 상관관계 분석 ===")

# 시간 관련 변수들과의 상관관계
if isinstance(df.index, pd.DatetimeIndex):
    # 시간 기반 변수 생성
    df['day_of_year'] = df.index.dayofyear
    df['week_of_year'] = df.index.isocalendar().week
    
    # 상관관계 계산
    correlation_vars = ['month', 'weekday', 'day_of_year', 'week_of_year']
    correlation_vars = [var for var in correlation_vars if var in df.columns]
    
    if len(correlation_vars) > 0:
        corr_data = df[correlation_vars + [target_col]].corr()
        
        print(f"\n🔗 시간 변수와 '{target_col}' 상관관계:")
        target_corr = corr_data[target_col].drop(target_col).sort_values(key=abs, ascending=False)
        for var, corr_val in target_corr.items():
            print(f"  • {var}: {corr_val:.4f}")

# %%
# =============================================================================
# 13. 통계 요약 리포트 생성
# =============================================================================

print("\n" + "="*60)
print("📋 기본 통계 분석 완료 리포트")
print("="*60)

if len(numeric_cols) > 0:
    print(f"\n🎯 주요 통계 지표 ('{target_col}'):")
    print(f"  • 데이터 기간: {df.index.min().strftime('%Y-%m-%d')} ~ {df.index.max().strftime('%Y-%m-%d')}")
    print(f"  • 총 데이터 포인트: {len(df):,}개")
    print(f"  • 평균: {data_series.mean():,.2f} MW")
    print(f"  • 표준편차: {data_series.std():,.2f} MW")
    print(f"  • 최솟값: {data_series.min():,.2f} MW")
    print(f"  • 최댓값: {data_series.max():,.2f} MW")
    print(f"  • 변동계수: {(data_series.std() / data_series.mean()) * 100:.2f}%")
    
    print(f"\n📊 데이터 품질:")
    print(f"  • 누락값: {df[target_col].isnull().sum():,}개")
    print(f"  • 중복값: {df.duplicated().sum():,}개")
    print(f"  • 이상값 (IQR): {len(outliers_iqr):,}개")
    print(f"  • 시계열 연속성: {len(date_range) - len(missing_dates):,}/{len(date_range):,}일")

print(f"\n💾 결과 저장 위치:")
print(f"  • 통계 그래프: {output_dir / 'basic_statistics_overview.png'}")

print(f"\n🎉 Task 2.2 완료!")
print(f"다음 단계: Task 2.3 - Create Time Series Plots") 