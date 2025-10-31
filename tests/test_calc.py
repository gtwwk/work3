import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from calculator import (
    calculate_monthly_payment,
    calculate_total_payment,
    calculate_total_interest,
    calculate_loan_schedule
)


class TestMortgageCalculator:

    def test_monthly_payment_calculation(self):
        """Тест расчета ежемесячного платежа"""
        # Кредит 1 000 000 руб на 10 лет под 7% годовых
        payment = calculate_monthly_payment(1000000, 7, 10)
        # Проверяем, что платеж в разумных пределах
        assert 11000 < payment < 12000
        assert payment == 11610.85  # Наше вычисленное значение

        # Кредит 2 000 000 руб на 15 лет под 8% годовых
        payment = calculate_monthly_payment(2000000, 8, 15)
        assert 19000 < payment < 20000
        assert payment == 19113.04  # Наше вычисленное значение

    def test_monthly_payment_calculation_with_tolerance(self):
        """Тест расчета ежемесячного платежа с допуском"""
        # Проверяем несколько случаев с проверкой логики, а не точных значений
        test_cases = [
            (1000000, 7, 10, 11610, 11611),  # 1 млн на 10 лет под 7%
            (2000000, 8, 15, 19113, 19114),  # 2 млн на 15 лет под 8%
            (500000, 5, 5, 9435, 9436),  # 500 тыс на 5 лет под 5%
            (1500000, 6, 20, 10746, 10747),  # 1.5 млн на 20 лет под 6%
        ]

        for principal, rate, years, min_expected, max_expected in test_cases:
            payment = calculate_monthly_payment(principal, rate, years)
            assert min_expected <= payment <= max_expected, \
                f"Ошибка для {principal} под {rate}% на {years} лет: получено {payment}, ожидается между {min_expected} и {max_expected}"

    def test_monthly_payment_zero_interest(self):
        """Тест расчета платежа при нулевой процентной ставке"""
        payment = calculate_monthly_payment(120000, 0, 10)
        expected_payment = 1000.00  # 120000 / (10 * 12)
        assert payment == expected_payment

        # Дополнительные проверки для нулевой ставки
        payment2 = calculate_monthly_payment(240000, 0, 20)
        expected_payment2 = 1000.00  # 240000 / (20 * 12)
        assert payment2 == expected_payment2

    def test_monthly_payment_invalid_input(self):
        """Тест обработки невалидных входных данных"""
        with pytest.raises(ValueError):
            calculate_monthly_payment(-100000, 7, 10)

        with pytest.raises(ValueError):
            calculate_monthly_payment(100000, -7, 10)

        with pytest.raises(ValueError):
            calculate_monthly_payment(100000, 7, -10)

    def test_total_payment_calculation(self):
        """Тест расчета общей суммы выплат"""
        monthly_payment = 11610.85
        years = 10
        total = calculate_total_payment(monthly_payment, years)
        expected_total = 11610.85 * 12 * 10
        assert total == round(expected_total, 2)

        # Проверка округления
        assert calculate_total_payment(1000.00, 1) == 12000.00
        assert calculate_total_payment(500.50, 2) == 12012.00

    def test_total_interest_calculation(self):
        """Тест расчета общей переплаты"""
        total_payment = 1393302.00  # 11610.85 * 12 * 10
        principal = 1000000
        total_interest = calculate_total_interest(total_payment, principal)
        expected_interest = 393302.00
        assert total_interest == expected_interest

        # Дополнительные проверки
        assert calculate_total_interest(120000, 100000) == 20000.00
        assert calculate_total_interest(50000, 50000) == 0.00

    def test_loan_schedule(self):
        """Тест расчета графика платежей"""
        schedule = calculate_loan_schedule(100000, 12, 1)

        # Проверяем общее количество платежей
        assert len(schedule) == 12

        # Проверяем структуру каждого платежа
        for payment in schedule:
            assert 'month' in payment
            assert 'payment' in payment
            assert 'principal' in payment
            assert 'interest' in payment
            assert 'balance' in payment
            assert isinstance(payment['month'], int)
            assert isinstance(payment['payment'], (int, float))
            assert isinstance(payment['principal'], (int, float))
            assert isinstance(payment['interest'], (int, float))
            assert isinstance(payment['balance'], (int, float))

        # Проверяем, что последний платеж обнуляет баланс
        last_payment = schedule[-1]
        assert last_payment['balance'] == 0.00

        # Проверяем, что сумма основного долга и процентов равна платежу (с учетом округления)
        for payment in schedule:
            calculated_payment = payment['principal'] + payment['interest']
            assert abs(calculated_payment - payment['payment']) < 0.02

    def test_loan_schedule_accuracy(self):
        """Тест точности графика платежей"""
        schedule = calculate_loan_schedule(100000, 12, 1)
        total_principal = sum(payment['principal'] for payment in schedule)
        total_interest = sum(payment['interest'] for payment in schedule)

        # Сумма выплаченного основного долга должна равняться исходной сумме кредита
        # Допускаем небольшую погрешность из-за округления
        assert abs(total_principal - 100000) < 0.05

        # Общая сумма выплат должна равняться сумме всех платежей
        total_payments = sum(payment['payment'] for payment in schedule)
        assert abs(total_payments - (total_principal + total_interest)) < 0.05

    def test_loan_schedule_complete_payment(self):
        """Тест полного погашения кредита"""
        test_cases = [
            (50000, 10, 2),
            (100000, 5, 1),
            (200000, 8, 3),
        ]

        for principal, rate, years in test_cases:
            schedule = calculate_loan_schedule(principal, rate, years)

            # Проверяем, что кредит полностью погашен
            assert schedule[-1]['balance'] == 0.00

            # Проверяем, что общая сумма выплаченного основного долга равна начальной сумме
            total_principal = sum(payment['principal'] for payment in schedule)
            assert abs(total_principal - principal) < 0.05

    def test_consistency_between_functions(self):
        """Тест согласованности между функциями калькулятора"""
        test_cases = [
            (1000000, 7, 10),
            (500000, 5, 5),
            (1500000, 6, 20),
        ]

        for principal, rate, years in test_cases:
            # Расчет ежемесячного платежа
            monthly = calculate_monthly_payment(principal, rate, years)

            # Расчет общей суммы выплат
            total = calculate_total_payment(monthly, years)

            # Расчет переплаты
            interest = calculate_total_interest(total, principal)

            # Проверяем согласованность
            assert abs(total - (principal + interest)) < 0.01

            # Проверяем, что ежемесячный платеж разумен
            assert monthly > principal / (years * 12)  # Должен быть больше, чем при нулевой ставке