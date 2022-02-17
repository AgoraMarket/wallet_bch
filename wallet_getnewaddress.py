
from app import db
from app.classes.wallet_bch import Bch_Wallet, Bch_WalletTransactions, Bch_WalletAddresses


def getnewaddress(user_id):
    """
    THIS function gets a new address for the user
    :param user_id:
    :return:
    """
    userswallet = db.session.query(Bch_Wallet) \
        .filter_by(user_id=user_id) \
        .first()
    x = db.session.query(Bch_WalletAddresses) \
        .filter(Bch_WalletAddresses.status == 0) \
        .first()

    # Test to see if user doesn't have any current incomming transactions..get new one if not
    incdeposit = db.session.query(Bch_WalletTransactions) \
        .filter(Bch_WalletTransactions.category == 3,
                Bch_WalletTransactions.confirmed == 0,
                Bch_WalletTransactions.user_id == user_id,
                ) \
        .first()
    if incdeposit is None:
        # status 0 = not used
        # status 1 = current main
        # status 2 = used
        if userswallet.address1status == 1:
            userswallet.address1status = 2
            userswallet.address2 = x.bchaddress
            userswallet.address2status = 1
            userswallet.address3status = 0

            x.user_id = user_id
            x.status = 1

            db.session.add(x)
            db.session.add(userswallet)
            db.session.commit()

        elif userswallet.address2status == 1:
            userswallet.address2status = 2
            userswallet.address3 = x.bchaddress
            userswallet.address3status = 1
            userswallet.address1status = 0

            x.user_id = user_id
            x.status = 1

            db.session.add(x)
            db.session.add(userswallet)
            db.session.commit()

        elif userswallet.address3status == 1:
            userswallet.address3status = 2
            userswallet.address1 = x.bchaddress
            userswallet.address1status = 1
            userswallet.address2status = 0

            x.user_id = user_id
            x.status = 1

            db.session.add(userswallet)
            db.session.add(x)
            db.session.commit()
        elif userswallet.address3status == 0 \
                and userswallet.address2status == 0 \
                and userswallet.address1status == 0:
            userswallet.address3status = 2
            userswallet.address1 = x.bchaddress
            userswallet.address1status = 1
            userswallet.address2status = 0

            x.user_id = user_id
            x.status = 1

            db.session.add(userswallet)
            db.session.add(x)
            db.session.commit()
        elif userswallet.address3status == 1 \
                and userswallet.address2status == 1 \
                and userswallet.address1status == 1:
            userswallet.address3status = 2
            userswallet.address1 = x.bchaddress
            userswallet.address1status = 1
            userswallet.address1status = 1
            userswallet.address2status = 0

            x.user_id = user_id
            x.status = 1

            db.session.add(userswallet)
            db.session.add(x)
            db.session.commit()
        elif userswallet.address3status == 2 \
                and userswallet.address2status == 2 \
                and userswallet.address1status == 2:
            userswallet.address3status = 2
            userswallet.address1 = x.bchaddress
            userswallet.address1status = 1
            userswallet.address2status = 0

            x.user_id = user_id
            x.status = 1

            db.session.add(userswallet)
            db.session.add(x)
            db.session.commit()
        elif userswallet.address3status == 3 \
                and userswallet.address2status == 3 \
                and userswallet.address1status == 3:
            userswallet.address3status = 2
            userswallet.address1 = x.bchaddress
            userswallet.address1status = 1
            userswallet.address2status = 0

            x.user_id = user_id
            x.status = 1

            db.session.add(userswallet)
            db.session.add(x)
            db.session.commit()
        else:
            pass

