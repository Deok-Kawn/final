#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 3.4: Feature Normalization and Scaling

한국 전력 수요 시계열 데이터의 피처들을 정규화 및 스케일링합니다.
시계열 특성을 보존하면서 모델 학습에 최적화된 형태로 변환합니다.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, PowerTransformer
import joblib
import warnings
import json
import os
from datetime import datetime

# 한글 폰트 설정
plt.rcParams['font.family'] = ['Malgun Gothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
warnings.filterwarnings('ignore')

def analyze_feature_types(df):
    """피처 타입을 분석하고 분류합니다."""
    
    feature_types = {
        'target': [],
        'datetime': [],
        'categorical': [],
        'binary': [],
        'numerical': [],
        'cyclical': [],
        'skip': []  # 이미 정규화된 피처들
    }
    
    for col in df.columns:
        if col == 'power_consumption':
            feature_types['target'].append(col)
        elif col == 'date':
            feature_types['datetime'].append(col)
        elif col.endswith('_name') or col == 'holiday_type':
            feature_types['categorical'].append(col)
        elif col.startswith('is_') or col in ['weekday_name', 'month_name']:
            feature_types['binary'].append(col)
        elif col.endswith('_sin') or col.endswith('_cos'):
            feature_types['cyclical'].append(col)
        elif col in ['year', 'month', 'quarter', 'dayofweek', 'dayofyear', 'weekofyear', 'season']:
            feature_types['numerical'].append(col)
        elif col.startswith('lag_') or col.startswith('rolling_') or col == 'daily_change':
            feature_types['numerical'].append(col)
        else:
            feature_types['skip'].append(col)
    
    return feature_types

def get_optimal_scaler(data, feature_name):
    """피처의 분포 특성을 분석하여 최적 스케일러를 선택합니다."""
    
    # 결측값 제거하고 분석
    clean_data = data.dropna()
    
    if len(clean_data) == 0:
        return None, "No valid data"
    
    # 기본 통계량
    skewness = abs(clean_data.skew())
    
    # IQR을 이용한 이상치 비율 계산
    Q1 = clean_data.quantile(0.25)
    Q3 = clean_data.quantile(0.75)
    IQR = Q3 - Q1
    outliers = ((clean_data < (Q1 - 1.5 * IQR)) | (clean_data > (Q3 + 1.5 * IQR))).sum()
    outlier_ratio = outliers / len(clean_data)
    
    # 분포의 범위
    data_range = clean_data.max() - clean_data.min()
    
    # 스케일러 선택 로직
    if outlier_ratio > 0.1:  # 이상치가 10% 이상
        return RobustScaler(), f"RobustScaler (outlier_ratio: {outlier_ratio:.3f})"
    elif skewness > 2:  # 매우 치우친 분포
        return PowerTransformer(method='yeo-johnson'), f"PowerTransformer (skewness: {skewness:.3f})"
    elif data_range < 100 and clean_data.min() >= 0:  # 작은 범위의 양수 데이터
        return MinMaxScaler(), f"MinMaxScaler (range: {data_range:.1f})"
    else:  # 일반적인 경우
        return StandardScaler(), f"StandardScaler (default)"

def normalize_features(df, feature_types):
    """피처들을 정규화합니다."""
    
    df_normalized = df.copy()
    scalers = {}
    scaling_info = {}
    
    # 정규화할 피처들 (numerical 피처만)
    features_to_scale = feature_types['numerical']
    
    print(f"정규화 대상 피처 수: {len(features_to_scale)}")
    
    for feature in features_to_scale:
        print(f"\n처리 중: {feature}")
        
        # 결측값 임시 처리 (중위수로 채움)
        original_na_mask = df_normalized[feature].isna()
        if original_na_mask.any():
            median_val = df_normalized[feature].median()
            df_normalized[feature].fillna(median_val, inplace=True)
            print(f"  - 결측값 {original_na_mask.sum()}개를 중위수 {median_val:.2f}로 임시 처리")
        
        # 최적 스케일러 선택
        scaler, reason = get_optimal_scaler(df_normalized[feature], feature)
        
        if scaler is None:
            print(f"  - 스킵 (유효 데이터 없음)")
            continue
        
        # 스케일링 적용
        try:
            # 2D 배열로 변환
            feature_values = df_normalized[feature].values.reshape(-1, 1)
            scaled_values = scaler.fit_transform(feature_values)
            df_normalized[feature] = scaled_values.flatten()
            
            # 스케일러 및 정보 저장
            scalers[feature] = scaler
            scaling_info[feature] = {
                'scaler_type': type(scaler).__name__,
                'reason': reason,
                'original_mean': float(df[feature].mean()) if not df[feature].isna().all() else None,
                'original_std': float(df[feature].std()) if not df[feature].isna().all() else None,
                'scaled_mean': float(df_normalized[feature].mean()),
                'scaled_std': float(df_normalized[feature].std())
            }
            
            print(f"  - 적용: {reason}")
            print(f"  - 변환 전: 평균 {df[feature].mean():.3f}, 표준편차 {df[feature].std():.3f}")
            print(f"  - 변환 후: 평균 {df_normalized[feature].mean():.3f}, 표준편차 {df_normalized[feature].std():.3f}")
            
        except Exception as e:
            print(f"  - 오류 발생: {e}")
            continue
        
        # 원본 결측값 패턴 복원
        if original_na_mask.any():
            df_normalized.loc[original_na_mask, feature] = np.nan
            print(f"  - 원본 결측값 패턴 복원 완료")
    
    return df_normalized, scalers, scaling_info

def validate_scaling_quality(df_original, df_scaled, feature_types):
    """스케일링 품질을 검증합니다."""
    
    validation_results = {}
    
    numerical_features = feature_types['numerical']
    
    for feature in numerical_features:
        if feature not in df_scaled.columns:
            continue
        
        # 결측값 제외하고 비교
        original_clean = df_original[feature].dropna()
        scaled_clean = df_scaled[feature].dropna()
        
        if len(original_clean) == 0 or len(scaled_clean) == 0:
            continue
        
        # 검증 기준들
        criteria = {}
        
        # 1. 스케일링된 피처의 평균이 0 근처인지 (StandardScaler의 경우)
        criteria['mean_near_zero'] = abs(scaled_clean.mean()) < 0.1
        
        # 2. 스케일링된 피처의 표준편차가 1 근처인지 (StandardScaler의 경우)
        criteria['std_near_one'] = 0.8 < scaled_clean.std() < 1.2
        
        # 3. 결측값 패턴이 보존되었는지
        original_na_pattern = df_original[feature].isna()
        scaled_na_pattern = df_scaled[feature].isna()
        criteria['na_pattern_preserved'] = original_na_pattern.equals(scaled_na_pattern)
        
        # 4. 상대적 순서가 보존되었는지 (상관관계 확인)
        if len(original_clean) > 1 and len(scaled_clean) > 1:
            correlation = original_clean.corr(scaled_clean)
            criteria['order_preserved'] = correlation > 0.95
        else:
            criteria['order_preserved'] = True
        
        # 5. 이상치가 과도하게 증가하지 않았는지
        original_outliers = ((original_clean - original_clean.mean()).abs() > 3 * original_clean.std()).sum()
        scaled_outliers = ((scaled_clean - scaled_clean.mean()).abs() > 3 * scaled_clean.std()).sum()
        criteria['outliers_controlled'] = scaled_outliers <= original_outliers * 1.5
        
        # 전체 품질 점수
        quality_score = sum(criteria.values()) / len(criteria)
        
        validation_results[feature] = {
            'criteria': criteria,
            'quality_score': quality_score,
            'passed': quality_score >= 0.8  # 80% 이상 기준 통과
        }
    
    return validation_results

def create_scaling_visualizations(df_original, df_scaled, feature_types, output_dir):
    """스케일링 효과를 시각화합니다."""
    
    numerical_features = feature_types['numerical'][:9]  # 처음 9개만 시각화
    
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    axes = axes.flatten()
    
    for i, feature in enumerate(numerical_features):
        if i >= 9:
            break
        
        ax = axes[i]
        
        # 결측값 제외
        original_clean = df_original[feature].dropna()
        scaled_clean = df_scaled[feature].dropna()
        
        if len(original_clean) == 0:
            ax.text(0.5, 0.5, 'No valid data', ha='center', va='center', transform=ax.transAxes)
            ax.set_title(feature)
            continue
        
        # 분포 비교
        ax.hist(original_clean, bins=30, alpha=0.5, label='Original', density=True)
        ax.hist(scaled_clean, bins=30, alpha=0.5, label='Scaled', density=True)
        
        ax.set_title(f'{feature}\nOrig: μ={original_clean.mean():.2f}, σ={original_clean.std():.2f}\n'
                    f'Scaled: μ={scaled_clean.mean():.2f}, σ={scaled_clean.std():.2f}')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # 남은 subplot 제거
    for i in range(len(numerical_features), 9):
        fig.delaxes(axes[i])
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'scaling_effects_comparison.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def generate_comprehensive_report(df_original, df_scaled, feature_types, scaling_info, 
                                validation_results, output_dir):
    """종합 분석 보고서를 생성합니다."""
    
    report = []
    report.append("# Task 3.4: Feature Normalization and Scaling 결과 보고서\n")
    report.append(f"생성 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 전체 요약
    total_features = len(df_original.columns)
    numerical_features = len(feature_types['numerical'])
    scaled_features = len([f for f in feature_types['numerical'] if f in scaling_info])
    
    report.append("## 📊 전체 요약\n")
    report.append(f"- **전체 피처 수**: {total_features}개")
    report.append(f"- **수치형 피처 수**: {numerical_features}개")
    report.append(f"- **스케일링 적용**: {scaled_features}개 ({scaled_features/numerical_features*100:.1f}%)")
    report.append(f"- **데이터 행 수**: {len(df_scaled):,}행\n")
    
    # 피처 타입별 분류
    report.append("## 🏷️ 피처 타입별 분류\n")
    for type_name, features in feature_types.items():
        if features:
            report.append(f"### {type_name.title()} 피처 ({len(features)}개)")
            for feature in features:
                report.append(f"- `{feature}`")
            report.append("")
    
    # 스케일링 결과
    report.append("## ⚙️ 스케일링 적용 결과\n")
    for feature, info in scaling_info.items():
        report.append(f"### {feature}")
        report.append(f"- **스케일러**: {info['scaler_type']}")
        report.append(f"- **선택 이유**: {info['reason']}")
        if info['original_mean'] is not None:
            report.append(f"- **변환 전**: 평균 {info['original_mean']:.3f}, 표준편차 {info['original_std']:.3f}")
        report.append(f"- **변환 후**: 평균 {info['scaled_mean']:.3f}, 표준편차 {info['scaled_std']:.3f}")
        report.append("")
    
    # 품질 검증 결과
    report.append("## ✅ 품질 검증 결과\n")
    passed_count = sum(1 for result in validation_results.values() if result['passed'])
    total_validated = len(validation_results)
    
    report.append(f"**검증 통과율**: {passed_count}/{total_validated} ({passed_count/total_validated*100:.1f}%)\n")
    
    for feature, result in validation_results.items():
        status = "✅ 통과" if result['passed'] else "❌ 실패"
        report.append(f"### {feature} - {status} (점수: {result['quality_score']:.2f})")
        
        for criterion, passed in result['criteria'].items():
            symbol = "✓" if passed else "✗"
            report.append(f"- {symbol} {criterion}")
        report.append("")
    
    # 시계열 특성 보존 확인
    report.append("## 🕐 시계열 특성 보존 확인\n")
    
    # 타겟 변수와의 상관관계 비교
    target_corr_original = {}
    target_corr_scaled = {}
    
    for feature in feature_types['numerical']:
        if feature in df_original.columns and feature in df_scaled.columns:
            orig_corr = df_original['power_consumption'].corr(df_original[feature])
            scaled_corr = df_scaled['power_consumption'].corr(df_scaled[feature])
            
            if not pd.isna(orig_corr) and not pd.isna(scaled_corr):
                target_corr_original[feature] = orig_corr
                target_corr_scaled[feature] = scaled_corr
    
    report.append("### 타겟 변수와의 상관관계 보존도")
    report.append("| 피처명 | 원본 상관관계 | 스케일링 후 | 차이 | 보존도 |")
    report.append("|--------|-------------|------------|------|--------|")
    
    correlation_changes = []
    for feature in target_corr_original:
        orig = target_corr_original[feature]
        scaled = target_corr_scaled[feature]
        diff = abs(orig - scaled)
        preservation = "우수" if diff < 0.01 else "양호" if diff < 0.05 else "주의"
        
        report.append(f"| {feature} | {orig:.3f} | {scaled:.3f} | {diff:.3f} | {preservation} |")
        correlation_changes.append(diff)
    
    if correlation_changes:
        avg_change = np.mean(correlation_changes)
        report.append(f"\n**평균 상관관계 변화**: {avg_change:.4f} (낮을수록 좋음)")
    
    # 다음 단계 안내
    report.append("\n## 🚀 다음 단계: Task 3.5\n")
    report.append("**Time-Aware Data Splitting**을 위한 완전한 정규화 데이터셋이 준비되었습니다.")
    report.append("\n### 활용 가능한 파일들")
    report.append("- `electricity_data_normalized.csv`: 정규화된 전체 데이터셋")
    report.append("- `scalers.joblib`: 저장된 스케일러 객체들 (미래 데이터 적용용)")
    report.append("- `scaling_metadata.json`: 상세 스케일링 정보")
    
    # 보고서 저장
    with open(os.path.join(output_dir, 'feature_normalization_report.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    return report

def main():
    """메인 실행 함수"""
    
    # 입력 데이터 로드
    input_path = 'results/preprocessing/03_derived_variables/electricity_data_with_core_derived.csv'
    df = pd.read_csv(input_path)
    
    print("=" * 80)
    print("Task 3.4: Feature Normalization and Scaling")
    print("=" * 80)
    print(f"입력 데이터: {df.shape[0]:,}행 × {df.shape[1]}열")
    print(f"날짜 범위: {df['date'].min()} ~ {df['date'].max()}")
    
    # 출력 디렉토리 생성
    output_dir = 'results/preprocessing/04_normalization'
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. 피처 타입 분석
    print("\n1단계: 피처 타입 분석")
    feature_types = analyze_feature_types(df)
    
    for type_name, features in feature_types.items():
        if features:
            print(f"  {type_name}: {len(features)}개")
    
    # 2. 피처 정규화
    print("\n2단계: 피처 정규화 수행")
    df_normalized, scalers, scaling_info = normalize_features(df, feature_types)
    
    # 3. 품질 검증
    print("\n3단계: 스케일링 품질 검증")
    validation_results = validate_scaling_quality(df, df_normalized, feature_types)
    
    passed_count = sum(1 for result in validation_results.values() if result['passed'])
    total_count = len(validation_results)
    print(f"품질 검증 통과: {passed_count}/{total_count} ({passed_count/total_count*100:.1f}%)")
    
    # 4. 시각화
    print("\n4단계: 스케일링 효과 시각화")
    create_scaling_visualizations(df, df_normalized, feature_types, output_dir)
    
    # 5. 결과 저장
    print("\n5단계: 결과 저장")
    
    # 정규화된 데이터셋 저장
    normalized_output_path = os.path.join(output_dir, 'electricity_data_normalized.csv')
    df_normalized.to_csv(normalized_output_path, index=False, encoding='utf-8')
    print(f"정규화 데이터셋 저장: {normalized_output_path}")
    
    # 스케일러 객체들 저장
    scalers_path = os.path.join(output_dir, 'scalers.joblib')
    joblib.dump(scalers, scalers_path)
    print(f"스케일러 객체들 저장: {scalers_path}")
    
    # 메타데이터 저장 (JSON 직렬화 가능하도록 변환)
    metadata = {
        'feature_types': feature_types,
        'scaling_info': scaling_info,
        'validation_results': {k: {
            'quality_score': float(v['quality_score']),
            'passed': bool(v['passed']),
            'criteria': {kk: bool(vv) for kk, vv in v['criteria'].items()}
        } for k, v in validation_results.items()},
        'processing_datetime': datetime.now().isoformat(),
        'input_shape': list(df.shape),
        'output_shape': list(df_normalized.shape)
    }
    
    metadata_path = os.path.join(output_dir, 'scaling_metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"메타데이터 저장: {metadata_path}")
    
    # 6. 종합 보고서 생성
    print("\n6단계: 종합 보고서 생성")
    report = generate_comprehensive_report(df, df_normalized, feature_types, scaling_info, 
                                         validation_results, output_dir)
    
    # 최종 요약
    print("\n" + "=" * 80)
    print("🎉 Task 3.4 완료!")
    print("=" * 80)
    print(f"✅ 정규화된 데이터셋: {df_normalized.shape[0]:,}행 × {df_normalized.shape[1]}열")
    print(f"✅ 스케일링 적용 피처: {len(scaling_info)}개")
    print(f"✅ 품질 검증 통과: {passed_count}/{total_count}개")
    print(f"✅ 결과 저장 위치: {output_dir}")
    
    return df_normalized, scalers, validation_results

if __name__ == "__main__":
    main() 