#!/bin/bash
# Task Master - Python 3.8.20 Environment Setup Script
# 이 스크립트를 실행하여 Python 3.8 환경을 활성화합니다.

echo "Activating Task Master Python 3.8.20 environment..."

# Conda 환경 활성화
source /opt/anaconda3/bin/activate taskmaster_py38

# Python 버전 확인
echo "Python version check:"
python --version

# 설치된 패키지 주요 버전 확인
echo "Key packages versions:"
python -c "
import pandas as pd
import numpy as np
import torch
import sklearn
import matplotlib
import seaborn

print(f'✓ Pandas: {pd.__version__}')
print(f'✓ NumPy: {np.__version__}') 
print(f'✓ PyTorch: {torch.__version__}')
print(f'✓ Scikit-learn: {sklearn.__version__}')
print(f'✓ Matplotlib: {matplotlib.__version__}')
print(f'✓ Seaborn: {seaborn.__version__}')
"

echo ""
echo "Environment successfully activated!"
echo "You can now use Task Master with Python 3.8.20"
echo ""
echo "To activate this environment manually, run:"
echo "conda activate taskmaster_py38"
echo ""
echo "To deactivate the environment, run:"
echo "conda deactivate" 