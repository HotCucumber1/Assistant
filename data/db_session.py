import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec
from sqlalchemy.orm import Session


SqlAlchemyBase = dec.declarative_base()
__factory = None


def global_init(db_file: str):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных")

    connection = f"sqlite:///{db_file.strip()}?check_same_thread=False"
    print('Подключение к базе данных по адресу:', connection)

    engine = sa.create_engine(connection, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from data import __all_models
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
