from datetime import datetime

from app import db
from app.classes.wallet_bch import Bch_WalletTransactions
    
now = datetime.utcnow()
   
   
def add_transaction(category,
                    amount,
                    user_id,
                    txid,
                    block,
                    balance,
                    confirmed,
                    fee,
                    address):   
    # create and watch transaction
    trans = Bch_WalletTransactions(
        category=3,
        user_id=user_id,
        confirmations=howmanyconfs,
        txid=txid,
        amount=amount2,
        address='',
        blockhash='',
        timerecieved=0,
        timeoft=0,
        commentbch='',
        otheraccount=0,
        balance=shortaddcurrent,
        fee=0,
        confirmed=0,
        orderid=0,
        senderid=0,
        digital_currency=dcurrency,
        confirmed_fee=0,
    )
    db.session.add(trans)
    db.session.commit()