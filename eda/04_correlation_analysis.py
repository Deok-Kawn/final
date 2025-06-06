#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
상관관계 분석 및 피처 관계 분석
TaskMaster 작업 2.5: Generate Correlation Analysis and Feature Relationships
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = ['Arial Unicode MS', 'AppleGothic', 'Malgun Gothic']
plt.rcParams['axes.unicode_minus'] = False

def load_and_prepare_data():
    """데이터 로딩 및 피처 엔지니어링"""
    print("📊 데이터 로딩 및 전처리 시작...")
    
    # 데이터 로딩
    df = pd.read_csv('data/shared/data.csv')
    
    # 날짜 변환
    df['date'] = pd.to_datetime(df['date'], format='%Y.%m.%d')
    df = df.sort_values('date').reset_index(drop=True)
    
    # 기본 시간 기반 피처 생성
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['dayofweek'] = df['date'].dt.dayofweek  # 0=월요일, 6=일요일
    df['dayofyear'] = df['date'].dt.dayofyear
    df['week'] = df['date'].dt.isocalendar().week
    df['quarter'] = df['date'].dt.quarter
    
    # 계절 변수
    def get_season(month):
        if month in [12, 1, 2]:
            return 0  # 겨울
        elif month in [3, 4, 5]:
            return 1  # 봄
        elif month in [6, 7, 8]:
            return 2  # 여름
        else:
            return 3  # 가을
    
    df['season'] = df['month'].apply(get_season)
    
    # 주말/평일 구분
    df['is_weekend'] = (df['dayofweek'] >= 5).astype(int)
    df['is_weekday'] = (df['dayofweek'] < 5).astype(int)
    
    # 휴일 근사치 (간단한 공휴일)
    holidays = ['01-01', '03-01', '05-05', '06-06', '08-15', '10-03', '10-09', '12-25']
    df['is_holiday'] = df['date'].dt.strftime('%m-%d').isin(holidays).astype(int)
    
    # 래그 피처 (과거 전력 수요)
    df['power_lag1'] = df['최대전력(MW)'].shift(1)  # 1일 전
    df['power_lag7'] = df['최대전력(MW)'].shift(7)  # 1주일 전
    df['power_lag30'] = df['최대전력(MW)'].shift(30)  # 1개월 전
    df['power_lag365'] = df['최대전력(MW)'].shift(365)  # 1년 전
    
    # 이동평균 피처
    df['power_ma3'] = df['최대전력(MW)'].rolling(window=3, min_periods=1).mean()  # 3일 이동평균
    df['power_ma7'] = df['최대전력(MW)'].rolling(window=7, min_periods=1).mean()  # 1주일 이동평균
    df['power_ma30'] = df['최대전력(MW)'].rolling(window=30, min_periods=1).mean()  # 1개월 이동평균
    
    # 변화율 피처
    df['power_change_1d'] = df['최대전력(MW)'].pct_change(1) * 100  # 1일 변화율
    df['power_change_7d'] = df['최대전력(MW)'].pct_change(7) * 100  # 1주일 변화율
    
    # 롤링 통계량
    df['power_std7'] = df['최대전력(MW)'].rolling(window=7, min_periods=1).std()  # 1주일 표준편차
    df['power_min7'] = df['최대전력(MW)'].rolling(window=7, min_periods=1).min()  # 1주일 최솟값
    df['power_max7'] = df['최대전력(MW)'].rolling(window=7, min_periods=1).max()  # 1주일 최댓값
    
    # 시간 트렌드 (연속적인 날짜 번호)
    df['time_trend'] = (df['date'] - df['date'].min()).dt.days
    
    # 계절성 인코딩 (원형 인코딩)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    df['dayofyear_sin'] = np.sin(2 * np.pi * df['dayofyear'] / 365)
    df['dayofyear_cos'] = np.cos(2 * np.pi * df['dayofyear'] / 365)
    
    print(f"✅ 피처 생성 완료: {df.shape[1]}개 변수, {df.shape[0]}개 관측치")
    return df

def create_correlation_analysis(df):
    """상관관계 분석 수행"""
    print("\n🔍 상관관계 분석 시작...")
    
    # 수치형 변수만 선택
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if 'date' in df.columns:
        numeric_cols = [col for col in numeric_cols if col != 'date']
    
    # 상관관계 매트릭스 계산
    correlation_matrix = df[numeric_cols].corr()
    
    # 전력 수요와 다른 변수들의 상관관계 추출
    power_correlations = correlation_matrix['최대전력(MW)'].abs().sort_values(ascending=False)
    
    print("📈 전력 수요와 상관관계가 높은 상위 10개 변수:")
    for i, (var, corr) in enumerate(power_correlations.head(11).items(), 1):
        if var != '최대전력(MW)':  # 자기 자신 제외
            print(f"{i:2d}. {var}: {corr:.3f}")
    
    return correlation_matrix, power_correlations, numeric_cols

def create_visualizations(df, correlation_matrix, power_correlations, numeric_cols):
    """시각화 생성"""
    print("\n📊 시각화 생성 중...")
    
    # 1. 전체 상관관계 히트맵
    plt.figure(figsize=(20, 16))
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    sns.heatmap(correlation_matrix, 
                mask=mask,
                annot=True, 
                fmt='.2f',
                cmap='RdBu_r',
                center=0,
                square=True,
                linewidths=0.5,
                cbar_kws={"shrink": .8},
                annot_kws={'size': 8})
    plt.title('변수 간 상관관계 히트맵', fontsize=16, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('results/eda/correlation_heatmap_full.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. 전력 수요와 주요 변수들의 상관관계 (상위 15개)
    top_vars = power_correlations.head(16).index[1:16]  # 자기 자신 제외하고 상위 15개
    selected_vars = ['최대전력(MW)'] + list(top_vars)
    
    plt.figure(figsize=(12, 10))
    corr_subset = correlation_matrix.loc[selected_vars, selected_vars]
    sns.heatmap(corr_subset,
                annot=True,
                fmt='.3f',
                cmap='RdBu_r',
                center=0,
                square=True,
                linewidths=0.5)
    plt.title('전력 수요와 주요 변수들의 상관관계', fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('results/eda/correlation_heatmap_main.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. 전력 수요 상관관계 막대 그래프
    plt.figure(figsize=(12, 8))
    top_15_corr = power_correlations.head(16)[1:16]  # 자기 자신 제외
    colors = ['red' if x < 0 else 'blue' for x in correlation_matrix.loc[top_15_corr.index, '최대전력(MW)']]
    
    bars = plt.barh(range(len(top_15_corr)), 
                    correlation_matrix.loc[top_15_corr.index, '최대전력(MW)'],
                    color=colors, alpha=0.7)
    plt.yticks(range(len(top_15_corr)), top_15_corr.index)
    plt.xlabel('상관계수', fontsize=12)
    plt.title('전력 수요와 다른 변수들의 상관관계 (상위 15개)', fontsize=14, fontweight='bold')
    plt.grid(axis='x', alpha=0.3)
    
    # 값 표시
    for i, (idx, val) in enumerate(zip(top_15_corr.index, correlation_matrix.loc[top_15_corr.index, '최대전력(MW)'])):
        plt.text(val + 0.01 if val >= 0 else val - 0.01, i, f'{val:.3f}', 
                va='center', ha='left' if val >= 0 else 'right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('results/eda/correlation_barplot.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. 시간 변수들과 전력 수요의 관계 산점도
    time_vars = ['year', 'month', 'dayofweek', 'season', 'time_trend']
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    for i, var in enumerate(time_vars):
        if i < len(axes):
            axes[i].scatter(df[var], df['최대전력(MW)'], alpha=0.5, s=1)
            axes[i].set_xlabel(var)
            axes[i].set_ylabel('최대전력(MW)')
            axes[i].set_title(f'{var} vs 최대전력 수요')
            
            # 상관계수 표시
            corr = df[var].corr(df['최대전력(MW)'])
            axes[i].text(0.05, 0.95, f'상관계수: {corr:.3f}', 
                        transform=axes[i].transAxes, fontsize=10,
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # 빈 subplot 제거
    if len(time_vars) < len(axes):
        fig.delaxes(axes[-1])
    
    plt.suptitle('시간 변수들과 전력 수요의 관계', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('results/eda/time_variables_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. 래그 변수들과 전력 수요의 관계
    lag_vars = ['power_lag1', 'power_lag7', 'power_lag30', 'power_lag365']
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.flatten()
    
    for i, var in enumerate(lag_vars):
        if var in df.columns:
            # NaN 제거
            mask = ~(df[var].isna() | df['최대전력(MW)'].isna())
            x_data = df.loc[mask, var]
            y_data = df.loc[mask, '최대전력(MW)']
            
            axes[i].scatter(x_data, y_data, alpha=0.5, s=1)
            axes[i].set_xlabel(f'{var} (MW)')
            axes[i].set_ylabel('최대전력(MW)')
            axes[i].set_title(f'{var} vs 현재 전력 수요')
            
            # 회귀선 추가
            z = np.polyfit(x_data, y_data, 1)
            p = np.poly1d(z)
            axes[i].plot(x_data, p(x_data), "r--", alpha=0.8)
            
            # 상관계수 표시
            corr = x_data.corr(y_data)
            axes[i].text(0.05, 0.95, f'상관계수: {corr:.3f}', 
                        transform=axes[i].transAxes, fontsize=10,
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.suptitle('래그 변수들과 전력 수요의 관계', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('results/eda/lag_variables_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ 시각화 완료: 5개 차트 생성")

def analyze_feature_relationships(df):
    """피처 관계 심화 분석"""
    print("\n🔬 피처 관계 심화 분석...")
    
    # 계절별 전력 수요 분석
    seasonal_analysis = df.groupby('season')['최대전력(MW)'].agg([
        'mean', 'std', 'min', 'max', 'count'
    ]).round(2)
    
    season_names = {0: '겨울', 1: '봄', 2: '여름', 3: '가을'}
    seasonal_analysis.index = [season_names[i] for i in seasonal_analysis.index]
    
    print("\n📊 계절별 전력 수요 통계:")
    print(seasonal_analysis)
    
    # 요일별 전력 수요 분석
    weekday_analysis = df.groupby('dayofweek')['최대전력(MW)'].agg([
        'mean', 'std', 'count'
    ]).round(2)
    
    weekday_names = ['월', '화', '수', '목', '금', '토', '일']
    weekday_analysis.index = weekday_names
    
    print("\n📅 요일별 전력 수요 통계:")
    print(weekday_analysis)
    
    # 월별 전력 수요 분석
    monthly_analysis = df.groupby('month')['최대전력(MW)'].agg([
        'mean', 'std', 'count'
    ]).round(2)
    
    print("\n📆 월별 전력 수요 통계:")
    print(monthly_analysis)
    
    return seasonal_analysis, weekday_analysis, monthly_analysis

def save_correlation_results(correlation_matrix, power_correlations):
    """상관관계 분석 결과 저장"""
    print("\n💾 분석 결과 저장 중...")
    
    # 전체 상관관계 매트릭스 저장
    correlation_matrix.to_csv('results/eda/correlation_matrix.csv')
    
    # 전력 수요와의 상관관계 저장
    power_corr_df = pd.DataFrame({
        'variable': power_correlations.index,
        'correlation': power_correlations.values,
        'abs_correlation': power_correlations.values
    })
    power_corr_df.to_csv('results/eda/power_correlations.csv', index=False)
    
    print("✅ 결과 파일 저장 완료")

def main():
    """메인 실행 함수"""
    print("🚀 상관관계 분석 및 피처 관계 분석 시작")
    print("=" * 50)
    
    try:
        # 데이터 로딩 및 전처리
        df = load_and_prepare_data()
        
        # 상관관계 분석
        correlation_matrix, power_correlations, numeric_cols = create_correlation_analysis(df)
        
        # 시각화 생성
        create_visualizations(df, correlation_matrix, power_correlations, numeric_cols)
        
        # 피처 관계 심화 분석
        seasonal_analysis, weekday_analysis, monthly_analysis = analyze_feature_relationships(df)
        
        # 결과 저장
        save_correlation_results(correlation_matrix, power_correlations)
        
        print("\n" + "=" * 50)
        print("🎉 상관관계 분석 완료!")
        print(f"📁 생성된 파일들이 'results/eda/' 폴더에 저장되었습니다.")
        print("\n📊 주요 발견사항:")
        print("• 전력 수요와 가장 상관관계가 높은 변수들을 식별했습니다")
        print("• 시간 관련 변수들의 영향도를 분석했습니다")
        print("• 래그 변수들의 예측 가능성을 확인했습니다")
        print("• 계절성 패턴의 구체적인 수치를 확인했습니다")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        raise

if __name__ == "__main__":
    main() 