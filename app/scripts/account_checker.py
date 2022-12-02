
from app import db
from app.classes.auth import Auth_User
from app.classes.wallet_bch import \
    Bch_Wallet, \
    Bch_WalletAddresses,\
    Bch_WalletUnconfirmed



def bch_get_address(userswallet):
    """
    if user has a wallet but no address
    :param userswallet:
    :return:
    """
    # get the user an unused address

    print(f"user id has no address: {userswallet.user_id}")
    # sets users wallet with this address
    getnewaddress = db.session\
        .query(Bch_WalletAddresses)\
        .filter(Bch_WalletAddresses.status == 0)\
        .first()
    userswallet.address1 = getnewaddress.bchaddress
    userswallet.address1status = 1
    # update address in listing as used
    getnewaddress.status = 1

    db.session.add(userswallet)
    db.session.add(getnewaddress)

    print(f"adding an address to the wallet {getnewaddress.bchaddress}")

def bch_create_wallet(user_id):
    """
    if no address or wallet!
    :param user_id:
    :return:
    """

    getnewaddress = db.session\
        .query(Bch_WalletAddresses)\
        .filter(Bch_WalletAddresses.status == 0)\
        .first()

    # if user has no wallet in database
    # create it and give it an address

    print(f"user id has no address OR WALLET..failure somewhere! {user_id}")
    print("fixing problem")

    # create a new wallet
    btc_cash_walletcreate = Bch_Wallet(user_id=user_id,
                                      currentbalance=0,
                                      unconfirmed=0,
                                      address1=getnewaddress.bchaddress,
                                      address1status=1,
                                      address2='',
                                      address2status=0,
                                      address3='',
                                      address3status=0,
                                      locked=0,
                                      transactioncount=0
                                      )
    # add an unconfirmed
    btc_cash_newunconfirmed = Bch_WalletUnconfirmed(
        user_id=user_id,
        unconfirmed1=0,
        unconfirmed2=0,
        unconfirmed3=0,
        unconfirmed4=0,
        unconfirmed5=0,
        txid1='',
        txid2='',
        txid3='',
        txid4='',
        txid5='',
    )
    getnewaddress.status = 1

    db.session.add(getnewaddress)
    db.session.add(btc_cash_walletcreate)
    db.session.add(btc_cash_newunconfirmed)


    print(f"created wallet: {getnewaddress.bchaddress}")
def main():
    """
    Gets all users see if wallet is ok.
    If not redirects it

    :return:
    """
    getusers = db.session\
        .query(Auth_User)\
        .all()
    amount = 0
    for f in getusers:
        userswallet = db.session\
            .query(Bch_Wallet)\
            .filter(f.id == Bch_Wallet.user_id)\
            .first()
        # if wallet doesnt exist
        if not userswallet:
            # create a wallet
            bch_create_wallet(user_id=f.user_id)
        else:
            # if wallet starts with bitcoincash do nothing
            if userswallet.address1.startswith('bitcoincash'):
                pass
            else:
                # get address
                bch_get_address(userswallet)

                # add counter for commit
                newamount = amount =+ 1
                amount = amount + newamount

    if amount > 0:
        db.session.commit()


