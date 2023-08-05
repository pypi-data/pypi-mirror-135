import logging
import uuid

from typing import Callable, Optional

from context_helper import Context, ctx
from graphql_api import GraphQLAPI

try:
    from sqlalchemy_orm import Database, TypeMapper, EnumType, UUIDType
    from sqlalchemy_orm.base.base import Model
    from sqlalchemy_orm.query import Query

except ImportError:
    raise ImportError("DataRM package not found")

from sqlalchemy_gql.relay_base import RelayBase


Base = Model(type_map=TypeMapper(types=[EnumType, UUIDType]))


@GraphQLAPI.type(abstract=True)
class ModelBase(RelayBase, Base):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__()

    @classmethod
    def query(cls, session=None) -> Query:
        if session is None:
            if ctx.db_session is None:
                raise AttributeError(
                    "db_session not set in the current context"
                )
            return ctx.db_session.query(cls)

        return super().query(session=session)

    @classmethod
    def filter(cls, *args, **kwargs) -> Query:
        query = cls.query()
        if args:
            query = query.filter(*args)
        if kwargs:
            query = query.filter_by(**kwargs)

        return query

    @classmethod
    def get(cls, id: uuid.UUID = None) -> Optional['Base']:
        if id:
            return cls.filter(id=id).one_or_none()

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"<{self.__class__.__name__} id: '{str(self.id)[:4]}'>"

    def create(self, session=None):
        if session is None:
            session = ctx.db_session

        return session.add(self)

    @GraphQLAPI.field(mutable=True)
    def delete(self, session=None) -> bool:
        if session is None:
            session = ctx.db_session

        session.delete(self)
        return True


class DatabaseManager:

    def __init__(self, url: str = "sqlite:///pool.db"):
        self.logger = logging.getLogger("db")
        self.logger.info(f"Connecting DatabaseService with url {url}")

        self.url = url
        self.db = Database(url)
        self.base = ModelBase

    def with_db_session(
        self,
        func: Callable = None,
        context_key_name="db_session"
    ):
        """
        Create a db session, then wrap `func`
        in a new context so it can access the db session.
        """
        def with_context(*args, **kwargs):
            db_session = self.db.session()
            response = None

            try:
                with Context(**{context_key_name: db_session}):
                    response = func(*args, **kwargs)

            except Exception as err:
                db_session.rollback()
                raise err
            else:
                db_session.commit()
            finally:
                db_session.close()

            return response

        return with_context

    def install(self, wipe_database_if_not_empty=True) -> bool:
        """
        Create the models in the db
        """
        if not self.db.is_empty():
            if wipe_database_if_not_empty:
                self.logger.info(f"Wiping db '{self.db}'")
                self.db.wipe()
            else:
                self.logger.warning(
                    f"Attempted setup to a db '{self.db}' that was not empty"
                )

        self.logger.info("Installing user management db.")

        # Create tables
        self.db.create_all(self.base)

        return True
