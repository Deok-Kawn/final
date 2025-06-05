"""
실험 추적 및 로그 관리
"""
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class ExperimentTracker:
    """실험 결과 추적 및 관리 클래스"""
    
    def __init__(self, experiment_dir="experiments"):
        self.experiment_dir = Path(experiment_dir)
        self.experiment_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_file = self.experiment_dir / "experiment_log.json"
        self.experiments = self.load_experiments()
    
    def load_experiments(self):
        """기존 실험 로그 로딩"""
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_experiments(self):
        """실험 로그 저장"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.experiments, f, indent=2, ensure_ascii=False)
    
    def log_experiment(self, model_name, hyperparams, metrics, notes=""):
        """실험 결과 로깅"""
        experiment = {
            'timestamp': datetime.now().isoformat(),
            'model_name': model_name,
            'hyperparams': hyperparams,
            'metrics': metrics,
            'notes': notes,
            'experiment_id': len(self.experiments) + 1
        }
        
        self.experiments.append(experiment)
        self.save_experiments()
        
        print(f"✓ 실험 #{experiment['experiment_id']} 로깅 완료")
        print(f"  모델: {model_name}")
        print(f"  RMSE: {metrics.get('RMSE', 'N/A'):.4f}")
        
        return experiment['experiment_id']
    
    def get_experiment(self, experiment_id):
        """특정 실험 조회"""
        for exp in self.experiments:
            if exp['experiment_id'] == experiment_id:
                return exp
        return None
    
    def list_experiments(self, top_n=10):
        """실험 목록 조회"""
        df = pd.DataFrame(self.experiments)
        
        if df.empty:
            print("기록된 실험이 없습니다.")
            return df
        
        # RMSE 기준으로 정렬
        if 'metrics' in df.columns:
            df['RMSE'] = df['metrics'].apply(lambda x: x.get('RMSE', float('inf')))
            df = df.sort_values('RMSE').head(top_n)
        
        # 출력용 포맷팅
        display_cols = ['experiment_id', 'model_name', 'RMSE', 'timestamp', 'notes']
        available_cols = [col for col in display_cols if col in df.columns]
        
        print(f"=== 상위 {min(top_n, len(df))}개 실험 ===")
        print(df[available_cols].to_string(index=False))
        
        return df[available_cols]
    
    def compare_experiments(self, experiment_ids):
        """실험 비교"""
        experiments = [self.get_experiment(eid) for eid in experiment_ids]
        experiments = [exp for exp in experiments if exp is not None]
        
        if not experiments:
            print("비교할 실험이 없습니다.")
            return
        
        comparison_data = []
        for exp in experiments:
            data = {
                'experiment_id': exp['experiment_id'],
                'model_name': exp['model_name'],
                'timestamp': exp['timestamp']
            }
            
            # 메트릭 추가
            data.update(exp['metrics'])
            
            # 주요 하이퍼파라미터 추가
            for key, value in exp['hyperparams'].items():
                if key in ['learning_rate', 'epochs', 'batch_size', 'hidden_size']:
                    data[key] = value
            
            comparison_data.append(data)
        
        df = pd.DataFrame(comparison_data)
        print("=== 실험 비교 ===")
        print(df.to_string(index=False))
        
        return df
    
    def plot_experiment_history(self, metric='RMSE'):
        """실험 히스토리 시각화"""
        if not self.experiments:
            print("기록된 실험이 없습니다.")
            return
        
        df = pd.DataFrame(self.experiments)
        
        if 'metrics' not in df.columns:
            print("메트릭 정보가 없습니다.")
            return
        
        # 메트릭 추출
        df[metric] = df['metrics'].apply(lambda x: x.get(metric, None))
        df = df.dropna(subset=[metric])
        
        if df.empty:
            print(f"{metric} 정보가 없습니다.")
            return
        
        # 시각화
        plt.figure(figsize=(12, 6))
        
        # 시간순 메트릭 변화
        plt.subplot(1, 2, 1)
        plt.plot(df['experiment_id'], df[metric], marker='o')
        plt.xlabel('실험 ID')
        plt.ylabel(metric)
        plt.title(f'{metric} 변화 추이')
        plt.grid(True)
        
        # 모델별 메트릭 비교
        plt.subplot(1, 2, 2)
        model_metrics = df.groupby('model_name')[metric].agg(['mean', 'min', 'count'])
        model_metrics.plot(kind='bar', y='mean', ax=plt.gca())
        plt.xlabel('모델')
        plt.ylabel(f'평균 {metric}')
        plt.title(f'모델별 평균 {metric}')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        # 이미지 저장
        save_path = self.experiment_dir / f"{metric}_history.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"차트 저장: {save_path}")
        
        plt.show()
    
    def export_to_csv(self, filename="experiment_results.csv"):
        """실험 결과 CSV 출력"""
        if not self.experiments:
            print("기록된 실험이 없습니다.")
            return
        
        # 데이터 플래튼
        flattened_data = []
        for exp in self.experiments:
            data = {
                'experiment_id': exp['experiment_id'],
                'model_name': exp['model_name'],
                'timestamp': exp['timestamp'],
                'notes': exp['notes']
            }
            
            # 메트릭 플래튼
            data.update(exp['metrics'])
            
            # 하이퍼파라미터 플래튼
            for key, value in exp['hyperparams'].items():
                data[f'param_{key}'] = value
            
            flattened_data.append(data)
        
        df = pd.DataFrame(flattened_data)
        
        # CSV 저장
        filepath = self.experiment_dir / filename
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"실험 결과 CSV 저장: {filepath}")
        
        return df


class ModelComparison:
    """모델 성능 비교 도구"""
    
    @staticmethod
    def compare_predictions(y_true, predictions_dict, title="모델 예측 비교"):
        """여러 모델의 예측 결과 비교"""
        plt.figure(figsize=(15, 8))
        
        # 실제값 플롯
        plt.plot(y_true, label='실제값', linewidth=2, alpha=0.8)
        
        # 각 모델의 예측값 플롯
        colors = plt.cm.Set1(np.linspace(0, 1, len(predictions_dict)))
        for i, (model_name, y_pred) in enumerate(predictions_dict.items()):
            plt.plot(y_pred, label=f'{model_name} 예측', 
                    color=colors[i], linewidth=1.5, alpha=0.7)
        
        plt.xlabel('시간')
        plt.ylabel('값')
        plt.title(title)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def create_metrics_table(models_metrics):
        """모델별 메트릭 비교 테이블"""
        df = pd.DataFrame(models_metrics).T
        
        # 포맷팅
        for col in df.columns:
            if col in ['RMSE', 'MAE', 'MAPE']:
                df[col] = df[col].round(4)
        
        print("=== 모델 성능 비교 ===")
        print(df.to_string())
        
        return df 