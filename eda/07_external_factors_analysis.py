#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
외부 요인 및 특별 이벤트 분석
TaskMaster 작업 2.7: External Factors and Special Events Analysis

전력 수요에 영향을 미치는 외부 요인들을 분석하여 예측 모델 개선을 위한 인사이트 도출
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = ['Arial Unicode MS', 'AppleGothic', 'Malgun Gothic']
plt.rcParams['axes.unicode_minus'] = False

def load_and_prepare_data():
    """데이터 로딩 및 전처리"""
    print("📊 데이터 로딩 및 전처리...")
    
    # 데이터 로딩
    df = pd.read_csv('data/shared/data.csv')
    
    # 날짜 변환 및 정렬
    df['date'] = pd.to_datetime(df['date'], format='%Y.%m.%d')
    df = df.sort_values('date').reset_index(drop=True)
    
    # 기본 시간 변수 추가
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['weekday'] = df['date'].dt.weekday  # 0=월요일, 6=일요일
    df['day_of_year'] = df['date'].dt.dayofyear
    
    print(f"✅ 데이터 준비 완료: {len(df)}개 데이터 포인트")
    print(f"📅 기간: {df['date'].min().strftime('%Y-%m-%d')} ~ {df['date'].max().strftime('%Y-%m-%d')}")
    
    return df

def create_korean_holidays(start_year=2005, end_year=2023):
    """한국 공휴일 정보 생성"""
    print("\n🇰🇷 한국 공휴일 정보 생성 중...")
    
    holidays = []
    
    for year in range(start_year, end_year + 1):
        # 고정 공휴일
        fixed_holidays = [
            (f'{year}-01-01', '신정'),
            (f'{year}-03-01', '삼일절'),
            (f'{year}-05-05', '어린이날'),
            (f'{year}-06-06', '현충일'),
            (f'{year}-08-15', '광복절'),
            (f'{year}-10-03', '개천절'),
            (f'{year}-10-09', '한글날'),
            (f'{year}-12-25', '성탄절'),
        ]
        
        # 추석 (음력 8월 15일) - 근사값 사용
        chuseok_dates = {
            2005: ['2005-09-17', '2005-09-18', '2005-09-19'],
            2006: ['2006-10-05', '2006-10-06', '2006-10-07'],
            2007: ['2007-09-24', '2007-09-25', '2007-09-26'],
            2008: ['2008-09-12', '2008-09-13', '2008-09-14', '2008-09-15'],
            2009: ['2009-10-02', '2009-10-03', '2009-10-04'],
            2010: ['2010-09-21', '2010-09-22', '2010-09-23'],
            2011: ['2011-09-10', '2011-09-11', '2011-09-12', '2011-09-13'],
            2012: ['2012-09-29', '2012-09-30', '2012-10-01'],
            2013: ['2013-09-18', '2013-09-19', '2013-09-20'],
            2014: ['2014-09-06', '2014-09-07', '2014-09-08', '2014-09-09'],
            2015: ['2015-09-26', '2015-09-27', '2015-09-28'],
            2016: ['2016-09-14', '2016-09-15', '2016-09-16'],
            2017: ['2017-10-03', '2017-10-04', '2017-10-05', '2017-10-06'],
            2018: ['2018-09-22', '2018-09-23', '2018-09-24', '2018-09-25'],
            2019: ['2019-09-12', '2019-09-13', '2019-09-14'],
            2020: ['2020-09-30', '2020-10-01', '2020-10-02'],
            2021: ['2021-09-20', '2021-09-21', '2021-09-22'],
            2022: ['2022-09-09', '2022-09-10', '2022-09-11', '2022-09-12'],
            2023: ['2023-09-28', '2023-09-29', '2023-09-30']
        }
        
        # 설날 (음력 1월 1일) - 근사값 사용
        lunar_new_year_dates = {
            2005: ['2005-02-07', '2005-02-08', '2005-02-09'],
            2006: ['2006-01-28', '2006-01-29', '2006-01-30'],
            2007: ['2007-02-17', '2007-02-18', '2007-02-19'],
            2008: ['2008-02-06', '2008-02-07', '2008-02-08'],
            2009: ['2009-01-25', '2009-01-26', '2009-01-27'],
            2010: ['2010-02-13', '2010-02-14', '2010-02-15'],
            2011: ['2011-02-02', '2011-02-03', '2011-02-04'],
            2012: ['2012-01-22', '2012-01-23', '2012-01-24'],
            2013: ['2013-02-09', '2013-02-10', '2013-02-11'],
            2014: ['2014-01-30', '2014-01-31', '2014-02-01'],
            2015: ['2015-02-18', '2015-02-19', '2015-02-20'],
            2016: ['2016-02-07', '2016-02-08', '2016-02-09'],
            2017: ['2017-01-27', '2017-01-28', '2017-01-29'],
            2018: ['2018-02-15', '2018-02-16', '2018-02-17'],
            2019: ['2019-02-04', '2019-02-05', '2019-02-06'],
            2020: ['2020-01-24', '2020-01-25', '2020-01-26'],
            2021: ['2021-02-11', '2021-02-12', '2021-02-13'],
            2022: ['2022-01-31', '2022-02-01', '2022-02-02'],
            2023: ['2023-01-21', '2023-01-22', '2023-01-23']
        }
        
        # 고정 공휴일 추가
        holidays.extend([(date, name) for date, name in fixed_holidays])
        
        # 추석 추가
        if year in chuseok_dates:
            for i, date in enumerate(chuseok_dates[year]):
                name = ['추석 전날', '추석', '추석 다음날', '추석 연휴'][i] if len(chuseok_dates[year]) > 3 else ['추석 전날', '추석', '추석 다음날'][i]
                holidays.append((date, name))
        
        # 설날 추가
        if year in lunar_new_year_dates:
            for i, date in enumerate(lunar_new_year_dates[year]):
                name = ['설날 전날', '설날', '설날 다음날'][i]
                holidays.append((date, name))
        
        # 부처님 오신 날 (음력 4월 8일) - 대략적 날짜
        buddha_birthday = {
            2005: '2005-05-15', 2006: '2006-05-05', 2007: '2007-05-24',
            2008: '2008-05-12', 2009: '2009-05-02', 2010: '2010-05-21',
            2011: '2011-05-10', 2012: '2012-05-28', 2013: '2013-05-17',
            2014: '2014-05-06', 2015: '2015-05-25', 2016: '2016-05-14',
            2017: '2017-05-03', 2018: '2018-05-22', 2019: '2019-05-12',
            2020: '2020-04-30', 2021: '2021-05-19', 2022: '2022-05-08',
            2023: '2023-05-27'
        }
        
        if year in buddha_birthday:
            holidays.append((buddha_birthday[year], '부처님 오신 날'))
    
    # DataFrame으로 변환
    holiday_df = pd.DataFrame(holidays, columns=['date', 'holiday_name'])
    holiday_df['date'] = pd.to_datetime(holiday_df['date'])
    
    print(f"✅ 총 {len(holiday_df)}개 공휴일 정보 생성 완료")
    
    return holiday_df

def analyze_holiday_impact(df, holidays_df):
    """공휴일 영향 분석"""
    print("\n🎉 공휴일 영향 분석 중...")
    
    # 공휴일 정보 병합
    df_analysis = df.copy()
    df_analysis['is_holiday'] = df_analysis['date'].isin(holidays_df['date'])
    
    # 공휴일 전후 영향 분석
    df_analysis['is_before_holiday'] = df_analysis['date'].isin(holidays_df['date'] - timedelta(days=1))
    df_analysis['is_after_holiday'] = df_analysis['date'].isin(holidays_df['date'] + timedelta(days=1))
    
    # 주말 여부
    df_analysis['is_weekend'] = df_analysis['weekday'].isin([5, 6])  # 토요일, 일요일
    df_analysis['is_weekday'] = ~df_analysis['is_weekend']
    
    # 공휴일 타입별 분석
    holiday_types = {
        '신정': ['신정'],
        '설날': ['설날 전날', '설날', '설날 다음날'],
        '삼일절': ['삼일절'],
        '부처님오신날': ['부처님 오신 날'],
        '어린이날': ['어린이날'],
        '현충일': ['현충일'],
        '광복절': ['광복절'],
        '추석': ['추석 전날', '추석', '추석 다음날', '추석 연휴'],
        '개천절': ['개천절'],
        '한글날': ['한글날'],
        '성탄절': ['성탄절']
    }
    
    # 공휴일별 전력 수요 평균 계산
    holiday_impact = {}
    
    for holiday_type, holiday_names in holiday_types.items():
        holiday_dates = holidays_df[holidays_df['holiday_name'].isin(holiday_names)]['date']
        holiday_power = df_analysis[df_analysis['date'].isin(holiday_dates)]['최대전력(MW)']
        
        if len(holiday_power) > 0:
            holiday_impact[holiday_type] = {
                'count': len(holiday_power),
                'mean_power': holiday_power.mean(),
                'std_power': holiday_power.std()
            }
    
    # 평일/주말/공휴일 비교
    normal_weekday = df_analysis[(~df_analysis['is_holiday']) & (~df_analysis['is_weekend'])]['최대전력(MW)']
    weekend = df_analysis[df_analysis['is_weekend'] & (~df_analysis['is_holiday'])]['최대전력(MW)']
    holidays = df_analysis[df_analysis['is_holiday']]['최대전력(MW)']
    
    comparison_stats = {
        '평일': {'mean': normal_weekday.mean(), 'std': normal_weekday.std(), 'count': len(normal_weekday)},
        '주말': {'mean': weekend.mean(), 'std': weekend.std(), 'count': len(weekend)},
        '공휴일': {'mean': holidays.mean(), 'std': holidays.std(), 'count': len(holidays)}
    }
    
    print("📊 평일/주말/공휴일 전력 수요 비교:")
    for day_type, stats in comparison_stats.items():
        print(f"  {day_type}: 평균 {stats['mean']:,.0f}MW (±{stats['std']:,.0f}), {stats['count']}일")
    
    return df_analysis, holiday_impact, comparison_stats

def analyze_special_events(df):
    """특별 이벤트 영향 분석"""
    print("\n🌟 특별 이벤트 영향 분석 중...")
    
    # 주요 특별 이벤트 정의
    special_events = {
        '2008 베이징 올림픽': ['2008-08-08', '2008-08-24'],
        '2010 밴쿠버 동계올림픽': ['2010-02-12', '2010-02-28'],
        '2012 런던 올림픽': ['2012-07-27', '2012-08-12'],
        '2014 소치 동계올림픽': ['2014-02-07', '2014-02-23'],
        '2016 리우 올림픽': ['2016-08-05', '2016-08-21'],
        '2018 평창 동계올림픽': ['2018-02-09', '2018-02-25'],
        '2020 도쿄 올림픽': ['2021-07-23', '2021-08-08'],  # 코로나로 연기
        '2022 베이징 동계올림픽': ['2022-02-04', '2022-02-20'],
        
        # 대선
        '2007 대선': ['2007-12-19', '2007-12-19'],
        '2012 대선': ['2012-12-19', '2012-12-19'],
        '2017 대선': ['2017-05-09', '2017-05-09'],
        '2022 대선': ['2022-03-09', '2022-03-09'],
        
        # 경제 위기
        '2008 금융위기': ['2008-09-01', '2009-03-31'],
        '2011 유럽재정위기': ['2011-07-01', '2011-12-31'],
        
        # 코로나19
        '코로나19 팬데믹': ['2020-01-20', '2023-05-05'],  # WHO 팬데믹 종료 선언까지
        
        # 기타 사회적 이벤트
        '2014 세월호 참사': ['2014-04-16', '2014-04-30'],
        '2016-2017 촛불집회': ['2016-10-29', '2017-04-29'],
    }
    
    # 이벤트별 영향 분석
    event_impact = {}
    
    for event_name, (start_date, end_date) in special_events.items():
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        
        # 데이터 범위 내에 있는 이벤트만 분석
        if start_dt >= df['date'].min() and start_dt <= df['date'].max():
            # 이벤트 기간 데이터
            event_data = df[(df['date'] >= start_dt) & (df['date'] <= end_dt)]['최대전력(MW)']
            
            # 같은 기간 전년도 데이터 (비교군)
            prev_year_start = start_dt - pd.DateOffset(years=1)
            prev_year_end = end_dt - pd.DateOffset(years=1)
            prev_year_data = df[(df['date'] >= prev_year_start) & (df['date'] <= prev_year_end)]['최대전력(MW)']
            
            if len(event_data) > 0 and len(prev_year_data) > 0:
                event_impact[event_name] = {
                    'event_mean': event_data.mean(),
                    'prev_year_mean': prev_year_data.mean(),
                    'change_percent': ((event_data.mean() - prev_year_data.mean()) / prev_year_data.mean()) * 100,
                    'days_count': len(event_data),
                    'period': f"{start_date} ~ {end_date}"
                }
    
    return event_impact

def analyze_seasonal_patterns(df):
    """계절별 특별 패턴 분석"""
    print("\n🌸 계절별 특별 패턴 분석 중...")
    
    # 계절 정의
    def get_season(month):
        if month in [12, 1, 2]:
            return '겨울'
        elif month in [3, 4, 5]:
            return '봄'
        elif month in [6, 7, 8]:
            return '여름'
        else:  # 9, 10, 11
            return '가을'
    
    df_seasonal = df.copy()
    df_seasonal['season'] = df_seasonal['month'].apply(get_season)
    
    seasonal_impact = {}
    
    # 계절별 기본 통계
    for season in ['봄', '여름', '가을', '겨울']:
        season_data = df_seasonal[df_seasonal['season'] == season]['최대전력(MW)']
        seasonal_impact[season] = {
            'mean': season_data.mean(),
            'std': season_data.std(),
            'min': season_data.min(),
            'max': season_data.max(),
            'count': len(season_data)
        }
    
    return seasonal_impact

def create_economic_proxy_variables(df):
    """경제 지표 프록시 변수 생성"""
    print("\n📈 경제 지표 프록시 변수 생성 중...")
    
    df_econ = df.copy()
    
    # 연도별 전력 수요 성장률 (GDP 성장률 프록시)
    yearly_power = df_econ.groupby('year')['최대전력(MW)'].mean()
    yearly_growth = yearly_power.pct_change() * 100
    
    # 산업활동 지수 프록시 (평일 전력 수요)
    df_econ['is_weekday'] = ~df_econ['weekday'].isin([5, 6])
    monthly_industrial = df_econ[df_econ['is_weekday']].groupby(['year', 'month'])['최대전력(MW)'].mean()
    
    # 전력 집약도 지수 (주말 대비 평일 전력 수요 비율)
    monthly_weekend = df_econ[~df_econ['is_weekday']].groupby(['year', 'month'])['최대전력(MW)'].mean()
    power_intensity = {}
    
    for year in df_econ['year'].unique():
        for month in range(1, 13):
            weekday_key = (year, month)
            if weekday_key in monthly_industrial.index and weekday_key in monthly_weekend.index:
                weekend_power = monthly_weekend[weekday_key]
                weekday_power = monthly_industrial[weekday_key]
                if weekend_power > 0:
                    power_intensity[weekday_key] = weekday_power / weekend_power
    
    economic_indicators = {
        'yearly_growth': yearly_growth.to_dict(),
        'monthly_industrial_proxy': monthly_industrial.to_dict(),
        'power_intensity_ratio': power_intensity
    }
    
    return economic_indicators

def visualize_external_factors(df_analysis, holiday_impact, comparison_stats, event_impact, seasonal_impact):
    """외부 요인 분석 결과 시각화"""
    print("\n📊 외부 요인 분석 시각화 생성 중...")
    
    # 1. 공휴일 vs 평일/주말 비교
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    
    # 평일/주말/공휴일 비교 박스플롯
    day_types = []
    power_values = []
    
    for day_type in ['평일', '주말', '공휴일']:
        if day_type == '평일':
            data = df_analysis[(~df_analysis['is_holiday']) & (~df_analysis['is_weekend'])]['최대전력(MW)']
        elif day_type == '주말':
            data = df_analysis[df_analysis['is_weekend'] & (~df_analysis['is_holiday'])]['최대전력(MW)']
        else:  # 공휴일
            data = df_analysis[df_analysis['is_holiday']]['최대전력(MW)']
        
        day_types.extend([day_type] * len(data))
        power_values.extend(data.tolist())
    
    box_data = pd.DataFrame({'day_type': day_types, 'power': power_values})
    sns.boxplot(data=box_data, x='day_type', y='power', ax=axes[0, 0])
    axes[0, 0].set_title('평일/주말/공휴일 전력 수요 분포', fontsize=14, fontweight='bold')
    axes[0, 0].set_ylabel('전력 수요 (MW)')
    
    # 공휴일별 평균 전력 수요
    if holiday_impact:
        holiday_names = list(holiday_impact.keys())
        holiday_means = [holiday_impact[name]['mean_power'] for name in holiday_names]
        
        axes[0, 1].bar(holiday_names, holiday_means, color='coral', alpha=0.7)
        axes[0, 1].set_title('공휴일별 평균 전력 수요', fontsize=14, fontweight='bold')
        axes[0, 1].set_ylabel('평균 전력 수요 (MW)')
        axes[0, 1].tick_params(axis='x', rotation=45)
    
    # 월별 평일/주말 전력 수요 패턴
    monthly_weekday = df_analysis[df_analysis['is_weekday']].groupby('month')['최대전력(MW)'].mean()
    monthly_weekend = df_analysis[~df_analysis['is_weekday']].groupby('month')['최대전력(MW)'].mean()
    
    months = range(1, 13)
    axes[1, 0].plot(months, monthly_weekday, marker='o', label='평일', linewidth=2)
    axes[1, 0].plot(months, monthly_weekend, marker='s', label='주말', linewidth=2)
    axes[1, 0].set_title('월별 평일/주말 전력 수요 패턴', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('월')
    axes[1, 0].set_ylabel('평균 전력 수요 (MW)')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # 계절별 전력 수요
    if seasonal_impact:
        seasons = ['봄', '여름', '가을', '겨울']
        seasonal_means = [seasonal_impact[season]['mean'] for season in seasons if season in seasonal_impact]
        seasonal_names = [season for season in seasons if season in seasonal_impact]
        
        colors = ['lightgreen', 'orange', 'brown', 'lightblue']
        axes[1, 1].bar(seasonal_names, seasonal_means, color=colors[:len(seasonal_names)], alpha=0.7)
        axes[1, 1].set_title('계절별 평균 전력 수요', fontsize=14, fontweight='bold')
        axes[1, 1].set_ylabel('평균 전력 수요 (MW)')
    
    plt.tight_layout()
    plt.savefig('results/eda/05_external_factors/external_factors_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. 특별 이벤트 영향 시각화
    if event_impact:
        fig, ax = plt.subplots(1, 1, figsize=(15, 8))
        
        event_names = list(event_impact.keys())
        change_percentages = [event_impact[name]['change_percent'] for name in event_names]
        
        colors = ['red' if x < 0 else 'blue' for x in change_percentages]
        bars = ax.bar(range(len(event_names)), change_percentages, color=colors, alpha=0.7)
        
        ax.set_title('특별 이벤트별 전력 수요 변화율 (전년 동기 대비)', fontsize=14, fontweight='bold')
        ax.set_ylabel('변화율 (%)')
        ax.set_xticks(range(len(event_names)))
        ax.set_xticklabels(event_names, rotation=45, ha='right')
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.grid(True, alpha=0.3)
        
        # 값 표시
        for i, (bar, value) in enumerate(zip(bars, change_percentages)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (0.5 if value > 0 else -1.5),
                   f'{value:.1f}%', ha='center', va='bottom' if value > 0 else 'top')
        
        plt.tight_layout()
        plt.savefig('results/eda/05_external_factors/special_events_impact.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    print("✅ 외부 요인 분석 시각화 저장 완료")

def generate_external_factors_report(df, holiday_impact, comparison_stats, event_impact, seasonal_impact, economic_indicators):
    """외부 요인 분석 종합 보고서 생성"""
    print("\n📝 외부 요인 분석 보고서 생성 중...")
    
    # 평일 대비 변화율 계산
    baseline_power = comparison_stats['평일']['mean']
    weekend_change = ((comparison_stats['주말']['mean'] - baseline_power) / baseline_power) * 100
    holiday_change = ((comparison_stats['공휴일']['mean'] - baseline_power) / baseline_power) * 100
    
    report = f"""
=== 🌟 외부 요인 및 특별 이벤트 분석 보고서 ===

📊 데이터 개요:
- 분석 기간: {df['date'].min().strftime('%Y년 %m월 %d일')} ~ {df['date'].max().strftime('%Y년 %m월 %d일')}
- 총 분석 일수: {len(df):,}일
- 분석 범위: 공휴일, 특별 이벤트, 계절 패턴, 경제 지표 프록시

🎉 공휴일 영향 분석:

1. 일반적 패턴:
   - 평일 평균: {comparison_stats['평일']['mean']:,.0f} MW
   - 주말 평균: {comparison_stats['주말']['mean']:,.0f} MW ({weekend_change:+.1f}%)
   - 공휴일 평균: {comparison_stats['공휴일']['mean']:,.0f} MW ({holiday_change:+.1f}%)

2. 주요 발견사항:
   - 주말 전력 수요는 평일 대비 {abs(weekend_change):.1f}% {'감소' if weekend_change < 0 else '증가'}
   - 공휴일 전력 수요는 평일 대비 {abs(holiday_change):.1f}% {'감소' if holiday_change < 0 else '증가'}
   - 공휴일이 주말보다 전력 수요가 {'높음' if comparison_stats['공휴일']['mean'] > comparison_stats['주말']['mean'] else '낮음'}

3. 공휴일별 특성:"""

    if holiday_impact:
        report += "\n"
        for holiday_name, impact in holiday_impact.items():
            change_vs_baseline = ((impact['mean_power'] - baseline_power) / baseline_power) * 100
            report += f"   - {holiday_name}: {impact['mean_power']:,.0f} MW ({change_vs_baseline:+.1f}%, {impact['count']}일)\n"

    report += f"""
🌟 특별 이벤트 영향:"""

    if event_impact:
        # 영향이 큰 순서로 정렬
        sorted_events = sorted(event_impact.items(), key=lambda x: abs(x[1]['change_percent']), reverse=True)
        
        report += f"\n주요 특별 이벤트 영향 (전년 동기 대비):\n"
        for event_name, impact in sorted_events[:10]:  # 상위 10개만 표시
            report += f"   - {event_name}: {impact['change_percent']:+.1f}% ({impact['period']})\n"
        
        # 가장 큰 영향
        biggest_impact = max(event_impact.items(), key=lambda x: abs(x[1]['change_percent']))
        report += f"\n최대 영향 이벤트: {biggest_impact[0]} ({biggest_impact[1]['change_percent']:+.1f}%)"

    report += f"""

🌸 계절별 패턴 분석:"""

    if seasonal_impact:
        for season in ['봄', '여름', '가을', '겨울']:
            if season in seasonal_impact:
                season_data = seasonal_impact[season]
                season_change = ((season_data['mean'] - baseline_power) / baseline_power) * 100
                report += f"\n   - {season}: {season_data['mean']:,.0f} MW ({season_change:+.1f}%, {season_data['count']}일)"

    report += f"""

📈 경제 지표 프록시 변수:

1. 연도별 전력 수요 성장률 (GDP 성장률 프록시):"""

    if 'yearly_growth' in economic_indicators:
        for year, growth in economic_indicators['yearly_growth'].items():
            if not pd.isna(growth):
                report += f"\n   - {year}년: {growth:+.1f}%"

    report += f"""

2. 전력 집약도 지수:
   - 평일/주말 전력 수요 비율로 산업 활동 강도 측정
   - 비율이 높을수록 산업 활동이 활발함을 의미

💡 예측 모델링을 위한 권장사항:

1. 핵심 외부 요인 변수:
   - is_holiday: 공휴일 여부 (중요도: 높음)
   - is_weekend: 주말 여부 (중요도: 높음)
   - holiday_type: 공휴일 유형별 세분화 (중요도: 중간)
   - season: 계절 정보 (중요도: 높음)

2. 특별 이벤트 변수:
   - major_event: 올림픽, 월드컵 등 대형 스포츠 이벤트
   - economic_crisis: 경제 위기 기간
   - pandemic: 팬데믹 기간 (코로나19 등)

3. 경제 지표 프록시:
   - yearly_growth_rate: 전력 수요 기반 경제 성장률
   - industrial_activity_index: 평일 전력 수요 기반 산업 활동 지수
   - power_intensity_ratio: 평일/주말 전력 비율

4. 모델링 전략:
   - 공휴일과 주말 효과를 별도 변수로 처리
   - 계절별 차별화된 모델 또는 계절 더미 변수 활용
   - 특별 이벤트는 기간별 더미 변수로 처리
   - 경제 지표는 라그를 고려한 피처 엔지니어링 적용

📁 생성된 분석 파일:
- external_factors_analysis.png: 공휴일/계절별 전력 수요 분석
- special_events_impact.png: 특별 이벤트 영향 분석
- external_factors_analysis_report.txt: 종합 분석 보고서

분석 완료 시간: {pd.Timestamp.now().strftime('%Y년 %m월 %d일 %H시 %M분')}
"""
    
    # 보고서 저장
    with open('results/eda/05_external_factors/external_factors_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("✅ 외부 요인 분석 보고서 저장: external_factors_analysis_report.txt")
    print(report)

def main():
    """메인 실행 함수"""
    print("🚀 외부 요인 및 특별 이벤트 분석 시작")
    print("=" * 70)
    
    # 결과 폴더 생성
    import os
    os.makedirs('results/eda/05_external_factors', exist_ok=True)
    
    try:
        # 1. 데이터 로딩
        df = load_and_prepare_data()
        
        # 2. 한국 공휴일 정보 생성
        holidays_df = create_korean_holidays()
        
        # 3. 공휴일 영향 분석
        df_analysis, holiday_impact, comparison_stats = analyze_holiday_impact(df, holidays_df)
        
        # 4. 특별 이벤트 영향 분석
        event_impact = analyze_special_events(df)
        
        # 5. 계절별 패턴 분석
        seasonal_impact = analyze_seasonal_patterns(df)
        
        # 6. 경제 지표 프록시 변수 생성
        economic_indicators = create_economic_proxy_variables(df)
        
        # 7. 시각화
        visualize_external_factors(df_analysis, holiday_impact, comparison_stats, event_impact, seasonal_impact)
        
        # 8. 종합 보고서 생성
        generate_external_factors_report(df, holiday_impact, comparison_stats, event_impact, seasonal_impact, economic_indicators)
        
        print("\n" + "=" * 70)
        print("🎉 외부 요인 및 특별 이벤트 분석 완료!")
        print("📁 모든 결과가 'results/eda/05_external_factors/' 폴더에 저장되었습니다.")
        print("🎯 예측 모델링에 활용할 외부 요인 피처들이 준비되었습니다.")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        raise

if __name__ == "__main__":
    main() 