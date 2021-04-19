from app import db
from app.models import BchWalletWork


# run once every day
def deleteoldorder():

    getwork = db.session.query(BchWalletWork).filter_by(type=0).all()
    if getwork:
        for f in getwork:
            db.session.delete(f)
        db.session.commit()


if __name__ == '__main__':
    deleteoldorder()
