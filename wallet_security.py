from app import db
from decimal import Decimal

from app.classes.wallet_bch import Bch_Wallet

def bch_check_balance(user_id, amount):
    userwallet = db.session.query(Bch_Wallet)\
        .filter(Bch_Wallet.user_id == user_id)\
        .first()
    curbal = Decimal(userwallet.currentbalance) + Decimal(amount)
    amounttocheck = Decimal(amount)

    if Decimal(amounttocheck) <= Decimal(curbal):
        return 1
    else:
        return 0
