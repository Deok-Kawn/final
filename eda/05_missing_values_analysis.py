#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
누락값 상세 분석
EDA 추가 분석: 누락값의 패턴, 위치, 시기별 분포 등을 종합적으로 분석
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정 (Mac용)
plt.rcParams['font.family'] = ['Arial Unicode MS', 'AppleGothic', 'Malgun Gothic']
plt.rcParams['axes.unicode_minus'] = False

def load_and_prepare_data():
    """데이터 로딩 및 기본 전처리"""
    print("📊 데이터 로딩 중...")
    
    # 데이터 로딩
    df = pd.read_csv('data/shared/data.csv')
    
    # 날짜 변환
    df['date'] = pd.to_datetime(df['date'], format='%Y.%m.%d')
    df = df.sort_values('date').reset_index(drop=True)
    
    print(f"✅ 데이터 로딩 완료: {df.shape[0]}행 × {df.shape[1]}열")
    return df

def analyze_missing_values(df):
    """누락값 상세 분석"""
    print("\n🔍 누락값 상세 분석 시작...")
    
    # 1. 기본 누락값 통계
    missing_count = df.isnull().sum()
    missing_percent = (df.isnull().sum() / len(df) * 100).round(3)
    
    missing_summary = pd.DataFrame({
        '컬럼명': missing_count.index,
        '누락값 개수': missing_count.values,
        '누락값 비율(%)': missing_percent.values
    })
    
    print("📋 누락값 기본 통계:")
    print(missing_summary)
    
    # 2. 전력 데이터 누락값 위치 확인
    if '최대전력(MW)' in df.columns:
        power_missing = df[df['최대전력(MW)'].isnull()]
        
        if len(power_missing) > 0:
            print(f"\n⚠️ 전력 데이터 누락값 발견: {len(power_missing)}개")
            print("누락값이 있는 날짜들:")
            for idx, row in power_missing.iterrows():
                print(f"  - {row['date'].strftime('%Y년 %m월 %d일 (%A)')}")
            
            # 누락값 날짜 분석
            power_missing_copy = power_missing.copy()
            power_missing_copy['year'] = power_missing_copy['date'].dt.year
            power_missing_copy['month'] = power_missing_copy['date'].dt.month
            power_missing_copy['dayofweek'] = power_missing_copy['date'].dt.dayofweek
            power_missing_copy['day_name'] = power_missing_copy['date'].dt.day_name()
            
            print("\n📅 누락값 시기별 분포:")
            print("연도별:")
            year_dist = power_missing_copy['year'].value_counts().sort_index()
            for year, count in year_dist.items():
                print(f"  - {year}년: {count}개")
            
            print("\n월별:")
            month_dist = power_missing_copy['month'].value_counts().sort_index()
            month_names = ['1월', '2월', '3월', '4월', '5월', '6월', 
                          '7월', '8월', '9월', '10월', '11월', '12월']
            for month, count in month_dist.items():
                print(f"  - {month_names[month-1]}: {count}개")
            
            print("\n요일별:")
            dayofweek_dist = power_missing_copy['day_name'].value_counts()
            for day, count in dayofweek_dist.items():
                print(f"  - {day}: {count}개")
            
            return power_missing_copy, missing_summary
        else:
            print("\n✅ 전력 데이터에 누락값 없음")
            return None, missing_summary
    
    return None, missing_summary

def analyze_missing_patterns(df, power_missing):
    """누락값 패턴 분석"""
    print("\n🔍 누락값 패턴 분석...")
    
    if power_missing is None or len(power_missing) == 0:
        print("누락값이 없어서 패턴 분석을 건너뜁니다.")
        return
    
    # 1. 연속된 누락값 확인
    missing_dates = power_missing['date'].sort_values().tolist()
    consecutive_groups = []
    current_group = [missing_dates[0]]
    
    for i in range(1, len(missing_dates)):
        if (missing_dates[i] - missing_dates[i-1]).days == 1:
            current_group.append(missing_dates[i])
        else:
            consecutive_groups.append(current_group)
            current_group = [missing_dates[i]]
    consecutive_groups.append(current_group)
    
    print("📈 연속된 누락값 그룹:")
    for i, group in enumerate(consecutive_groups):
        if len(group) == 1:
            print(f"  그룹 {i+1}: {group[0].strftime('%Y-%m-%d')} (1일)")
        else:
            print(f"  그룹 {i+1}: {group[0].strftime('%Y-%m-%d')} ~ {group[-1].strftime('%Y-%m-%d')} ({len(group)}일 연속)")
    
    # 2. 공휴일/주말과의 관계 분석
    weekend_missing = power_missing[power_missing['dayofweek'] >= 5]
    weekday_missing = power_missing[power_missing['dayofweek'] < 5]
    
    print(f"\n📅 주말/평일 분포:")
    print(f"  - 주말 누락: {len(weekend_missing)}개")
    print(f"  - 평일 누락: {len(weekday_missing)}개")
    
    # 3. 누락값 주변 데이터 확인
    print("\n🔍 누락값 전후 데이터 확인:")
    for date in missing_dates[:5]:  # 상위 5개만 표시
        # 전후 3일씩 확인
        start_date = date - timedelta(days=3)
        end_date = date + timedelta(days=3)
        
        context_data = df[(df['date'] >= start_date) & (df['date'] <= end_date)].copy()
        context_data['is_missing'] = context_data['최대전력(MW)'].isnull()
        
        print(f"\n📅 {date.strftime('%Y-%m-%d')} 주변 데이터:")
        for _, row in context_data.iterrows():
            status = "❌ 누락" if row['is_missing'] else f"{row['최대전력(MW)']:,.0f} MW"
            marker = "👉 " if row['date'] == date else "   "
            print(f"{marker}{row['date'].strftime('%Y-%m-%d (%a)')}: {status}")

def create_missing_visualizations(df, power_missing, missing_summary):
    """누락값 시각화 생성"""
    print("\n📊 누락값 시각화 생성 중...")
    
    # 1. 누락값 위치 시각화 (시계열)
    plt.figure(figsize=(15, 8))
    
    # 전체 데이터 플롯
    plt.subplot(2, 1, 1)
    plt.plot(df['date'], df['최대전력(MW)'], linewidth=0.8, alpha=0.7, color='blue')
    
    # 누락값 위치 표시
    if power_missing is not None and len(power_missing) > 0:
        for _, row in power_missing.iterrows():
            plt.axvline(x=row['date'], color='red', linestyle='--', alpha=0.8, linewidth=2)
    
    plt.title('전력 수요 시계열 데이터 - 누락값 위치 표시', fontsize=14, fontweight='bold')
    plt.ylabel('최대전력(MW)')
    plt.grid(True, alpha=0.3)
    plt.legend(['전력 수요', '누락값'], loc='upper left')
    
    # 2. 누락값 연도별 분포
    plt.subplot(2, 1, 2)
    if power_missing is not None and len(power_missing) > 0:
        year_counts = power_missing['year'].value_counts().sort_index()
        plt.bar(year_counts.index, year_counts.values, color='orange', alpha=0.7)
        plt.title('누락값 연도별 분포', fontsize=12, fontweight='bold')
        plt.xlabel('연도')
        plt.ylabel('누락값 개수')
        plt.grid(True, alpha=0.3)
        
        # 값 표시
        for year, count in year_counts.items():
            plt.text(year, count + 0.1, str(count), ha='center', va='bottom')
    else:
        plt.text(0.5, 0.5, '누락값이 없습니다', ha='center', va='center', 
                transform=plt.gca().transAxes, fontsize=16)
        plt.title('누락값 연도별 분포', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('results/eda/missing_values_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. 누락값 히트맵 (월별, 요일별)
    if power_missing is not None and len(power_missing) > 0:
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # 월별 분포
        month_counts = power_missing['month'].value_counts().reindex(range(1, 13), fill_value=0)
        month_names = ['1월', '2월', '3월', '4월', '5월', '6월', 
                      '7월', '8월', '9월', '10월', '11월', '12월']
        
        axes[0].bar(range(1, 13), month_counts.values, color='lightcoral', alpha=0.7)
        axes[0].set_xticks(range(1, 13))
        axes[0].set_xticklabels(month_names, rotation=45)
        axes[0].set_title('누락값 월별 분포')
        axes[0].set_ylabel('누락값 개수')
        axes[0].grid(True, alpha=0.3)
        
        # 요일별 분포
        dayofweek_counts = power_missing['dayofweek'].value_counts().reindex(range(7), fill_value=0)
        day_names = ['월', '화', '수', '목', '금', '토', '일']
        
        axes[1].bar(range(7), dayofweek_counts.values, color='lightblue', alpha=0.7)
        axes[1].set_xticks(range(7))
        axes[1].set_xticklabels(day_names)
        axes[1].set_title('누락값 요일별 분포')
        axes[1].set_ylabel('누락값 개수')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('results/eda/missing_values_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    print("✅ 시각화 완료: missing_values_analysis.png, missing_values_distribution.png")

def generate_missing_data_report(df, power_missing, missing_summary):
    """누락값 분석 보고서 생성"""
    print("\n📝 누락값 분석 보고서 생성 중...")
    
    # 전체 데이터 기간 확인
    start_date = df['date'].min()
    end_date = df['date'].max()
    total_days = (end_date - start_date).days + 1
    expected_data_points = total_days
    actual_data_points = len(df)
    
    # 누락된 날짜 찾기 (날짜 연속성 확인)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    missing_dates_in_range = set(date_range) - set(df['date'])
    
    report = f"""
=== 📊 누락값 분석 상세 보고서 ===

📋 기본 정보:
- 전체 데이터 기간: {start_date.strftime('%Y년 %m월 %d일')} ~ {end_date.strftime('%Y년 %m월 %d일')}
- 예상 데이터 포인트: {expected_data_points:,}개
- 실제 데이터 포인트: {actual_data_points:,}개
- 전체적으로 누락된 날짜: {len(missing_dates_in_range)}개

📊 전력 데이터 누락값:
- 전력 데이터 누락: {missing_summary.loc[missing_summary['컬럼명'] == '최대전력(MW)', '누락값 개수'].iloc[0] if '최대전력(MW)' in missing_summary['컬럼명'].values else 0}개
- 누락 비율: {missing_summary.loc[missing_summary['컬럼명'] == '최대전력(MW)', '누락값 비율(%)'].iloc[0] if '최대전력(MW)' in missing_summary['컬럼명'].values else 0}%

"""
    
    if power_missing is not None and len(power_missing) > 0:
        report += f"""
🔍 누락값 세부 분석:
- 가장 이른 누락값: {power_missing['date'].min().strftime('%Y년 %m월 %d일')}
- 가장 늦은 누락값: {power_missing['date'].max().strftime('%Y년 %m월 %d일')}
- 누락값 분포 기간: {(power_missing['date'].max() - power_missing['date'].min()).days + 1}일
"""
        
        # 연도별 분포
        year_dist = power_missing['year'].value_counts().sort_index()
        report += "\n연도별 누락값 분포:\n"
        for year, count in year_dist.items():
            report += f"  - {year}년: {count}개\n"
        
        # 요일별 분포
        dayofweek_dist = power_missing['dayofweek'].value_counts()
        weekend_count = power_missing[power_missing['dayofweek'] >= 5].shape[0]
        weekday_count = power_missing[power_missing['dayofweek'] < 5].shape[0]
        
        report += f"""
요일별 누락값 분포:
  - 평일 누락: {weekday_count}개
  - 주말 누락: {weekend_count}개
  - 주말 누락 비율: {weekend_count/len(power_missing)*100:.1f}%
"""
    
    else:
        report += "\n✅ 전력 데이터에 누락값이 없습니다.\n"
    
    # 전체적으로 누락된 날짜가 있다면
    if len(missing_dates_in_range) > 0:
        report += f"""
📅 데이터셋에서 완전히 누락된 날짜들 (상위 10개):
"""
        sorted_missing_dates = sorted(list(missing_dates_in_range))[:10]
        for missing_date in sorted_missing_dates:
            report += f"  - {missing_date.strftime('%Y년 %m월 %d일 (%A)')}\n"
        
        if len(missing_dates_in_range) > 10:
            report += f"  ... 및 {len(missing_dates_in_range) - 10}개 더\n"
    
    report += f"""
💡 권장사항:
1. 누락값이 적으므로({'주로 특정 시기에 집중' if power_missing is not None and len(power_missing) > 0 else '문제없음'}) 선형보간법 또는 계절성을 고려한 보간법 사용 권장
2. 주변 날짜의 패턴을 활용한 예측값 대체 고려
3. 누락값이 특정 패턴(주말, 공휴일 등)과 연관성이 있는지 추가 확인 필요
4. 모델링 시 누락값 처리 전략을 사전에 수립
"""
    
    # 보고서 저장
    with open('results/eda/missing_values_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("✅ 보고서 저장 완료: missing_values_report.txt")
    print(report)

def main():
    """메인 실행 함수"""
    print("🚀 누락값 상세 분석 시작")
    print("=" * 50)
    
    try:
        # 데이터 로딩
        df = load_and_prepare_data()
        
        # 누락값 분석
        power_missing, missing_summary = analyze_missing_values(df)
        
        # 누락값 패턴 분석
        analyze_missing_patterns(df, power_missing)
        
        # 시각화 생성
        create_missing_visualizations(df, power_missing, missing_summary)
        
        # 보고서 생성
        generate_missing_data_report(df, power_missing, missing_summary)
        
        print("\n" + "=" * 50)
        print("🎉 누락값 상세 분석 완료!")
        print("📁 생성된 파일들이 'results/eda/' 폴더에 저장되었습니다.")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        raise

if __name__ == "__main__":
    main() 