from app import db
from decimal import Decimal

from app.models import BchWallet


def checkbalance(user_id, amount):
    userwallet = db.session.query(BchWallet)\
        .filter(BchWallet.user_id == user_id)\
        .first()
    curbal = Decimal(userwallet.currentbalance) + Decimal(amount)
    amounttocheck = Decimal(amount)

    if Decimal(amounttocheck) <= Decimal(curbal):
        return 1
    else:
        return 0
