"""How much capital can you get from your bank?"""
import click
from utils import compute_capital, get_total_interest


@click.command()
@click.option(
    "--credit-duration-in-year",
    help="How long for your credit in years, e.g. 25 years",
    required=True,
    type=int,
)
@click.option("--rate", help="rate loan, e.g. 2.44", required=True, type=float)
@click.option(
    "--payments-per-year",
    help="number of payments per year, e.g. 26 or 24",
    default=26,
    type=int,
)
@click.option(
    "--regular-payment",
    help="Payment you make on regular basis",
    required=True,
    type=float,
)
def main(
    credit_duration_in_year: int,
    rate: float,
    payments_per_year: int,
    regular_payment: float,
):
    """How much capital can you get from your bank?"""
    capital = compute_capital(
        credit_duration_in_year=credit_duration_in_year,
        rate=rate,
        payments_per_year=payments_per_year,
        regular_payment=regular_payment,
    )

    total_interest = get_total_interest(
        capital=capital,
        credit_duration_in_year=credit_duration_in_year,
        payments_per_year=payments_per_year,
        regular_payment=regular_payment,
    )

    total_per_year = regular_payment * payments_per_year

    percentage_total_interest = 100 * total_interest / (capital + total_interest)

    print(
        f"""
You can loan a capital of : {capital}
  - you will pay {total_per_year} per year for {credit_duration_in_year} years
  - at the end, you will have paid {capital + total_interest}
  - full interest amount for the bank will be: {total_interest} (i.e. {percentage_total_interest} %)
        """
    )


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
