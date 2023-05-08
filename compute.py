from math import log
import click
import matplotlib.pyplot as plt


def calcul_mensualite(montant, taux, echeances, diviseur=26):
    return (montant * taux / diviseur) / (1 - (1 + (taux / diviseur)) ** -echeances)


def calcul_nombre_echeances(montant, taux, diviseur, mensualite):
    return -(log(1 - ((montant * taux) / (diviseur * mensualite)))) / (log(1 + (taux / diviseur)))


def calcul_montant_restant(mensualite, echeances, taux, diviseur):
    return mensualite * ((1 - (1 + (taux / diviseur)) ** -echeances)) * diviseur / taux


def interet_total(montant, echeances, mensualite):
    return (echeances * mensualite) - montant


def credit_integral(
    montant,
    taux,
    echeances,
    nb_paiements_annuels,
    montant_anticipe: float = None,
    montant_anticipe_echeance: int = None,
) -> list:
    paiement = calcul_mensualite(montant, taux, echeances, nb_paiements_annuels)
    compteur = 1

    total_paiement = 0
    total_interet = 0
    total_capital_rembourse = 0

    res = []

    nb_payments_done = 0

    while compteur <= echeances:
        montant_restant = calcul_montant_restant(
            paiement, echeances - compteur, taux, nb_paiements_annuels
        )
        montant_restant_precedent = calcul_montant_restant(
            paiement, echeances - compteur + 1, taux, nb_paiements_annuels
        )
        remboursement_capital = montant_restant_precedent - montant_restant
        remboursement_interet = paiement - remboursement_capital

        total_paiement += paiement
        total_interet += remboursement_interet
        total_capital_rembourse = total_paiement - total_interet

        if montant_anticipe and montant_anticipe_echeance and montant_anticipe_echeance == compteur:
            total_capital_rembourse += montant_anticipe
            total_paiement += montant_anticipe
            echeances = int(
                calcul_nombre_echeances(
                    montant - total_capital_rembourse,
                    taux,
                    nb_paiements_annuels,
                    paiement,
                )
            )
            compteur = 0
            montant_anticipe = 0

        print(
            f"Payment #{nb_payments_done}, you are going to pay: {remboursement_capital} CAD for capital, {remboursement_interet} d'interet. Total coût {total_paiement}, total interet {total_interet}, total capital rembourse {total_capital_rembourse}"
        )

        res.append(
            {
                "remboursement_capital": remboursement_capital,
                "remboursement_interet": remboursement_interet,
                "total_paiement": total_paiement,
                "total_interet": total_interet,
                "total_capital_rembourse": total_capital_rembourse,
            }
        )

        compteur += 1
        nb_payments_done += 1

    return res


@click.command()
@click.option(
    "--starting-capital",
    help="Capital you loaned, e.g. 400000",
    required=True,
    type=float,
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
@click.option(
    "--early-repayment-amount",
    help="Early repayment, e.g. 20000 ",
    required=False,
    type=float,
)
@click.option(
    "--early-repayment-time",
    help="after which payment you do your early repayment, e.g. 26 == 1 year anniversary ",
    required=False,
    type=int,
)
def compute_credit(
    starting_capital: float,
    rate: float,
    payments_per_year: int,
    regular_payment: float,
    early_repayment_amount: float = None,
    early_repayment_time: int = None,
):
    nb_paiements_initial = int(
        calcul_nombre_echeances(
            float(starting_capital),
            float(rate) / 100,
            int(payments_per_year),
            float(regular_payment),
        )
    )

    print(
        f"You loaned {starting_capital} CAD with rate {rate}%. You pay {regular_payment} CAD, {payments_per_year} times a year."
    )
    print(f"So you are going to pay {nb_paiements_initial} times until you are done.")

    results = credit_integral(
        starting_capital,
        rate / 100,
        nb_paiements_initial,
        payments_per_year,
        early_repayment_amount,
        early_repayment_time,
    )

    fig, ax = plt.subplots()
    xy1 = [x["total_interet"] for x in results]
    xy2 = [x["total_capital_rembourse"] for x in results]
    lines = {
        "interet": xy1,
        "capital": xy2,
    }

    ax.stackplot(
        [i for i in range(len(results))],
        lines.values(),
        labels=lines.keys(),
        alpha=0.8,
    )
    ax.legend(loc="upper left")
    ax.set_title("Loan")
    ax.set_xlabel("payments")
    ax.set_ylabel("CAD")

    plt.show()


if __name__ == "__main__":
    compute_credit()
