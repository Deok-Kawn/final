"""
시계열 데이터 시각화 유틸리티
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False


class TimeSeriesVisualizer:
    """시계열 데이터 시각화 클래스"""
    
    def __init__(self, figsize=(15, 8), style='whitegrid'):
        self.figsize = figsize
        sns.set_style(style)
        
    def plot_time_series(self, data, date_col=None, value_col=None, 
                        title="시계열 데이터", save_path=None):
        """기본 시계열 그래프"""
        plt.figure(figsize=self.figsize)
        
        if date_col and value_col:
            plt.plot(pd.to_datetime(data[date_col]), data[value_col], linewidth=1.5)
            plt.xlabel('날짜')
        else:
            plt.plot(data, linewidth=1.5)
            plt.xlabel('시간 인덱스')
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.ylabel('값')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_seasonal_decomposition(self, data, period=365, title="계절성 분해"):
        """계절성 분해 시각화"""
        from statsmodels.tsa.seasonal import seasonal_decompose
        
        # 계절성 분해
        decomposition = seasonal_decompose(data, model='additive', period=period)
        
        fig, axes = plt.subplots(4, 1, figsize=(15, 12))
        
        # 원본 데이터
        decomposition.observed.plot(ax=axes[0], title='원본 데이터')
        axes[0].grid(True, alpha=0.3)
        
        # 트렌드
        decomposition.trend.plot(ax=axes[1], title='트렌드', color='orange')
        axes[1].grid(True, alpha=0.3)
        
        # 계절성
        decomposition.seasonal.plot(ax=axes[2], title='계절성', color='green')
        axes[2].grid(True, alpha=0.3)
        
        # 잔차
        decomposition.resid.plot(ax=axes[3], title='잔차', color='red')
        axes[3].grid(True, alpha=0.3)
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        return decomposition
    
    def plot_distribution_analysis(self, data, bins=50, title="분포 분석"):
        """데이터 분포 분석"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 히스토그램
        axes[0, 0].hist(data, bins=bins, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('히스토그램')
        axes[0, 0].set_xlabel('값')
        axes[0, 0].set_ylabel('빈도')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 박스플롯
        axes[0, 1].boxplot(data)
        axes[0, 1].set_title('박스플롯')
        axes[0, 1].set_ylabel('값')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Q-Q 플롯
        from scipy import stats
        stats.probplot(data, dist="norm", plot=axes[1, 0])
        axes[1, 0].set_title('Q-Q 플롯 (정규분포)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 밀도 플롯
        axes[1, 1].hist(data, bins=bins, density=True, alpha=0.7, color='lightgreen')
        axes[1, 1].set_title('확률 밀도')
        axes[1, 1].set_xlabel('값')
        axes[1, 1].set_ylabel('밀도')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def plot_correlation_matrix(self, df, title="상관관계 행렬"):
        """상관관계 행렬 히트맵"""
        plt.figure(figsize=(12, 10))
        
        # 숫자형 컬럼만 선택
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numeric_cols].corr()
        
        # 히트맵 생성
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))  # 상삼각 마스크
        sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', center=0,
                   square=True, fmt='.2f', cbar_kws={"shrink": 0.8})
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        return corr_matrix
    
    def plot_feature_importance(self, feature_names, importances, 
                              title="특성 중요도", top_n=20):
        """특성 중요도 시각화"""
        # 중요도 순으로 정렬
        indices = np.argsort(importances)[::-1][:top_n]
        
        plt.figure(figsize=(12, 8))
        plt.bar(range(len(indices)), importances[indices])
        plt.xticks(range(len(indices)), [feature_names[i] for i in indices], rotation=45)
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('특성')
        plt.ylabel('중요도')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def plot_prediction_comparison(self, y_true, y_pred, 
                                 title="예측 결과 비교", sample_size=None):
        """예측 결과 비교 시각화"""
        if sample_size and len(y_true) > sample_size:
            idx = np.random.choice(len(y_true), sample_size, replace=False)
            y_true_sample = y_true[idx]
            y_pred_sample = y_pred[idx]
        else:
            y_true_sample = y_true
            y_pred_sample = y_pred
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # 시계열 비교
        axes[0].plot(y_true_sample, label='실제값', linewidth=2, alpha=0.8)
        axes[0].plot(y_pred_sample, label='예측값', linewidth=1.5, alpha=0.8)
        axes[0].set_title('시계열 비교')
        axes[0].set_xlabel('시간')
        axes[0].set_ylabel('값')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # 산점도
        axes[1].scatter(y_true_sample, y_pred_sample, alpha=0.6)
        axes[1].plot([y_true_sample.min(), y_true_sample.max()], 
                    [y_true_sample.min(), y_true_sample.max()], 
                    'r--', linewidth=2, label='완벽한 예측')
        axes[1].set_title('실제값 vs 예측값')
        axes[1].set_xlabel('실제값')
        axes[1].set_ylabel('예측값')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def plot_residuals_analysis(self, y_true, y_pred, title="잔차 분석"):
        """잔차 분석 시각화"""
        residuals = y_true - y_pred
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 잔차 시계열
        axes[0, 0].plot(residuals, linewidth=1)
        axes[0, 0].axhline(y=0, color='r', linestyle='--', alpha=0.7)
        axes[0, 0].set_title('잔차 시계열')
        axes[0, 0].set_xlabel('시간')
        axes[0, 0].set_ylabel('잔차')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 잔차 히스토그램
        axes[0, 1].hist(residuals, bins=30, alpha=0.7, color='lightcoral')
        axes[0, 1].set_title('잔차 분포')
        axes[0, 1].set_xlabel('잔차')
        axes[0, 1].set_ylabel('빈도')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 잔차 vs 예측값
        axes[1, 0].scatter(y_pred, residuals, alpha=0.6)
        axes[1, 0].axhline(y=0, color='r', linestyle='--', alpha=0.7)
        axes[1, 0].set_title('잔차 vs 예측값')
        axes[1, 0].set_xlabel('예측값')
        axes[1, 0].set_ylabel('잔차')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Q-Q 플롯 (잔차)
        from scipy import stats
        stats.probplot(residuals, dist="norm", plot=axes[1, 1])
        axes[1, 1].set_title('잔차 Q-Q 플롯')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()


def quick_eda_plot(data, target_col, date_col=None):
    """빠른 EDA 시각화"""
    visualizer = TimeSeriesVisualizer()
    
    print("🔍 빠른 EDA 시각화를 시작합니다...")
    
    # 1. 시계열 플롯
    visualizer.plot_time_series(data, date_col, target_col, 
                               title=f"{target_col} 시계열 데이터")
    
    # 2. 분포 분석
    visualizer.plot_distribution_analysis(data[target_col], 
                                        title=f"{target_col} 분포 분석")
    
    # 3. 기본 통계
    print(f"\n📊 {target_col} 기본 통계:")
    print(f"  평균: {data[target_col].mean():,.2f}")
    print(f"  표준편차: {data[target_col].std():,.2f}")
    print(f"  최솟값: {data[target_col].min():,.2f}")
    print(f"  최댓값: {data[target_col].max():,.2f}")
    print(f"  결측값: {data[target_col].isnull().sum()}개")


def plot_model_comparison(models_results, metric='RMSE'):
    """여러 모델 성능 비교 시각화"""
    plt.figure(figsize=(12, 6))
    
    models = list(models_results.keys())
    scores = [models_results[model][metric] for model in models]
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(models)))
    bars = plt.bar(models, scores, color=colors, alpha=0.8, edgecolor='black')
    
    # 막대 위에 값 표시
    for bar, score in zip(bars, scores):
        plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.01,
                f'{score:.2f}', ha='center', va='bottom', fontweight='bold')
    
    plt.title(f'모델별 {metric} 비교', fontsize=16, fontweight='bold')
    plt.xlabel('모델')
    plt.ylabel(metric)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show() 