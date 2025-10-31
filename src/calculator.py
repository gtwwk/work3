def calculate_monthly_payment(principal, annual_rate, years):

    if principal <= 0:
        raise ValueError("Сумма кредита должна быть положительной")
    if annual_rate < 0:
        raise ValueError("Процентная ставка не может быть отрицательной")
    if years <= 0:
        raise ValueError("Срок кредита должен быть положительным")

    monthly_rate = annual_rate / 100 / 12
    num_payments = years * 12

    if monthly_rate == 0:
        return round(principal / num_payments, 2)

    monthly_payment = (principal * monthly_rate *
                       (1 + monthly_rate) ** num_payments) / \
                      ((1 + monthly_rate) ** num_payments - 1)

    return round(monthly_payment, 2)


def calculate_total_payment(monthly_payment, years):

    return round(monthly_payment * years * 12, 2)


def calculate_total_interest(total_payment, principal):

    return round(total_payment - principal, 2)


def calculate_loan_schedule(principal, annual_rate, years):

    monthly_payment = calculate_monthly_payment(principal, annual_rate, years)
    monthly_rate = annual_rate / 100 / 12
    balance = principal
    schedule = []

    for month in range(1, years * 12 + 1):
        interest_payment = balance * monthly_rate
        principal_payment = monthly_payment - interest_payment

        # Корректировка последнего платежа
        if month == years * 12:
            principal_payment = balance
            monthly_payment = principal_payment + interest_payment
            balance = 0
        else:
            balance -= principal_payment
            # Избегаем отрицательного баланса из-за округления
            balance = max(round(balance, 10), 0)

        schedule.append({
            'month': month,
            'payment': round(monthly_payment, 2),
            'principal': round(principal_payment, 2),
            'interest': round(interest_payment, 2),
            'balance': round(balance, 2)
        })

    return schedule