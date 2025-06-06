#!/usr/bin/env python3
import pandas as pd
from datetime import datetime

# 데이터 로딩
df = pd.read_csv('data/shared/data.csv')
df['date'] = pd.to_datetime(df['date'], format='%Y.%m.%d')

# 전체 날짜 범위 생성
start_date = df['date'].min()
end_date = df['date'].max()
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# 누락된 날짜들 찾기
missing_dates = set(date_range) - set(df['date'])
missing_dates_list = sorted(list(missing_dates))

print(f'📅 누락된 모든 날짜 ({len(missing_dates_list)}개):')
print('=' * 50)

for i, missing_date in enumerate(missing_dates_list, 1):
    day_name = missing_date.strftime('%A')
    day_name_kr = {'Monday': '월요일', 'Tuesday': '화요일', 'Wednesday': '수요일', 
                   'Thursday': '목요일', 'Friday': '금요일', 'Saturday': '토요일', 'Sunday': '일요일'}[day_name]
    print(f'{i:2d}. {missing_date.strftime("%Y년 %m월 %d일")} ({day_name_kr})')

# 요일별 분포 확인
weekday_counts = {}
for missing_date in missing_dates_list:
    day_name = missing_date.strftime('%A')
    day_name_kr = {'Monday': '월요일', 'Tuesday': '화요일', 'Wednesday': '수요일', 
                   'Thursday': '목요일', 'Friday': '금요일', 'Saturday': '토요일', 'Sunday': '일요일'}[day_name]
    weekday_counts[day_name_kr] = weekday_counts.get(day_name_kr, 0) + 1

print(f'\n📊 요일별 누락 분포:')
for day, count in weekday_counts.items():
    print(f'- {day}: {count}개')

# 연도별 분포
year_counts = {}
for missing_date in missing_dates_list:
    year = missing_date.year
    year_counts[year] = year_counts.get(year, 0) + 1

print(f'\n📅 연도별 누락 분포:')
for year, count in sorted(year_counts.items()):
    print(f'- {year}년: {count}개')

# 2005년 초반에 집중되어 있는지 확인
print(f'\n🔍 2005년 1-3월 누락 패턴:')
early_2005 = [d for d in missing_dates_list if d.year == 2005 and d.month <= 3]
for missing_date in early_2005:
    day_name = missing_date.strftime('%A')
    day_name_kr = {'Monday': '월요일', 'Tuesday': '화요일', 'Wednesday': '수요일', 
                   'Thursday': '목요일', 'Friday': '금요일', 'Saturday': '토요일', 'Sunday': '일요일'}[day_name]
    print(f'- {missing_date.strftime("%Y년 %m월 %d일")} ({day_name_kr})') 