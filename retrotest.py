import pandas as pd
import numpy as np

# Загрузка данных
fees = pd.read_parquet('https://storage.yandexcloud.net/norvpublic/fees.parquet')
transactions = pd.read_parquet('https://storage.yandexcloud.net/norvpublic/transactions.parquet')


# Функция для расчета расходов на инкассацию
def calculate_incassation_expenses(row, fees):
    fee_row = fees[fees['atm_id'] == row['atm_id']].iloc[0]
    fixed_fee = fee_row['CashDeliveryFixedFee']
    percentage_fee = max(fee_row['CashDeliveryMinFee'], row['cash_in'] * fee_row['CashDeliveryPercentageFee'])
    return fixed_fee + percentage_fee


# Функция для оценки уровня сервиса
def calculate_service_level(transactions, service_level_threshold):
    total_cash_out = transactions['cash_out'].sum()
    total_cash_in = transactions['cash_in'].sum()

    # Определяем, сколько наличных должно быть доступно
    required_cash = total_cash_out * (1 / service_level_threshold)

    # Проверяем, достаточно ли наличных было в банкоматах
    if total_cash_in >= required_cash:
        return True  # Уровень сервиса достигнут
    else:
        return False  # Уровень сервиса не достигнут


# Моделирование различных сценариев
service_levels = [0.80, 0.90, 0.95]
results = []

for service_level in service_levels:
    total_expenses = 0
    for index, row in transactions.iterrows():
        # Расчет расходов на инкассацию
        expenses = calculate_incassation_expenses(row, fees)
        total_expenses += expenses

    # Оценка уровня сервиса
    service_level_met = calculate_service_level(transactions, service_level)

    results.append({
        'service_level': service_level,
        'total_expenses': total_expenses,
        'service_level_met': service_level_met
    })

# Преобразование результатов в DataFrame для удобного анализа
results_df = pd.DataFrame(results)

# Вывод результатов
print(results_df)