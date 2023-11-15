import os
import decimal

import flask
from flask import render_template, request
from decimal import Decimal, ROUND_CEILING

from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import DecimalField, SelectField, validators

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
        "price": 57.99
    },
    {
        "name": "Open Up 40Go Fibre",
        "price": 71.99
    }
]


class CalculEconomiesForm(FlaskForm):
    offre_actuelle = SelectField(label="Choississez votre offre actuelle",
                                 choices=[(offer["price"], offer["name"]) for offer in offers])
    offre_nouvelle = SelectField("Choississez votre nouvelle offre",
                                 choices=[(offer["price"], offer["name"]) for offer in offers])
    prix_forfait_mobile = DecimalField("Prix du forfait mobile",
                                       validators=[validators.DataRequired(), validators.NumberRange(min=0)])


def calculer_economies_annuel(offre_actuelle, offre_nouvelle, prix_forfait_mobile):
    """
  Calcule les économies réalisées en passant d'une offre à une autre.

  Args:
    offre_actuelle: Le prix de l'offre actuelle en euros.
    offre_nouvelle: Le prix de la nouvelle offre en euros.
    prix_forfait_mobile: Le prix du forfait mobile en euros.

  Returns:
    Les économies réalisées en euros.
  """
    economies = (offre_actuelle - (offre_nouvelle + prix_forfait_mobile)) * 12
    decimal.getcontext().rounding = ROUND_CEILING
    decimalvalue = Decimal(economies)
    return decimalvalue.quantize(Decimal('0.00'))


def calculer_economies_mensuel(offre_actuelle, offre_nouvelle, prix_forfait_mobile):
    """
  Calcule les économies réalisées en passant d'une offre à une autre.

  Args:
    offre_actuelle: Le prix de l'offre actuelle en euros.
    offre_nouvelle: Le prix de la nouvelle offre en euros.
    prix_forfait_mobile: Le prix du forfait mobile en euros.

  Returns:
    Les économies réalisées en euros.
  """
    economies = (offre_actuelle - (offre_nouvelle + prix_forfait_mobile)) * 12 / 12
    decimal.getcontext().rounding = ROUND_CEILING
    decimalvalue = Decimal(economies)
    return decimalvalue.quantize(Decimal('0.00'))


# Définition de l'application web

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

csrf = CSRFProtect(app)


# Route pour la page d'accueil

@app.route("/")
def index():
    form = CalculEconomiesForm()

    return render_template('index.html', economiesannuel=False, economiesmensuel=False, offers=offers, form=form)


# Route pour le calcul des économies

@app.route("/", methods=["POST"])
def calculer():
    form = CalculEconomiesForm()

    if form.validate_on_submit():
        offre_actuelle = float(form.offre_actuelle.data)
        offre_nouvelle = float(form.offre_nouvelle.data)
        prix_forfait_mobile = float(form.prix_forfait_mobile.data)

        # Calcul des économies

        economiesannuel = calculer_economies_annuel(offre_actuelle, offre_nouvelle, prix_forfait_mobile)
        economiesmensuel = calculer_economies_mensuel(offre_actuelle, offre_nouvelle, prix_forfait_mobile)

        # Affichage des résultats

        return render_template('index.html', economiesannuel=economiesannuel, economiesmensuel=economiesmensuel,
                               form=form)

    # Affichage des résultats

    return render_template('index.html', economiesannuel=None, economiesmensuel=None, form=form)


# Lancement de l'application web

if __name__ == "__main__":
    app.run(debug=True)
