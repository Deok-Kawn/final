"""
LSTM 모델 구현
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from .base_model import BaseModel


class TimeSeriesDataset(Dataset):
    """시계열 데이터셋 클래스"""
    
    def __init__(self, data, seq_length, target_col):
        self.data = data
        self.seq_length = seq_length
        self.target_col = target_col
        
        # 스케일링
        self.scaler = MinMaxScaler()
        self.scaled_data = self.scaler.fit_transform(data)
        
        # 시퀀스 생성
        self.sequences = []
        self.targets = []
        
        for i in range(len(self.scaled_data) - seq_length):
            seq = self.scaled_data[i:i+seq_length]
            target = self.scaled_data[i+seq_length, target_col]
            self.sequences.append(seq)
            self.targets.append(target)
        
        self.sequences = np.array(self.sequences)
        self.targets = np.array(self.targets)
    
    def __len__(self):
        return len(self.sequences)
    
    def __getitem__(self, idx):
        return torch.FloatTensor(self.sequences[idx]), torch.FloatTensor([self.targets[idx]])


class LSTMNet(nn.Module):
    """LSTM 신경망 모델"""
    
    def __init__(self, input_size, hidden_size=50, num_layers=2, dropout=0.2):
        super(LSTMNet, self).__init__()
        
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # LSTM 레이어
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout,
            batch_first=True
        )
        
        # 출력 레이어
        self.fc = nn.Linear(hidden_size, 1)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x):
        # LSTM forward
        lstm_out, _ = self.lstm(x)
        
        # 마지막 시점의 출력만 사용
        last_output = lstm_out[:, -1, :]
        
        # 드롭아웃 및 최종 예측
        output = self.dropout(last_output)
        output = self.fc(output)
        
        return output


class LSTMModel(BaseModel):
    """LSTM 기반 시계열 예측 모델"""
    
    def __init__(self, seq_length=30, hidden_size=50, num_layers=2, 
                 dropout=0.2, learning_rate=0.001, epochs=100, batch_size=32):
        super().__init__("LSTM")
        
        self.seq_length = seq_length
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.dropout = dropout
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.scaler = None
        self.model = None
        
    def prepare_data(self, df, target_col):
        """데이터 준비"""
        # 숫자형 컬럼만 선택
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        data = df[numeric_cols].values
        
        # 타겟 컬럼 인덱스 찾기
        target_idx = list(numeric_cols).index(target_col)
        
        return data, target_idx
    
    def fit(self, X, y):
        """모델 학습"""
        print(f"LSTM 모델 학습 시작... (Device: {self.device})")
        
        # 데이터 준비
        data, target_idx = self.prepare_data(X, y.name)
        
        # 데이터셋 생성
        dataset = TimeSeriesDataset(data, self.seq_length, target_idx)
        dataloader = DataLoader(dataset, batch_size=self.batch_size, shuffle=True)
        
        # 모델 초기화
        input_size = data.shape[1]
        self.model = LSTMNet(
            input_size=input_size,
            hidden_size=self.hidden_size,
            num_layers=self.num_layers,
            dropout=self.dropout
        ).to(self.device)
        
        # 손실함수 및 옵티마이저
        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        
        # 학습 루프
        self.model.train()
        for epoch in range(self.epochs):
            total_loss = 0
            for sequences, targets in dataloader:
                sequences = sequences.to(self.device)
                targets = targets.to(self.device)
                
                # Forward pass
                outputs = self.model(sequences)
                loss = criterion(outputs, targets)
                
                # Backward pass
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            if (epoch + 1) % 20 == 0:
                avg_loss = total_loss / len(dataloader)
                print(f"Epoch [{epoch+1}/{self.epochs}], Loss: {avg_loss:.4f}")
        
        self.scaler = dataset.scaler
        self.is_fitted = True
        print("LSTM 모델 학습 완료!")
    
    def predict(self, X):
        """예측"""
        if not self.is_fitted:
            raise ValueError("모델이 학습되지 않았습니다.")
        
        self.model.eval()
        predictions = []
        
        # 데이터 준비
        data, _ = self.prepare_data(X, X.columns[0])  # 첫 번째 컬럼을 임시 타겟으로 사용
        scaled_data = self.scaler.transform(data)
        
        with torch.no_grad():
            for i in range(self.seq_length, len(scaled_data)):
                seq = scaled_data[i-self.seq_length:i]
                seq = torch.FloatTensor(seq).unsqueeze(0).to(self.device)
                
                pred = self.model(seq)
                predictions.append(pred.cpu().numpy()[0, 0])
        
        return np.array(predictions)


def create_lstm_model(seq_length=30, hidden_size=50, num_layers=2):
    """LSTM 모델 생성 헬퍼 함수"""
    return LSTMModel(
        seq_length=seq_length,
        hidden_size=hidden_size,
        num_layers=num_layers
    ) 