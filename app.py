import decimal

import flask
from flask import render_template, request
from decimal import Decimal, ROUND_DOWN


def calculer_economies(offre_actuelle, offre_nouvelle):
    """
  Calcule les économies réalisées en passant d'une offre à une autre.

  Args:
    offre_actuelle: Le prix de l'offre actuelle en euros.
    offre_nouvelle: Le prix de la nouvelle offre en euros.

  Returns:
    Les économies réalisées en euros.
  """
    economies = ((offre_actuelle - offre_nouvelle) * 12) / 12
    decimal.getcontext().rounding = ROUND_DOWN
    decimalvalue = Decimal(economies)
    return decimalvalue.quantize(Decimal('0.01'))


# Définition de l'application web

app = flask.Flask(__name__)


# Route pour la page d'accueil

@app.route("/")
def index():
    offers = [
        {
            "name": "Livebox Fibre",
            "price": 42.99
        },
        {
            "name": "Livebox Up Fibre",
            "price": 51.99
        },
        {
            "name": "Livebox Max Fibre",
            "price": 67.98
        },
        {
            "name": "Open Up 40Go Fibre",
            "price": 71.99
        }
    ]

    return render_template('index.html', economies=False, offers=offers)


# Route pour le calcul des économies

@app.route("/calculer", methods=["POST"])
def calculer():
    # Récupération des données du formulaire

    prix_offre_actuelle = request.form.get("offre_actuelle")
    prix_offre_nouvelle = request.form.get("offre_nouvelle")

    # Conversion des champs en nombres flottants

    prix_offre_actuelle = float(prix_offre_actuelle)
    prix_offre_nouvelle = float(prix_offre_nouvelle)

    # Calcul des économies

    economies = calculer_economies(prix_offre_actuelle, prix_offre_nouvelle)

    # Affichage des résultats

    return render_template('index.html', economies=economies)


# Lancement de l'application web

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
