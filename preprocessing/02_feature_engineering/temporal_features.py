import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def create_temporal_features(df, date_col='date'):
    """
    시간적 특성 공학 - 핵심 피처만 생성
    """
    print("시간적 특성 공학 시작...")
    
    # 데이터 복사
    df_features = df.copy()
    
    # 1. 날짜 변환
    print("1. 날짜 형식 변환 중...")
    if df_features[date_col].dtype == 'object':
        df_features[date_col] = pd.to_datetime(df_features[date_col])
    
    # 2. 기본 시간 피처 생성
    print("2. 기본 시간 피처 생성 중...")
    df_features['year'] = df_features[date_col].dt.year
    df_features['month'] = df_features[date_col].dt.month
    df_features['day'] = df_features[date_col].dt.day
    df_features['dayofweek'] = df_features[date_col].dt.dayofweek  # 0=Monday
    df_features['dayofyear'] = df_features[date_col].dt.dayofyear
    df_features['weekofyear'] = df_features[date_col].dt.isocalendar().week
    df_features['quarter'] = df_features[date_col].dt.quarter
    
    # 3. 계절 정의 (한국 기준)
    print("3. 계절 피처 생성 중...")
    def get_season(month):
        if month in [3, 4, 5]:
            return 1  # 봄
        elif month in [6, 7, 8]:
            return 2  # 여름
        elif month in [9, 10, 11]:
            return 3  # 가을
        else:
            return 4  # 겨울
    
    df_features['season'] = df_features['month'].apply(get_season)
    
    # 4. 이진 피처
    print("4. 이진 피처 생성 중...")
    df_features['is_weekend'] = (df_features['dayofweek'] >= 5).astype(int)
    df_features['is_weekday'] = (df_features['dayofweek'] < 5).astype(int)
    df_features['is_month_start'] = df_features[date_col].dt.is_month_start.astype(int)
    df_features['is_month_end'] = df_features[date_col].dt.is_month_end.astype(int)
    
    # 5. 주기적 피처 (순환 인코딩)
    print("5. 주기적 피처 생성 중...")
    df_features['month_sin'] = np.sin(2 * np.pi * df_features['month'] / 12)
    df_features['month_cos'] = np.cos(2 * np.pi * df_features['month'] / 12)
    df_features['dayofweek_sin'] = np.sin(2 * np.pi * df_features['dayofweek'] / 7)
    df_features['dayofweek_cos'] = np.cos(2 * np.pi * df_features['dayofweek'] / 7)
    
    print(f"시간적 특성 공학 완료. 총 {len(df_features.columns)}개 피처 생성.")
    return df_features

def create_korean_holidays():
    """
    한국 공휴일 데이터베이스 생성 (핵심만)
    """
    holidays = []
    
    # 고정 공휴일
    fixed_holidays = [
        ('01-01', '신정'),
        ('03-01', '삼일절'),
        ('05-05', '어린이날'),
        ('06-06', '현충일'),
        ('08-15', '광복절'),
        ('10-03', '개천절'),
        ('10-09', '한글날'),
        ('12-25', '크리스마스')
    ]
    
    # 2005-2023년 고정 공휴일
    for year in range(2005, 2024):
        for date_str, name in fixed_holidays:
            holidays.append({
                'date': f"{year}-{date_str}",
                'name': name,
                'type': 'fixed'
            })
    
    # 주요 음력 공휴일 (대표적인 날짜들만)
    lunar_holidays = [
        # 설날 (음력 1.1 기준 대략적 양력 날짜)
        ('2005-02-07', '설날'), ('2005-02-08', '설날'), ('2005-02-09', '설날'),
        ('2006-01-28', '설날'), ('2006-01-29', '설날'), ('2006-01-30', '설날'),
        ('2007-02-17', '설날'), ('2007-02-18', '설날'), ('2007-02-19', '설날'),
        ('2008-02-06', '설날'), ('2008-02-07', '설날'), ('2008-02-08', '설날'),
        ('2009-01-25', '설날'), ('2009-01-26', '설날'), ('2009-01-27', '설날'),
        ('2010-02-13', '설날'), ('2010-02-14', '설날'), ('2010-02-15', '설날'),
        # 추석 (음력 8.15 기준 대략적 양력 날짜)
        ('2005-09-17', '추석'), ('2005-09-18', '추석'), ('2005-09-19', '추석'),
        ('2006-10-05', '추석'), ('2006-10-06', '추석'), ('2006-10-07', '추석'),
        ('2007-09-24', '추석'), ('2007-09-25', '추석'), ('2007-09-26', '추석'),
        ('2008-09-13', '추석'), ('2008-09-14', '추석'), ('2008-09-15', '추석'),
        ('2009-10-02', '추석'), ('2009-10-03', '추석'), ('2009-10-04', '추석'),
        ('2010-09-21', '추석'), ('2010-09-22', '추석'), ('2010-09-23', '추석'),
    ]
    
    for date_str, name in lunar_holidays:
        holidays.append({
            'date': date_str,
            'name': name,
            'type': 'lunar'
        })
    
    return pd.DataFrame(holidays)

def add_holiday_features(df, date_col='date'):
    """
    공휴일 피처 추가
    """
    print("공휴일 피처 생성 중...")
    
    # 공휴일 데이터베이스 생성
    holidays_df = create_korean_holidays()
    holidays_df['date'] = pd.to_datetime(holidays_df['date'])
    
    # 데이터 복사
    df_holiday = df.copy()
    if df_holiday[date_col].dtype == 'object':
        df_holiday[date_col] = pd.to_datetime(df_holiday[date_col])
    
    # 공휴일 여부 확인
    holiday_dates = set(holidays_df['date'].dt.date)
    df_holiday['is_holiday'] = df_holiday[date_col].dt.date.isin(holiday_dates).astype(int)
    
    # 공휴일 타입
    holiday_type_map = dict(zip(holidays_df['date'].dt.date, holidays_df['type']))
    df_holiday['holiday_type'] = df_holiday[date_col].dt.date.map(holiday_type_map).fillna('none')
    
    print(f"총 {df_holiday['is_holiday'].sum()}개 공휴일 확인됨.")
    return df_holiday, holidays_df

def main():
    """
    메인 실행 함수
    """
    print("=== Task 3.2: Temporal Feature Engineering ===")
    
    # 1. 데이터 로드
    print("\n1. 데이터 로드 중...")
    df = pd.read_csv('results/preprocessing/01_missing_value_imputation/final_imputed_dataset.csv')
    print(f"원본 데이터: {df.shape}")
    
    # 2. 시간적 특성 생성
    print("\n2. 시간적 특성 생성...")
    df_temporal = create_temporal_features(df)
    
    # 3. 공휴일 특성 추가
    print("\n3. 공휴일 특성 추가...")
    df_final, holidays_df = add_holiday_features(df_temporal)
    
    # 4. 결과 저장
    print("\n4. 결과 저장...")
    
    # 피처 엔지니어링 결과 저장
    output_path = 'results/preprocessing/02_feature_engineering/electricity_data_with_temporal_features.csv'
    df_final.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"시간 피처 데이터: {output_path}")
    
    # 공휴일 데이터베이스 저장
    holidays_path = 'results/preprocessing/02_feature_engineering/korean_holidays_database.csv'
    holidays_df.to_csv(holidays_path, index=False, encoding='utf-8-sig')
    print(f"공휴일 데이터베이스: {holidays_path}")
    
    # 5. 요약 정보
    print("\n=== 최종 결과 ===")
    print(f"최종 데이터 크기: {df_final.shape}")
    print(f"생성된 피처 수: {len(df_final.columns) - 2}")  # date, 최대전력 제외
    print(f"공휴일 데이터: {len(holidays_df)}개")
    
    # 생성된 피처 목록
    feature_cols = [col for col in df_final.columns if col not in ['date', '최대전력(MW)']]
    print(f"\n생성된 피처들:")
    for i, col in enumerate(feature_cols, 1):
        print(f"  {i:2d}. {col}")
    
    print("\nTask 3.2 완료!")
    return df_final, holidays_df

if __name__ == "__main__":
    df_final, holidays_df = main() 