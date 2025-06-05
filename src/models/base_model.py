"""
모델 베이스 클래스
"""
from abc import ABC, abstractmethod
import numpy as np
import pickle
from pathlib import Path
import joblib


class BaseModel(ABC):
    """모든 모델의 베이스 클래스"""
    
    def __init__(self, model_name="base_model"):
        self.model_name = model_name
        self.model = None
        self.is_fitted = False
        
    @abstractmethod
    def fit(self, X, y):
        """모델 학습"""
        pass
    
    @abstractmethod
    def predict(self, X):
        """예측"""
        pass
    
    def save_model(self, filepath):
        """모델 저장"""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # 모델 저장
        if hasattr(self.model, 'save'):  # PyTorch, TensorFlow 등
            self.model.save(str(filepath))
        else:  # sklearn, lightgbm 등
            joblib.dump(self.model, filepath)
        
        print(f"모델 저장 완료: {filepath}")
    
    def load_model(self, filepath):
        """모델 로딩"""
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {filepath}")
        
        self.model = joblib.load(filepath)
        self.is_fitted = True
        print(f"모델 로딩 완료: {filepath}")
    
    def evaluate(self, y_true, y_pred):
        """모델 평가"""
        from sklearn.metrics import mean_squared_error, mean_absolute_error
        
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mae = mean_absolute_error(y_true, y_pred)
        
        metrics = {
            'RMSE': rmse,
            'MAE': mae,
            'MAPE': np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        }
        
        return metrics
    
    def cross_validate(self, X, y, cv=5):
        """교차 검증"""
        from sklearn.model_selection import TimeSeriesSplit
        from sklearn.metrics import mean_squared_error
        
        tscv = TimeSeriesSplit(n_splits=cv)
        scores = []
        
        for train_idx, val_idx in tscv.split(X):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
            
            # 임시 모델 학습
            temp_model = self.__class__(self.model_name + "_cv")
            temp_model.fit(X_train, y_train)
            
            # 예측 및 평가
            y_pred = temp_model.predict(X_val)
            rmse = np.sqrt(mean_squared_error(y_val, y_pred))
            scores.append(rmse)
        
        return {
            'mean_rmse': np.mean(scores),
            'std_rmse': np.std(scores),
            'scores': scores
        } 