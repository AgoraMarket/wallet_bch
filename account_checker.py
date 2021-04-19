
from app import db

from app.models import \
    BchWallet, \
    User, \
    BchWalletAddresses,\
    BchUnconfirmed


def accounts_no_address_fix():
    """
    Gets all users see if wallet is ok.
    If not redirects it

    :return:
    """
    getusers = db.session.query(User).all()
    for f in getusers:
        userswallet = db.session.query(BchWallet).filter(f.id == BchWallet.user_id).first()
        if userswallet:
            if userswallet.address1.startswith('bitcoincash'):
                pass
            else:
                bch_get_address(userswallet)
        else:
            bch_create_wallet(user_id=f.user_id)

    print("committed")
    db.session.commit()


def bch_get_address(userswallet):
    """
    if user has a wallet but no address
    :param userswallet:
    :return:
    """
    # get the user an unused address
    print("user id has no address: ", userswallet.user_id)
    # sets users wallet with this address
    getnewaddress = db.session.query(BchWalletAddresses).filter(BchWalletAddresses.status == 0).first()
    userswallet.address1 = getnewaddress.bchaddress
    userswallet.address1status = 1
    # update address in listing as used
    getnewaddress.status = 1

    db.session.add(userswallet)
    db.session.add(getnewaddress)

    print("adding an address to the wallet", getnewaddress.bchaddress)


def bch_create_wallet(user_id):
    """
    if no address or wallet!
    :param user_id:
    :return:
    """
    getnewaddress = db.session.query(BchWalletAddresses).filter(BchWalletAddresses.status == 0).first()

    # if user has no wallet in database
    # create it and give it an address
    print("user id has no address OR WALLET..failure somewhere!: ", user_id)
    print("fixing problem")
    # create a new wallet
    btc_cash_walletcreate = BchWallet(user_id=user_id,
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
    btc_cash_newunconfirmed = BchUnconfirmed(
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

    print("created wallet:", getnewaddress.bchaddress)


if __name__ == '__main__':
    accounts_no_address_fix()
