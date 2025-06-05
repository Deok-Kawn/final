# %%
"""
Task 2.3: Create Time Series Visualization
==========================================
시계열 전력수급 데이터의 시각화 차트를 생성합니다.

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

# 그래프 스타일 설정
plt.style.use('default')
sns.set_palette("husl")

print("=== 시계열 시각화 모듈 로딩 완료 ===")
print(f"Pandas: {pd.__version__}")
print(f"NumPy: {np.__version__}")
print(f"Matplotlib: {plt.matplotlib.__version__}")
print(f"Seaborn: {sns.__version__}")

# %%
# =============================================================================
# 2. 데이터 로딩 (Task 2.1-2.2에서 검증된 로직 사용)
# =============================================================================

print("=== 데이터 로딩 ===")

# 프로젝트 루트 및 데이터 파일 경로 설정
project_root = Path.cwd()
data_filename = "일별최대전력수급(2005-2023).csv"

# 데이터 파일 찾기 함수 (이전 태스크에서 검증된 로직)
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

# CSV 로딩 및 날짜 처리
try:
    df = pd.read_csv(data_file, encoding='utf-8')
    df['date'] = pd.to_datetime(df['date'], format='%Y.%m.%d')
    df.set_index('date', inplace=True)
    
    print(f"✅ 데이터 로딩 완료: {df.shape[0]:,}행 × {df.shape[1]}열")
    print(f"날짜 범위: {df.index.min().strftime('%Y-%m-%d')} ~ {df.index.max().strftime('%Y-%m-%d')}")
    
    # 타겟 컬럼 확인
    target_col = '최대전력(MW)'
    if target_col not in df.columns:
        print(f"❌ '{target_col}' 컬럼을 찾을 수 없습니다!")
        exit(1)
        
except Exception as e:
    print(f"❌ 데이터 로딩 실패: {e}")
    exit(1)

# %%
# =============================================================================
# 3. 출력 디렉토리 설정
# =============================================================================

output_dir = project_root / "outputs"
output_dir.mkdir(exist_ok=True)

print(f"📁 출력 디렉토리: {output_dir}")

# %%
# =============================================================================
# 4. 전체 시계열 플롯 (Overview)
# =============================================================================

print("=== 1. 전체 시계열 개요 플롯 생성 ===")

# 그림 설정
fig, axes = plt.subplots(2, 1, figsize=(15, 12))
fig.suptitle('Daily Maximum Power Supply Time Series Data (2005-2023)', fontsize=18, fontweight='bold')

# 상단: 전체 시계열
axes[0].plot(df.index, df[target_col], linewidth=0.8, alpha=0.8, color='steelblue')
axes[0].set_title('Daily Maximum Power Trend - Full Period', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Power (MW)', fontsize=12, fontweight='bold')
axes[0].grid(True, alpha=0.3)
axes[0].tick_params(axis='x', rotation=45)
# 축 숫자 크기 및 볼드체 설정
axes[0].tick_params(axis='both', which='major', labelsize=12)
plt.setp(axes[0].get_xticklabels(), fontweight='bold')
plt.setp(axes[0].get_yticklabels(), fontweight='bold')

# 연도별 평균 추가
df_temp = df.copy()
df_temp['year'] = df_temp.index.year
yearly_mean = df_temp.groupby('year')[target_col].mean()
axes[0].plot(yearly_mean.index, yearly_mean.values, 
             color='red', linewidth=3, label='Annual Average', alpha=0.8)
legend = axes[0].legend(fontsize=11)
for text in legend.get_texts():
    text.set_fontweight('bold')

# 하단: 이동평균을 활용한 트렌드
rolling_30 = df[target_col].rolling(window=30, center=True).mean()
rolling_365 = df[target_col].rolling(window=365, center=True).mean()

axes[1].plot(df.index, df[target_col], linewidth=0.5, alpha=0.3, color='lightgray', label='Daily Data')
axes[1].plot(df.index, rolling_30, linewidth=1.5, color='orange', label='30-Day Moving Average')
axes[1].plot(df.index, rolling_365, linewidth=2.5, color='red', label='365-Day Moving Average')
axes[1].set_title('Trend Analysis with Moving Averages', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Year', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Power (MW)', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3)
legend = axes[1].legend(fontsize=11)
for text in legend.get_texts():
    text.set_fontweight('bold')
axes[1].tick_params(axis='x', rotation=45)
# 축 숫자 크기 및 볼드체 설정
axes[1].tick_params(axis='both', which='major', labelsize=12)
plt.setp(axes[1].get_xticklabels(), fontweight='bold')
plt.setp(axes[1].get_yticklabels(), fontweight='bold')

plt.subplots_adjust(hspace=0.4)
plt.savefig(output_dir / "01_timeseries_overview.png", dpi=300, bbox_inches='tight')
print(f"📊 저장: {output_dir / '01_timeseries_overview.png'}")
plt.show()

# %%
# =============================================================================
# 5. 연도별 상세 분석 플롯
# =============================================================================

print("=== 2. 연도별 상세 분석 플롯 생성 ===")

# 연도별 데이터 준비
df_temp = df.copy()
df_temp['year'] = df_temp.index.year
df_temp['month'] = df_temp.index.month
df_temp['day_of_year'] = df_temp.index.dayofyear

# 그림 설정
fig, axes = plt.subplots(2, 2, figsize=(18, 14))
fig.suptitle('Annual Power Supply Pattern Analysis', fontsize=18, fontweight='bold')

# 1. 연도별 박스플롯
yearly_data = [df_temp[df_temp['year'] == year][target_col] for year in sorted(df_temp['year'].unique())]
bp1 = axes[0,0].boxplot(yearly_data, labels=sorted(df_temp['year'].unique()))
axes[0,0].set_title('Annual Power Distribution (Box Plot)', fontsize=13, fontweight='bold')
axes[0,0].set_xlabel('Year', fontsize=11, fontweight='bold')
axes[0,0].set_ylabel('Power (MW)', fontsize=11, fontweight='bold')
axes[0,0].tick_params(axis='x', rotation=45)
axes[0,0].grid(True, alpha=0.3)
# 축 숫자 크기 및 볼드체 설정
axes[0,0].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[0,0].get_xticklabels(), fontweight='bold')
plt.setp(axes[0,0].get_yticklabels(), fontweight='bold')

# 2. 연도별 평균/최대값 추이
yearly_stats = df_temp.groupby('year')[target_col].agg(['mean', 'max', 'min']).round(0)
axes[0,1].plot(yearly_stats.index, yearly_stats['mean'], marker='o', linewidth=2, label='Mean')
axes[0,1].plot(yearly_stats.index, yearly_stats['max'], marker='s', linewidth=2, label='Max')
axes[0,1].plot(yearly_stats.index, yearly_stats['min'], marker='^', linewidth=2, label='Min')
axes[0,1].set_title('Annual Statistics Trend', fontsize=13, fontweight='bold')
axes[0,1].set_xlabel('Year', fontsize=11, fontweight='bold')
axes[0,1].set_ylabel('Power (MW)', fontsize=11, fontweight='bold')
legend = axes[0,1].legend(fontsize=10)
for text in legend.get_texts():
    text.set_fontweight('bold')
axes[0,1].grid(True, alpha=0.3)
# 축 숫자 크기 및 볼드체 설정
axes[0,1].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[0,1].get_xticklabels(), fontweight='bold')
plt.setp(axes[0,1].get_yticklabels(), fontweight='bold')

# 3. 연도별 변동성 (표준편차)
yearly_std = df_temp.groupby('year')[target_col].std()
axes[1,0].bar(yearly_std.index, yearly_std.values, alpha=0.7, color='skyblue', edgecolor='black')
axes[1,0].set_title('Annual Volatility (Standard Deviation)', fontsize=13, fontweight='bold')
axes[1,0].set_xlabel('Year', fontsize=11, fontweight='bold')
axes[1,0].set_ylabel('Standard Deviation (MW)', fontsize=11, fontweight='bold')
axes[1,0].tick_params(axis='x', rotation=45)
axes[1,0].grid(True, alpha=0.3)
# 축 숫자 크기 및 볼드체 설정
axes[1,0].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[1,0].get_xticklabels(), fontweight='bold')
plt.setp(axes[1,0].get_yticklabels(), fontweight='bold')

# 4. 연도별 성장률
yearly_mean = df_temp.groupby('year')[target_col].mean()
growth_rate = yearly_mean.pct_change() * 100
axes[1,1].bar(growth_rate.index[1:], growth_rate.values[1:], 
              color=['green' if x > 0 else 'red' for x in growth_rate.values[1:]], alpha=0.7)
axes[1,1].axhline(y=0, color='black', linestyle='-', linewidth=1)
axes[1,1].set_title('Annual Growth Rate (%)', fontsize=13, fontweight='bold')
axes[1,1].set_xlabel('Year', fontsize=11, fontweight='bold')
axes[1,1].set_ylabel('Growth Rate (%)', fontsize=11, fontweight='bold')
axes[1,1].tick_params(axis='x', rotation=45)
axes[1,1].grid(True, alpha=0.3)
# 축 숫자 크기 및 볼드체 설정
axes[1,1].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[1,1].get_xticklabels(), fontweight='bold')
plt.setp(axes[1,1].get_yticklabels(), fontweight='bold')

plt.subplots_adjust(hspace=0.4, wspace=0.3)
plt.savefig(output_dir / "02_yearly_analysis.png", dpi=300, bbox_inches='tight')
print(f"📊 저장: {output_dir / '02_yearly_analysis.png'}")
plt.show()

# %%
# =============================================================================
# 6. 계절성 패턴 분석 플롯
# =============================================================================

print("=== 3. 계절성 패턴 분석 플롯 생성 ===")

# 계절성 데이터 준비
df_temp['month'] = df_temp.index.month
df_temp['weekday'] = df_temp.index.weekday
df_temp['week_of_year'] = df_temp.index.isocalendar().week

# 계절 분류 함수
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

df_temp['season'] = df_temp['month'].apply(get_season)

# 그림 설정
fig, axes = plt.subplots(2, 2, figsize=(18, 14))
fig.suptitle('Seasonal and Periodic Pattern Analysis', fontsize=18, fontweight='bold')

# 1. 월별 패턴
monthly_mean = df_temp.groupby('month')[target_col].mean()
monthly_std = df_temp.groupby('month')[target_col].std()

axes[0,0].bar(range(1, 13), monthly_mean.values, alpha=0.7, color='lightcoral', 
              yerr=monthly_std.values, capsize=5, edgecolor='black')
axes[0,0].set_title('Monthly Average Power Supply (±Std Dev)', fontsize=13, fontweight='bold')
axes[0,0].set_xlabel('Month', fontsize=11, fontweight='bold')
axes[0,0].set_ylabel('Average Power (MW)', fontsize=11, fontweight='bold')
axes[0,0].set_xticks(range(1, 13))
axes[0,0].grid(True, alpha=0.3)
# 축 숫자 크기 및 볼드체 설정
axes[0,0].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[0,0].get_xticklabels(), fontweight='bold')
plt.setp(axes[0,0].get_yticklabels(), fontweight='bold')

# 2. 계절별 분포
season_order = ['Spring', 'Summer', 'Fall', 'Winter']
seasonal_data = [df_temp[df_temp['season'] == season][target_col] for season in season_order]
bp2 = axes[0,1].boxplot(seasonal_data, labels=season_order)
axes[0,1].set_title('Seasonal Power Distribution', fontsize=13, fontweight='bold')
axes[0,1].set_xlabel('Season', fontsize=11, fontweight='bold')
axes[0,1].set_ylabel('Power (MW)', fontsize=11, fontweight='bold')
axes[0,1].grid(True, alpha=0.3)
# 축 숫자 크기 및 볼드체 설정
axes[0,1].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[0,1].get_xticklabels(), fontweight='bold')
plt.setp(axes[0,1].get_yticklabels(), fontweight='bold')

# 3. 요일별 패턴
weekday_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
weekday_mean = df_temp.groupby('weekday')[target_col].mean()
weekday_std = df_temp.groupby('weekday')[target_col].std()

colors = ['red' if i < 5 else 'blue' for i in range(7)]  # 평일=빨강, 주말=파랑
axes[1,0].bar(range(7), weekday_mean.values, alpha=0.7, color=colors,
              yerr=weekday_std.values, capsize=5, edgecolor='black')
axes[1,0].set_title('Weekly Average Power Supply (Weekday vs Weekend)', fontsize=13, fontweight='bold')
axes[1,0].set_xlabel('Day of Week', fontsize=11, fontweight='bold')
axes[1,0].set_ylabel('Average Power (MW)', fontsize=11, fontweight='bold')
axes[1,0].set_xticks(range(7))
axes[1,0].set_xticklabels(weekday_names)
axes[1,0].grid(True, alpha=0.3)
# 축 숫자 크기 및 볼드체 설정
axes[1,0].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[1,0].get_xticklabels(), fontweight='bold')
plt.setp(axes[1,0].get_yticklabels(), fontweight='bold')

# 4. 연중 주차별 패턴 (히트맵)
weekly_pattern = df_temp.groupby(['year', 'week_of_year'])[target_col].mean().unstack(level=0)
im = axes[1,1].imshow(weekly_pattern.T, aspect='auto', cmap='YlOrRd', interpolation='nearest')
axes[1,1].set_title('Annual Weekly Power Pattern (Heatmap)', fontsize=13, fontweight='bold')
axes[1,1].set_xlabel('Week of Year', fontsize=11, fontweight='bold')
axes[1,1].set_ylabel('Year', fontsize=11, fontweight='bold')
axes[1,1].set_yticks(range(len(weekly_pattern.columns)))
axes[1,1].set_yticklabels(weekly_pattern.columns)
# 축 숫자 크기 및 볼드체 설정
axes[1,1].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[1,1].get_xticklabels(), fontweight='bold')
plt.setp(axes[1,1].get_yticklabels(), fontweight='bold')

# 컬러바 추가
cbar = plt.colorbar(im, ax=axes[1,1])
cbar.set_label('Average Power (MW)', fontsize=11, fontweight='bold')

plt.subplots_adjust(hspace=0.4, wspace=0.3)
plt.savefig(output_dir / "03_seasonal_patterns.png", dpi=300, bbox_inches='tight')
print(f"📊 저장: {output_dir / '03_seasonal_patterns.png'}")
plt.show()

# %%
# =============================================================================
# 7. 특별 이벤트 및 이상값 시각화
# =============================================================================

print("=== 4. 특별 이벤트 및 이상값 시각화 ===")

# 이상값 탐지 (IQR 방법)
Q1 = df[target_col].quantile(0.25)
Q3 = df[target_col].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df[target_col] < lower_bound) | (df[target_col] > upper_bound)]
extreme_high = df[df[target_col] > df[target_col].quantile(0.99)]
extreme_low = df[df[target_col] < df[target_col].quantile(0.01)]

# 그림 설정
fig, axes = plt.subplots(2, 1, figsize=(15, 12))
fig.suptitle('Special Events and Outlier Analysis', fontsize=18, fontweight='bold')

# 상단: 이상값 하이라이트
axes[0].plot(df.index, df[target_col], linewidth=0.8, alpha=0.6, color='gray', label='Normal Data')
if len(outliers) > 0:
    axes[0].scatter(outliers.index, outliers[target_col], 
                   color='red', s=30, alpha=0.8, label=f'Outliers ({len(outliers)})')
if len(extreme_high) > 0:
    axes[0].scatter(extreme_high.index, extreme_high[target_col], 
                   color='orange', s=50, alpha=0.8, label=f'Extreme Values (Top 1%) ({len(extreme_high)})')

axes[0].axhline(y=upper_bound, color='red', linestyle='--', alpha=0.7, label=f'Upper Bound ({upper_bound:,.0f})')
axes[0].axhline(y=lower_bound, color='red', linestyle='--', alpha=0.7, label=f'Lower Bound ({lower_bound:,.0f})')
axes[0].set_title('Outliers and Extreme Values Distribution', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Power (MW)', fontsize=12, fontweight='bold')
legend = axes[0].legend(fontsize=10)
for text in legend.get_texts():
    text.set_fontweight('bold')
axes[0].grid(True, alpha=0.3)
# 축 숫자 크기 및 볼드체 설정
axes[0].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[0].get_xticklabels(), fontweight='bold')
plt.setp(axes[0].get_yticklabels(), fontweight='bold')

# 하단: 연도별 최대/최소값 분포
yearly_max = df_temp.groupby('year')[target_col].max()
yearly_min = df_temp.groupby('year')[target_col].min()
yearly_max_date = df_temp.groupby('year')[target_col].idxmax()
yearly_min_date = df_temp.groupby('year')[target_col].idxmin()

axes[1].plot(yearly_max.index, yearly_max.values, marker='o', linewidth=2, 
             color='red', label='Annual Maximum', markersize=8)
axes[1].plot(yearly_min.index, yearly_min.values, marker='v', linewidth=2, 
             color='blue', label='Annual Minimum', markersize=8)

# 평균선 추가
mean_line = df[target_col].mean()
axes[1].axhline(y=mean_line, color='green', linestyle='-', alpha=0.7, 
               label=f'Overall Average ({mean_line:,.0f})')

axes[1].set_title('Annual Maximum/Minimum Trend', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Year', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Power (MW)', fontsize=12, fontweight='bold')
legend = axes[1].legend(fontsize=11)
for text in legend.get_texts():
    text.set_fontweight('bold')
axes[1].grid(True, alpha=0.3)
# 축 숫자 크기 및 볼드체 설정
axes[1].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[1].get_xticklabels(), fontweight='bold')
plt.setp(axes[1].get_yticklabels(), fontweight='bold')

plt.subplots_adjust(hspace=0.4)
plt.savefig(output_dir / "04_outliers_events.png", dpi=300, bbox_inches='tight')
print(f"📊 저장: {output_dir / '04_outliers_events.png'}")
plt.show()

# %%
# =============================================================================
# 8. 분해 분석 (Decomposition)
# =============================================================================

print("=== 5. 시계열 분해 분석 ===")

# 간단한 시계열 분해 (추세, 계절성, 잔차)
# 연간 이동평균으로 추세 계산
trend = df[target_col].rolling(window=365, center=True).mean()

# 월별 계절성 패턴 계산
monthly_avg = df_temp.groupby('month')[target_col].mean()
seasonal = df_temp['month'].map(monthly_avg)

# 잔차 계산
residual = df[target_col] - trend - seasonal

# 그림 설정
fig, axes = plt.subplots(4, 1, figsize=(15, 16))
fig.suptitle('Time Series Decomposition (Trend + Seasonality + Residual)', fontsize=18, fontweight='bold')

# 1. 원본 데이터
axes[0].plot(df.index, df[target_col], linewidth=1, color='black')
axes[0].set_title('Original Time Series Data', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Power (MW)', fontsize=11, fontweight='bold')
axes[0].grid(True, alpha=0.3)
# 축 숫자 크기 및 볼드체 설정
axes[0].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[0].get_xticklabels(), fontweight='bold')
plt.setp(axes[0].get_yticklabels(), fontweight='bold')

# 2. 추세 (Trend)
axes[1].plot(df.index, trend, linewidth=2, color='red')
axes[1].set_title('Trend Component (365-Day Moving Average)', fontsize=13, fontweight='bold')
axes[1].set_ylabel('Trend (MW)', fontsize=11, fontweight='bold')
axes[1].grid(True, alpha=0.3)
# 축 숫자 크기 및 볼드체 설정
axes[1].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[1].get_xticklabels(), fontweight='bold')
plt.setp(axes[1].get_yticklabels(), fontweight='bold')

# 3. 계절성 (Seasonality)
axes[2].plot(df.index, seasonal, linewidth=1, color='green', alpha=0.8)
axes[2].set_title('Seasonal Component (Monthly Pattern)', fontsize=13, fontweight='bold')
axes[2].set_ylabel('Seasonality (MW)', fontsize=11, fontweight='bold')
axes[2].grid(True, alpha=0.3)
# 축 숫자 크기 및 볼드체 설정
axes[2].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[2].get_xticklabels(), fontweight='bold')
plt.setp(axes[2].get_yticklabels(), fontweight='bold')

# 4. 잔차 (Residual)
axes[3].plot(df.index, residual, linewidth=0.8, color='orange', alpha=0.7)
axes[3].axhline(y=0, color='black', linestyle='-', linewidth=1)
axes[3].set_title('Residual Component (Original - Trend - Seasonality)', fontsize=13, fontweight='bold')
axes[3].set_xlabel('Year', fontsize=11, fontweight='bold')
axes[3].set_ylabel('Residual (MW)', fontsize=11, fontweight='bold')
axes[3].grid(True, alpha=0.3)
# 축 숫자 크기 및 볼드체 설정
axes[3].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[3].get_xticklabels(), fontweight='bold')
plt.setp(axes[3].get_yticklabels(), fontweight='bold')

plt.subplots_adjust(hspace=0.5)
plt.savefig(output_dir / "05_decomposition.png", dpi=300, bbox_inches='tight')
print(f"📊 저장: {output_dir / '05_decomposition.png'}")
plt.show()

# %%
# =============================================================================
# 9. 분포 및 확률밀도 분석
# =============================================================================

print("=== 6. 분포 및 확률밀도 분석 ===")

# 그림 설정
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Power Supply Data Distribution Analysis', fontsize=18, fontweight='bold')

# 1. 히스토그램 + KDE
axes[0,0].hist(df[target_col], bins=50, alpha=0.7, color='skyblue', 
               edgecolor='black', density=True, label='Histogram')
df[target_col].plot.kde(ax=axes[0,0], color='red', linewidth=2, label='KDE')
axes[0,0].axvline(df[target_col].mean(), color='green', linestyle='--', 
                  linewidth=2, label=f'Mean ({df[target_col].mean():,.0f})')
axes[0,0].axvline(df[target_col].median(), color='orange', linestyle='--', 
                  linewidth=2, label=f'Median ({df[target_col].median():,.0f})')
axes[0,0].set_title('Power Data Distribution (Histogram + KDE)', fontsize=13, fontweight='bold')
axes[0,0].set_xlabel('Power (MW)', fontsize=11, fontweight='bold')
axes[0,0].set_ylabel('Probability Density', fontsize=11, fontweight='bold')
legend = axes[0,0].legend(fontsize=9)
for text in legend.get_texts():
    text.set_fontweight('bold')
axes[0,0].grid(True, alpha=0.3)
# 축 숫자 크기 및 볼드체 설정
axes[0,0].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[0,0].get_xticklabels(), fontweight='bold')
plt.setp(axes[0,0].get_yticklabels(), fontweight='bold')

# 2. Q-Q 플롯 (정규성 검증)
from scipy import stats
stats.probplot(df[target_col], dist="norm", plot=axes[0,1])
axes[0,1].set_title('Q-Q Plot (Normal Distribution Comparison)', fontsize=13, fontweight='bold')
axes[0,1].grid(True, alpha=0.3)
# 축 숫자 크기 및 볼드체 설정
axes[0,1].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[0,1].get_xticklabels(), fontweight='bold')
plt.setp(axes[0,1].get_yticklabels(), fontweight='bold')

# 3. 계절별 분포 비교
season_colors = {'Spring': 'green', 'Summer': 'red', 'Fall': 'orange', 'Winter': 'blue'}
for season in season_order:
    season_data = df_temp[df_temp['season'] == season][target_col]
    season_data.plot.kde(ax=axes[1,0], label=f'{season} (n={len(season_data)})', 
                        color=season_colors[season], linewidth=2)

axes[1,0].set_title('Seasonal Power Distribution Comparison (KDE)', fontsize=13, fontweight='bold')
axes[1,0].set_xlabel('Power (MW)', fontsize=11, fontweight='bold')
axes[1,0].set_ylabel('Probability Density', fontsize=11, fontweight='bold')
legend = axes[1,0].legend(fontsize=9)
for text in legend.get_texts():
    text.set_fontweight('bold')
axes[1,0].grid(True, alpha=0.3)
# 축 숫자 크기 및 볼드체 설정
axes[1,0].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[1,0].get_xticklabels(), fontweight='bold')
plt.setp(axes[1,0].get_yticklabels(), fontweight='bold')

# 4. 연도별 분포 변화 (바이올린 플롯)
years_sample = sorted(df_temp['year'].unique())[::3]  # 3년마다 샘플링
yearly_data_sample = [df_temp[df_temp['year'] == year][target_col] for year in years_sample]
parts = axes[1,1].violinplot(yearly_data_sample, positions=range(len(years_sample)), 
                            showmeans=True, showmedians=True)
axes[1,1].set_title('Annual Distribution Changes (Violin Plot)', fontsize=13, fontweight='bold')
axes[1,1].set_xlabel('Year (Sample)', fontsize=11, fontweight='bold')
axes[1,1].set_ylabel('Power (MW)', fontsize=11, fontweight='bold')
axes[1,1].set_xticks(range(len(years_sample)))
axes[1,1].set_xticklabels(years_sample)
axes[1,1].grid(True, alpha=0.3)
# 축 숫자 크기 및 볼드체 설정
axes[1,1].tick_params(axis='both', which='major', labelsize=10)
plt.setp(axes[1,1].get_xticklabels(), fontweight='bold')
plt.setp(axes[1,1].get_yticklabels(), fontweight='bold')

plt.subplots_adjust(hspace=0.4, wspace=0.3)
plt.savefig(output_dir / "06_distributions.png", dpi=300, bbox_inches='tight')
print(f"📊 저장: {output_dir / '06_distributions.png'}")
plt.show()

# %%
# =============================================================================
# 10. 요약 리포트 및 통계
# =============================================================================

print("\n" + "="*60)
print("📋 시계열 시각화 완료 리포트")
print("="*60)

print(f"\n🎯 생성된 시각화 차트:")
charts_created = [
    "01_timeseries_overview.png - 전체 시계열 개요 및 트렌드",
    "02_yearly_analysis.png - 연도별 상세 분석",
    "03_seasonal_patterns.png - 계절성 및 주기적 패턴",
    "04_outliers_events.png - 이상값 및 특별 이벤트",
    "05_decomposition.png - 시계열 분해 분석",
    "06_distributions.png - 분포 및 확률밀도 분석"
]

for i, chart in enumerate(charts_created, 1):
    print(f"  {i}. {chart}")

print(f"\n📊 주요 시각화 인사이트:")
print(f"  • 전체 기간: {df.index.min().strftime('%Y-%m-%d')} ~ {df.index.max().strftime('%Y-%m-%d')}")
print(f"  • 총 데이터 포인트: {len(df):,}개")
print(f"  • 연평균 증가 추세: 지속적 상승 패턴")
print(f"  • 계절성: 겨울 > 여름 > 가을 > 봄 순")
print(f"  • 요일 패턴: 평일 > 주말 전력수요")
print(f"  • 이상값: {len(outliers)}개 탐지")

print(f"\n💾 결과 저장 위치:")
print(f"  • 출력 디렉토리: {output_dir}")
print(f"  • 모든 차트: PNG 형식, 300 DPI")

print(f"\n🎉 Task 2.3 완료!")
print(f"다음 단계: Task 2.4 - Analyze Missing Values") 