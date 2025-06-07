#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 3.5: Time-Aware Data Splitting for Competition

한국 전력 수요 예측 대회를 위한 시계열 데이터 분할 및 예측 템플릿 생성
- 훈련 데이터: 2005-2023년 전체 (6,939일)
- 예측 대상: 2024.1.1 ~ 2025.6.10 (527일)
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class CompetitionDataPreparator:
    """대회용 데이터 준비 클래스"""
    
    def __init__(self, input_path, output_dir):
        self.input_path = input_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 대회 설정
        self.prediction_start = datetime(2024, 1, 1)
        self.prediction_end = datetime(2025, 6, 10)
        self.total_prediction_days = 527
        
        # 데이터 로드
        self.train_data = None
        self.cv_folds = []
        
    def load_normalized_data(self):
        """정규화된 훈련 데이터 로드"""
        print("🔄 정규화된 데이터 로드 중...")
        
        self.train_data = pd.read_csv(self.input_path)
        self.train_data['date'] = pd.to_datetime(self.train_data['date'])
        
        print(f"   📊 데이터 형태: {self.train_data.shape}")
        print(f"   📅 기간: {self.train_data['date'].min()} ~ {self.train_data['date'].max()}")
        print(f"   🎯 타겟 범위: {self.train_data['최대전력(MW)'].min():.0f} ~ {self.train_data['최대전력(MW)'].max():.0f} MW")
        print()
        
    def create_prediction_dates(self):
        """527일 예측 날짜 생성"""
        print("🔄 예측 날짜 템플릿 생성 중...")
        
        # 527일 날짜 생성
        prediction_dates = []
        current_date = self.prediction_start
        
        for i in range(self.total_prediction_days):
            # 제출 형식으로 변환 (YYYY.M.D)
            formatted_date = f"{current_date.year}.{current_date.month}.{current_date.day}"
            prediction_dates.append({
                'date': formatted_date,
                'datetime': current_date,
                'iso_date': current_date.strftime('%Y-%m-%d')
            })
            current_date += timedelta(days=1)
        
        # 마지막 날짜 검증
        final_date = prediction_dates[-1]['datetime']
        if final_date != self.prediction_end:
            raise ValueError(f"날짜 계산 오류: 예상 {self.prediction_end}, 실제 {final_date}")
        
        print(f"   📅 예측 기간: {prediction_dates[0]['date']} ~ {prediction_dates[-1]['date']}")
        print(f"   📊 총 예측 일수: {len(prediction_dates)}일")
        print(f"   ✅ 527일 검증: {'통과' if len(prediction_dates) == 527 else '실패'}")
        print()
        
        return prediction_dates
    
    def create_time_features(self, prediction_dates):
        """예측 날짜에 대한 시간 피처 생성"""
        print("🔄 예측 날짜 시간 피처 생성 중...")
        
        features_list = []
        
        for date_info in prediction_dates:
            dt = date_info['datetime']
            
            # 기본 시간 피처
            features = {
                'date': date_info['iso_date'],
                'year': dt.year,
                'month': dt.month,
                'day': dt.day,
                'dayofweek': dt.weekday(),
                'dayofyear': dt.timetuple().tm_yday,
                'weekofyear': dt.isocalendar()[1],
                'quarter': (dt.month - 1) // 3 + 1,
                'season': self._get_season(dt.month)
            }
            
            # 이진 피처
            features.update({
                'is_weekend': 1 if dt.weekday() >= 5 else 0,
                'is_weekday': 1 if dt.weekday() < 5 else 0,
                'is_month_start': 1 if dt.day == 1 else 0,
                'is_month_end': 1 if dt.day == pd.Timestamp(dt).days_in_month else 0
            })
            
            # 주기적 피처
            features.update({
                'month_sin': np.sin(2 * np.pi * dt.month / 12),
                'month_cos': np.cos(2 * np.pi * dt.month / 12),
                'dayofweek_sin': np.sin(2 * np.pi * dt.weekday() / 7),
                'dayofweek_cos': np.cos(2 * np.pi * dt.weekday() / 7)
            })
            
            # 공휴일 피처 (기본값 설정)
            features.update({
                'is_holiday': 0,
                'holiday_type': 'none'
            })
            
            features_list.append(features)
        
        df_features = pd.DataFrame(features_list)
        print(f"   📊 생성된 피처 수: {len(df_features.columns)}개")
        print(f"   📅 피처 데이터 형태: {df_features.shape}")
        print()
        
        return df_features
    
    def _get_season(self, month):
        """계절 정보 반환"""
        if month in [12, 1, 2]:
            return 0  # 겨울
        elif month in [3, 4, 5]:
            return 1  # 봄
        elif month in [6, 7, 8]:
            return 2  # 여름
        else:
            return 3  # 가을
    
    def create_lag_initialization(self):
        """2023년 말 데이터로 2024년 lag 피처 초기화 값 생성"""
        print("🔄 Lag 피처 초기화 값 생성 중...")
        
        # 2023년 말 데이터 추출
        last_30_days = self.train_data.tail(30).copy()
        last_7_days = self.train_data.tail(7).copy()
        last_day = self.train_data.tail(1).copy()
        
        # 초기화 값 계산
        lag_init = {
            'lag_1day': float(last_day['최대전력(MW)'].iloc[0]),
            'lag_7day': float(last_7_days['최대전력(MW)'].iloc[0]),
            'rolling_7day_mean': float(last_7_days['최대전력(MW)'].mean()),
            'rolling_30day_mean': float(last_30_days['최대전력(MW)'].mean()),
            'daily_change': 0.0
        }
        
        print(f"   📊 Lag 초기값:")
        for key, value in lag_init.items():
            print(f"      {key}: {value:.2f}")
        print()
        
        return lag_init
    
    def create_cv_folds(self):
        """시계열 교차검증 폴드 생성"""
        print("🔄 시계열 교차검증 폴드 생성 중...")
        
        # 연도별 폴드 생성 (최근 4년)
        cv_folds = []
        
        for val_year in range(2020, 2024):
            train_end = f"{val_year-1}-12-31"
            val_start = f"{val_year}-01-01"
            val_end = f"{val_year}-12-31"
            
            fold = {
                'fold_id': val_year - 2019,
                'train_period': f"2005-01-01 ~ {train_end}",
                'validation_period': f"{val_start} ~ {val_end}",
                'train_size': len(self.train_data[self.train_data['date'] <= train_end]),
                'val_size': len(self.train_data[
                    (self.train_data['date'] >= val_start) & 
                    (self.train_data['date'] <= val_end)
                ])
            }
            
            cv_folds.append(fold)
            print(f"   📂 Fold {fold['fold_id']}: {fold['train_period']} → {fold['validation_period']}")
            print(f"      훈련: {fold['train_size']}일, 검증: {fold['val_size']}일")
        
        print(f"\n   📊 총 {len(cv_folds)}개 폴드 생성")
        print()
        
        self.cv_folds = cv_folds
        return cv_folds
    
    def save_results(self, prediction_features, submission_template, lag_init):
        """결과 저장"""
        print("🔄 결과 저장 중...")
        
        # 1. 전체 훈련 데이터 저장
        train_path = self.output_dir / 'train_data_full.csv'
        self.train_data.to_csv(train_path, index=False, encoding='utf-8-sig')
        print(f"   💾 훈련 데이터: {train_path}")
        
        # 2. 예측 피처 템플릿 저장
        pred_path = self.output_dir / 'prediction_template.csv'
        prediction_features.to_csv(pred_path, index=False, encoding='utf-8-sig')
        print(f"   💾 예측 템플릿: {pred_path}")
        
        # 3. 제출 파일 템플릿 저장
        sub_path = self.output_dir / 'submission_template.csv'
        submission_template.to_csv(sub_path, index=False, encoding='utf-8-sig')
        print(f"   💾 제출 템플릿: {sub_path}")
        
        # 4. CV 폴드 메타데이터 저장
        cv_metadata = {
            'cv_strategy': 'time_series_split',
            'num_folds': len(self.cv_folds),
            'folds': self.cv_folds
        }
        
        cv_path = self.output_dir / 'cv_folds_metadata.json'
        with open(cv_path, 'w', encoding='utf-8') as f:
            json.dump(cv_metadata, f, indent=2, ensure_ascii=False)
        print(f"   💾 CV 메타데이터: {cv_path}")
        
        # 5. Lag 초기화 값 저장
        lag_path = self.output_dir / 'lag_initialization.json'
        with open(lag_path, 'w', encoding='utf-8') as f:
            json.dump(lag_init, f, indent=2, ensure_ascii=False)
        print(f"   💾 Lag 초기값: {lag_path}")
        
        print()
    
    def run_complete_pipeline(self):
        """전체 파이프라인 실행"""
        print("🚀 Task 3.5: Time-Aware Data Splitting 시작")
        print("=" * 70)
        print()
        
        # 1. 데이터 로드
        self.load_normalized_data()
        
        # 2. 예측 날짜 생성
        prediction_dates = self.create_prediction_dates()
        
        # 3. 시간 피처 생성
        prediction_features = self.create_time_features(prediction_dates)
        
        # 4. Lag 초기화 값 생성
        lag_init = self.create_lag_initialization()
        
        # 5. CV 폴드 생성
        self.create_cv_folds()
        
        # 6. 제출 템플릿 생성
        submission_data = []
        for date_info in prediction_dates:
            submission_data.append({
                'date': date_info['date'],
                '최대전력(MW)': 0
            })
        submission_template = pd.DataFrame(submission_data)
        
        # 7. 결과 저장
        self.save_results(prediction_features, submission_template, lag_init)
        
        print("🎉 Task 3.5: Time-Aware Data Splitting 완료!")
        print("=" * 70)
        print()
        print("📋 생성된 파일:")
        for file_path in sorted(self.output_dir.glob('*')):
            print(f"   📄 {file_path.name}")
        print()
        print("✅ 다음 단계: Task 4 (Model Development) 준비 완료")


def main():
    """메인 실행 함수"""
    # 입력/출력 경로 설정
    input_path = 'results/preprocessing/04_normalization/electricity_data_normalized.csv'
    output_dir = 'results/preprocessing/05_data_splitting'
    
    # 데이터 준비 실행
    preparator = CompetitionDataPreparator(input_path, output_dir)
    preparator.run_complete_pipeline()


if __name__ == "__main__":
    main() 