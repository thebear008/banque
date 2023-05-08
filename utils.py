"""all functions to compute credit factors"""


def compute_capital(
    credit_duration_in_year: int,
    rate: float,
    payments_per_year: int,
    regular_payment: float,
) -> float:
    """This function tells you how much capital you can have
    if you have this :rate for :credit_duration_in_year years
    and if you pay :regular_payment :payments_per_year times per year"""

    number_of_payments = credit_duration_in_year * payments_per_year

    factor_one = regular_payment * payments_per_year / (rate / 100)

    factor_two = 1 - (1 + (rate / 100 / payments_per_year)) ** (-number_of_payments)

    return factor_one * factor_two


def get_total_interest(
    capital: float,
    credit_duration_in_year: int,
    payments_per_year: int,
    regular_payment: float,
) -> float:
    """This functions tells you how much you credit will cost
    from interest perspective if you pay :regular_payment :payments_per_year times
    per year for :credit_duration_in_year years"""

    return (regular_payment * payments_per_year * credit_duration_in_year) - capital
