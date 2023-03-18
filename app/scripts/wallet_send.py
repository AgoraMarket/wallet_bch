import requests
import json
from app import\
    url,\
    digital_currency,\
    minamount, \
    maxamount
from decimal import Decimal
from datetime import datetime
from app import db
from app.notification import \
    notification
from app.common.functions import \
    floating_decimals
from app.classes.wallet_bch import\
    Bch_Wallet,\
    Bch_WalletTransactions,\
    Bch_WalletFee,\
    Bch_WalletWork
from app.classes.auth import Auth_User

def securitybeforesending(sendto, user, adjusted_amount):
    """
    # This function checks regex, amounts, and length of addrss
    """

    regexpasses = 1

    # test if length of address is ok
    if 24 <= len(sendto) <= 36:
        lengthofaddress = 1
    else:
        lengthofaddress = 0
        notification(username=user.display_name,
                     user_uuid=user.uuid,
                     msg="Incorrect address for destination")

    # test to see if amount when adjusted is not too little or too much
    if Decimal(minamount) <= Decimal(adjusted_amount) <= Decimal(maxamount):
        amountcheck = 1
    else:
        amountcheck = 0
        notification(username=user.display_name,
                     user_uuid=user.uuid,
                     msg="Security didnt not allow sending coin")

    # count amount to pass
    totalamounttopass = regexpasses + lengthofaddress + amountcheck
    if totalamounttopass == 3:
        itpasses = True
    else:
        itpasses = False

    return itpasses


def sendcoin(user, sendto, amount, comment):
    """
    # This function sends the coin off site
    """

    # variables
    dcurrency = digital_currency
    timestamp = datetime.utcnow()

    # get the fee from db
    getwallet = db.session\
        .query(Bch_WalletFee)\
        .filter_by(id=1)\
        .first()
    walletfee = getwallet.btc
    # get the users wall
    userswallet = db.session\
        .query(Bch_Wallet)\
        .filter_by(user_id=user.id)\
        .first()
    # proceed to see if balances check
    curbal = floating_decimals(userswallet.currentbalance, 8)
    amounttomod = floating_decimals(amount, 8)
    adjusted_amountadd = floating_decimals(amounttomod - walletfee, 8)
    adjusted_amount = floating_decimals(adjusted_amountadd, 8)

    sendto_str = str(sendto)
    final_amount_str = str(adjusted_amount)
    comment_str = str(comment)

    # double check user
    securetosend = securitybeforesending(sendto=sendto,
                                         user_id=user.id,
                                         adjusted_amount=adjusted_amount
                                         )
    if securetosend is False:
        notification(username=user.display_name,
                     user_uuid=user.uuid,
                     msg="Security or amount did not allow sending")
    else:
        # send call to rpc
        cmdsendcoin = sendcoincall(address=str(sendto_str),
                                   amount=str(final_amount_str),
                                   comment=str(comment_str)
                                   )

        print("sending a transaction..")
        print("txid: ", cmdsendcoin['result'])

        print("*"*15)
        txid = cmdsendcoin['result']

        # adds to transactions with txid and confirmed = 0 so we can watch it
        trans = Bch_WalletTransactions(
            category=2,
            user_id=user.id,
            confirmations=0,
            txid=txid,
            blockhash='',
            timeoft=0,
            timerecieved=0,
            otheraccount=0,
            address='',
            fee=walletfee,
            created=timestamp,
            commentbch=comment_str,
            amount=amount,
            orderid=0,
            balance=curbal,
            confirmed=0,
            digital_currency=dcurrency
        )

        notification(username=user.display_name,
                     user_uuid=user.uuid,
                     msg="Coin has been successfully sent to destination.")

        db.session.add(userswallet)
        db.session.add(trans)




def sendcoincall(address, amount, comment):
    # standard json header
    headers = {'content-type': 'application/json'}

    rpc_input = {
        "method": "sendtoaddress",
        "params":
            {"address": address,
             "amount": amount,
             "comment": comment,
             "subtractfeefromamount": True,
             }
    }

    # add standard rpc values
    rpc_input.update({"jsonrpc": "1.0", "id": "0"})

    # execute the rpc request
    response = requests.post(
        url,
        data=json.dumps(rpc_input),
        headers=headers,
    )
    # the response in json
    response_json = response.json()

    return response_json

def main():
    """
    # main query
    """
    # see if any bitcoin work is waiting
    work = db.session\
        .query(Bch_WalletWork) \
        .filter(Bch_WalletWork.type == 2) \
        .order_by(Bch_WalletWork.created.desc()) \
        .all()

    if work:
        for f in work:
            # send coin off site
            if f.type == 2:
                user = db.session\
                    .query(Auth_User)\
                    .filter(Auth_User.id==f.user_id)\
                    .first()
                sendcoin(user=user,
                         sendto=f.sendto,
                         amount=f.amount,
                         comment=f.txtcomment)
                f.type = 0

        db.session.commit()
    else:
        print("no wallet work")

