"""
시계열 특성 엔지니어링
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class TimeSeriesFeatureEngine:
    """시계열 데이터의 특성 엔지니어링을 담당하는 클래스"""
    
    def __init__(self):
        pass
    
    def add_time_features(self, df, date_col='date'):
        """날짜 기반 특성 추가"""
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        
        # 기본 시간 특성
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        df['day'] = df[date_col].dt.day
        df['dayofweek'] = df[date_col].dt.dayofweek  # 0=월요일
        df['dayofyear'] = df[date_col].dt.dayofyear
        df['quarter'] = df[date_col].dt.quarter
        
        # 주말/평일
        df['is_weekend'] = (df['dayofweek'] >= 5).astype(int)
        
        # 계절 정보 (기상학적 계절)
        df['season'] = df['month'].map({
            12: 'winter', 1: 'winter', 2: 'winter',
            3: 'spring', 4: 'spring', 5: 'spring',
            6: 'summer', 7: 'summer', 8: 'summer',
            9: 'autumn', 10: 'autumn', 11: 'autumn'
        })
        
        # 순환 특성 (사인, 코사인)
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        df['day_sin'] = np.sin(2 * np.pi * df['dayofweek'] / 7)
        df['day_cos'] = np.cos(2 * np.pi * df['dayofweek'] / 7)
        
        return df
    
    def add_lag_features(self, df, target_col, lags=[1, 7, 14, 30, 365]):
        """래그 특성 추가"""
        df = df.copy()
        
        for lag in lags:
            df[f'{target_col}_lag_{lag}'] = df[target_col].shift(lag)
        
        return df
    
    def add_rolling_features(self, df, target_col, windows=[7, 14, 30, 90]):
        """롤링 통계 특성 추가"""
        df = df.copy()
        
        for window in windows:
            # 평균, 표준편차, 최대, 최소
            df[f'{target_col}_rolling_mean_{window}'] = df[target_col].rolling(window).mean()
            df[f'{target_col}_rolling_std_{window}'] = df[target_col].rolling(window).std()
            df[f'{target_col}_rolling_max_{window}'] = df[target_col].rolling(window).max()
            df[f'{target_col}_rolling_min_{window}'] = df[target_col].rolling(window).min()
            
            # 트렌드 (현재값 - 평균)
            df[f'{target_col}_trend_{window}'] = df[target_col] - df[f'{target_col}_rolling_mean_{window}']
        
        return df
    
    def add_diff_features(self, df, target_col, periods=[1, 7, 365]):
        """차분 특성 추가"""
        df = df.copy()
        
        for period in periods:
            df[f'{target_col}_diff_{period}'] = df[target_col].diff(period)
            df[f'{target_col}_pct_change_{period}'] = df[target_col].pct_change(period)
        
        return df
    
    def create_all_features(self, df, target_col, date_col='date'):
        """모든 특성을 한 번에 생성"""
        print("특성 엔지니어링 시작...")
        
        # 날짜 특성
        df = self.add_time_features(df, date_col)
        print("✓ 시간 특성 추가 완료")
        
        # 래그 특성
        df = self.add_lag_features(df, target_col)
        print("✓ 래그 특성 추가 완료")
        
        # 롤링 특성
        df = self.add_rolling_features(df, target_col)
        print("✓ 롤링 특성 추가 완료")
        
        # 차분 특성
        df = self.add_diff_features(df, target_col)
        print("✓ 차분 특성 추가 완료")
        
        print(f"특성 엔지니어링 완료: {df.shape[1]}개 특성")
        return df


def create_holiday_features(df, date_col='date'):
    """한국 공휴일 특성 추가 (간단 버전)"""
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    
    # 간단한 공휴일 (실제로는 holidays 라이브러리 사용 권장)
    holidays = [
        '01-01',  # 신정
        '02-12', '02-13', '02-14',  # 설날 (매년 다름, 예시)
        '03-01',  # 삼일절
        '05-05',  # 어린이날
        '06-06',  # 현충일
        '08-15',  # 광복절
        '10-03', '10-09',  # 추석 (매년 다름, 예시)
        '10-09',  # 한글날
        '12-25',  # 크리스마스
    ]
    
    df['is_holiday'] = df[date_col].dt.strftime('%m-%d').isin(holidays).astype(int)
    
    return df 