#!/usr/bin/env python3
"""
Демонстрационный скрипт для калькулятора ипотеки
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from calculator import (
    calculate_monthly_payment,
    calculate_total_payment,
    calculate_total_interest,
    calculate_loan_schedule
)


def main():
    print("🏠 Калькулятор ипотеки")
    print("=" * 50)

    # Пример расчета
    principal = 2000000  # 2 млн руб
    annual_rate = 7.5  # 7.5% годовых
    years = 15  # 15 лет

    print(f"Сумма кредита: {principal:,} руб.")
    print(f"Процентная ставка: {annual_rate}% годовых")
    print(f"Срок кредита: {years} лет")
    print("-" * 50)

    # Расчет основных показателей
    monthly_payment = calculate_monthly_payment(principal, annual_rate, years)
    total_payment = calculate_total_payment(monthly_payment, years)
    total_interest = calculate_total_interest(total_payment, principal)

    print(f"📅 Ежемесячный платеж: {monthly_payment:,.2f} руб.")
    print(f"💰 Общая сумма выплат: {total_payment:,.2f} руб.")
    print(f"💸 Переплата по кредиту: {total_interest:,.2f} руб.")
    print(f"📊 Переплата в процентах: {(total_interest / principal) * 100:.1f}%")

    # График платежей (первые 12 месяцев)
    print("\n📈 График платежей (первые 12 месяцев):")
    print("-" * 80)
    print(f"{'Месяц':<6} {'Платеж':<12} {'Основной долг':<15} {'Проценты':<12} {'Остаток':<12}")
    print("-" * 80)

    schedule = calculate_loan_schedule(principal, annual_rate, years)
    for payment in schedule[:12]:
        print(f"{payment['month']:<6} {payment['payment']:<12,.2f} {payment['principal']:<15,.2f} "
              f"{payment['interest']:<12,.2f} {payment['balance']:<12,.2f}")

    # Пример с нулевой процентной ставкой
    print("\n🔍 Пример с нулевой процентной ставкой:")
    print("-" * 50)
    principal_zero = 120000
    monthly_zero = calculate_monthly_payment(principal_zero, 0, 10)
    print(f"Сумма кредита: {principal_zero:,} руб. под 0% на 10 лет")
    print(f"Ежемесячный платеж: {monthly_zero:,.2f} руб.")
    print(f"Общая сумма выплат: {monthly_zero * 12 * 10:,.2f} руб.")
    print(f"Переплата: 0 руб.")


if __name__ == "__main__":
    main()