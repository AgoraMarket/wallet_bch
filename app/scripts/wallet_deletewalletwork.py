from app import db
from app.classes.wallet_bch import Bch_WalletWork


# run once every day
def main():
    """
    See if any thing int he database is completed and destroy it.  Keep records for a month
    """
    getwork = db.session\
        .query(Bch_WalletWork)\
        .filter_by(type=0)\
        .all()
    if getwork:
        for f in getwork:
            db.session.delete(f)
        db.session.commit()


if __name__ == '__main__':
    main()
