"""
데이터 로딩 유틸리티
"""
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class DataLoader:
    """시계열 데이터 로딩 및 기본 전처리를 담당하는 클래스"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.train_data = None
        self.submission_format = None
    
    def load_train_data(self, filename="일별최대전력수급(2005-2023).csv"):
        """학습 데이터 로딩"""
        file_path = self.data_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"데이터 파일을 찾을 수 없습니다: {file_path}")
        
        # CSV 파일 로딩 (인코딩 자동 감지)
        try:
            self.train_data = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            self.train_data = pd.read_csv(file_path, encoding='cp949')
        
        print(f"데이터 로딩 완료: {self.train_data.shape}")
        return self.train_data
    
    def load_submission_format(self, filename="submission_sample.csv"):
        """제출 형식 파일 로딩"""
        file_path = self.data_dir / filename
        
        if file_path.exists():
            self.submission_format = pd.read_csv(file_path)
            print(f"제출 형식 로딩 완료: {self.submission_format.shape}")
        
        return self.submission_format
    
    def get_basic_info(self):
        """데이터 기본 정보 출력"""
        if self.train_data is None:
            print("데이터가 로딩되지 않았습니다.")
            return
        
        print("=== 데이터 기본 정보 ===")
        print(f"데이터 크기: {self.train_data.shape}")
        print(f"컬럼: {list(self.train_data.columns)}")
        print(f"데이터 타입:\n{self.train_data.dtypes}")
        print(f"결측치:\n{self.train_data.isnull().sum()}")
        print(f"기간: {self.train_data.iloc[0, 0]} ~ {self.train_data.iloc[-1, 0]}")


def create_submission_file(predictions, output_path="submission.csv"):
    """예측 결과를 제출 형식으로 저장"""
    submission_df = pd.DataFrame({
        'date': pd.date_range(start='2024-01-01', periods=len(predictions), freq='D'),
        'prediction': predictions
    })
    
    submission_df.to_csv(output_path, index=False)
    print(f"제출 파일 저장 완료: {output_path}")
    return submission_df 