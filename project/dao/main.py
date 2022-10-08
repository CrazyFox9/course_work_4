from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO
from project.models import *
from project.tools.security import generate_password_hash


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all_order_by(self, page=None, filter=None):
        stmt = self._db_session.query(self.__model__)
        if filter:
            stmt = stmt.order_by(desc(self.__model__.year))
        elif page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()


class UsersDAO(BaseDAO[User]):
    __model__ = User

    def create(self, user_data):
        user = User(**user_data)
        try:
            self._db_session.add(user)
            self._db_session.commit()
            return user
        except Exception as e:
            print(e)
            self._db_session.rollback()

    def get_user_by_login(self, login):
        try:
            user = self._db_session.query(self.__model__).filter(self.__model__.email == login).one()
            return user
        except Exception as e:
            print(e)
            return []

    def update(self, login, user_data):
        try:
            self._db_session.query(self.__model__).filter(self.__model__.email == login).update(user_data)
            self._db_session.commit()
        except Exception as e:
            print(e)
            self._db_session.rollback()

    def update_password(self, login, user_data):
        try:
            self._db_session.query(self.__model__).filter(self.__model__.email == login).update(
                {
                    "password": generate_password_hash(user_data.get('new_password'))
                }
            )
            self._db_session.commit()
        except Exception as e:
            print(e)
            self._db_session.rollback()
