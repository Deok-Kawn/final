import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def create_core_derived_features(df, target_col='최대전력(MW)', date_col='date'):
    """
    핵심 5개 파생 변수 생성
    
    Parameters:
    - df: 시간 피처가 포함된 DataFrame
    - target_col: 전력 수요 컬럼명
    - date_col: 날짜 컬럼명
    
    Returns:
    - DataFrame: 핵심 파생 변수가 추가된 데이터프레임
    """
    print("=== 핵심 파생 변수 생성 시작 ===")
    print(f"입력 데이터: {df.shape}")
    
    # 데이터 복사 및 날짜 정렬
    df_derived = df.copy()
    df_derived[date_col] = pd.to_datetime(df_derived[date_col])
    df_derived = df_derived.sort_values(date_col).reset_index(drop=True)
    
    print("📊 핵심 5개 파생 변수 생성 중...")
    
    # 1. lag_1day: 어제 수요 (가장 직접적인 예측 신호)
    print("1. lag_1day - 어제 전력 수요")
    df_derived['lag_1day'] = df_derived[target_col].shift(1)
    
    # 2. lag_7day: 지난주 같은 요일 (주간 패턴)
    print("2. lag_7day - 지난주 같은 요일 수요")
    df_derived['lag_7day'] = df_derived[target_col].shift(7)
    
    # 3. rolling_7day_mean: 최근 1주 평균 (단기 트렌드)
    print("3. rolling_7day_mean - 최근 1주 평균")
    df_derived['rolling_7day_mean'] = df_derived[target_col].rolling(
        window=7, min_periods=1
    ).mean().shift(1)  # 미래 정보 누출 방지
    
    # 4. rolling_30day_mean: 최근 1달 평균 (중기 기준선)
    print("4. rolling_30day_mean - 최근 1달 평균")
    df_derived['rolling_30day_mean'] = df_derived[target_col].rolling(
        window=30, min_periods=1
    ).mean().shift(1)  # 미래 정보 누출 방지
    
    # 5. daily_change: 일간 변화량 (트렌드 방향)
    print("5. daily_change - 전일 대비 변화량")
    df_derived['daily_change'] = df_derived[target_col] - df_derived[target_col].shift(1)
    
    # 결측값 현황 확인
    print("\n📈 파생 변수 생성 결과:")
    derived_features = ['lag_1day', 'lag_7day', 'rolling_7day_mean', 'rolling_30day_mean', 'daily_change']
    
    for feature in derived_features:
        missing_count = df_derived[feature].isnull().sum()
        missing_pct = (missing_count / len(df_derived)) * 100
        print(f"  {feature}: {missing_count}개 결측값 ({missing_pct:.1f}%)")
    
    print(f"\n✅ 완료: {df_derived.shape[0]}행 × {df_derived.shape[1]}열 (파생 변수 5개 추가)")
    
    return df_derived

def analyze_derived_features(df, target_col='최대전력(MW)'):
    """
    생성된 파생 변수들의 특성 분석
    """
    print("\n=== 파생 변수 상관관계 분석 ===")
    
    derived_features = ['lag_1day', 'lag_7day', 'rolling_7day_mean', 'rolling_30day_mean', 'daily_change']
    
    correlations = []
    for feature in derived_features:
        # 결측값 제외하고 상관관계 계산
        corr = df[target_col].corr(df[feature])
        correlations.append((feature, corr))
        print(f"{feature}: {corr:.4f}")
    
    # 상관관계 순으로 정렬
    correlations.sort(key=lambda x: abs(x[1]), reverse=True)
    
    print(f"\n🏆 중요도 순위:")
    for i, (feature, corr) in enumerate(correlations, 1):
        print(f"{i}. {feature}: {corr:.4f}")
    
    return correlations

def save_derived_features_summary(df, output_path):
    """
    파생 변수 요약 정보 저장
    """
    derived_features = ['lag_1day', 'lag_7day', 'rolling_7day_mean', 'rolling_30day_mean', 'daily_change']
    
    summary = []
    summary.append("=== 핵심 파생 변수 생성 결과 ===\n")
    summary.append(f"데이터 크기: {df.shape[0]}행 × {df.shape[1]}열")
    summary.append(f"생성된 파생 변수: {len(derived_features)}개\n")
    
    summary.append("파생 변수 상세 정보:")
    for feature in derived_features:
        missing_count = df[feature].isnull().sum()
        missing_pct = (missing_count / len(df)) * 100
        mean_val = df[feature].mean() if missing_count < len(df) else np.nan
        std_val = df[feature].std() if missing_count < len(df) else np.nan
        
        summary.append(f"\n{feature}:")
        summary.append(f"  - 결측값: {missing_count}개 ({missing_pct:.1f}%)")
        if not np.isnan(mean_val):
            summary.append(f"  - 평균: {mean_val:.2f}")
            summary.append(f"  - 표준편차: {std_val:.2f}")
    
    # 파일 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary))
    
    print(f"\n📋 요약 보고서 저장: {output_path}")

if __name__ == "__main__":
    # 1. 데이터 로드
    print("데이터 로딩 중...")
    input_file = "results/preprocessing/02_feature_engineering/electricity_data_with_temporal_features.csv"
    df = pd.read_csv(input_file)
    
    # 2. 핵심 파생 변수 생성
    df_with_derived = create_core_derived_features(df)
    
    # 3. 파생 변수 분석
    correlations = analyze_derived_features(df_with_derived)
    
    # 4. 결과 저장
    output_dir = "results/preprocessing/03_derived_variables"
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # 데이터 저장
    output_file = f"{output_dir}/electricity_data_with_core_derived.csv"
    df_with_derived.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n💾 결과 데이터 저장: {output_file}")
    
    # 요약 보고서 저장
    summary_file = f"{output_dir}/core_derived_features_summary.txt"
    save_derived_features_summary(df_with_derived, summary_file)
    
    print(f"\n🎉 핵심 파생 변수 생성 완료!")
    print(f"   - 원본: {df.shape[1]}개 컬럼")
    print(f"   - 최종: {df_with_derived.shape[1]}개 컬럼 (5개 추가)") 