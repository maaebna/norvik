import requests
from xml.etree import ElementTree as ET
import pandas as pd

# URL для запроса к API ЦБ РФ
url = "https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?op=KeyRate"

# Выполняем запрос к API
response = requests.get(url)
# Парсим XML ответ
root = ET.fromstring(response.content)

# Извлекаем данные о ключевой ставке
key_rates = []
for item in root.findall('.//KeyRate'):
    date = item.find('Date').text
    rate = float(item.find('Value').text.replace(',', '.'))
    key_rates.append({'date': date, 'rate': rate})

# Создаем DataFrame
key_rates_df = pd.DataFrame(key_rates)
key_rates_df['date'] = pd.to_datetime(key_rates_df['date'])

# Объединяем таблицы transactions и key_rates по дате
transactions['date'] = pd.to_datetime(transactions['date'])
merged_df = pd.merge(transactions, key_rates_df, on='date', how='left')

# Рассчитываем упущенный процентный доход
merged_df['missed_income'] = merged_df['bal_end_of_day'] * (merged_df['rate'] / 100) / 365


def calculate_cash_delivery_fees(row):
    # Получаем тарифы для конкретного банкомата
    fee_row = fees[fees['atm_id'] == row['atm_id']].iloc[0]

    # Расчет фиксированной и процентной части
    fixed_fee = fee_row['CashDeliveryFixedFee']
    percentage_fee = max(fee_row['CashDeliveryMinFee'], row['cash_in'] * fee_row['CashDeliveryPercentageFee'])

    return fixed_fee + percentage_fee


merged_df['incassation_expenses'] = merged_df.apply(calculate_cash_delivery_fees, axis=1)

import matplotlib.pyplot as plt

# График снятий и пополнений по дням
plt.figure(figsize=(14, 7))
plt.plot(merged_df['date'], merged_df['cash_out'], label='Снятия', color='blue')
plt.plot(merged_df['date'], merged_df['cash_in'], label='Пополнения', color='green')
plt.title('Снятия и пополнения по дням')
plt.xlabel('Дата')
plt.ylabel('Сумма (руб.)')
plt.legend()
plt.show()