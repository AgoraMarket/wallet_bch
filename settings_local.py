from decimal import Decimal


class ApplicationConfig:
    CURRENT_SETTINGS = 'LOCAL'
    # databases info
    POSTGRES_USERNAME = 'postgres'
    POSTGRES_PW = 'password'
    POSTGRES_SERVER = 'database:5432'
    POSTGRES_DBNAME00 = 'clearnet'
    SQLALCHEMY_DATABASE_URI_0 = "postgresql+psycopg2://{}:{}@{}/{}".format(POSTGRES_USERNAME,
                                                                        POSTGRES_PW,
                                                                        POSTGRES_SERVER,
                                                                        POSTGRES_DBNAME00)
    SQLALCHEMY_BINDS = {'clearnet': SQLALCHEMY_DATABASE_URI_0}

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    DIGITAL_CURRENCY = 2

    MINCONF = str(6)
    MIN_AMOUNT = Decimal(0.00000001)
    MAX_AMOUNT = Decimal(0.5)

    RPC_USERNAME = 'droid'
    RPC_PASSWORD = '!Julie774'

    URL = "http://droid:julie774@127.0.0.1:8332/"
