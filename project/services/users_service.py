from typing import Optional

from project.dao import UsersDAO
from project.exceptions import ItemNotFound, InvalidPassword
from project.models import User
from project.tools.security import generate_password_hash, get_data_from_token, compare_passwords


class UsersService:
    def __init__(self, dao: UsersDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> User:
        if director := self.dao.get_by_id(pk):
            return director
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> list[User]:
        return self.dao.get_all(page=page)

    def create(self, user_data):
        user_data["password"] = generate_password_hash(user_data.get("password"))
        self.dao.create(user_data)

    def get_user_by_login(self, login):
        return self.dao.get_user_by_login(login)

    def get_user_by_token(self, refresh_token):
        data = get_data_from_token(refresh_token)

        if data:
            return self.get_user_by_login(data.get('email'))
        raise ItemNotFound(f'Пользователь не найден')

    def update_user(self, user_data, refresh_token):
        user = self.get_user_by_token(refresh_token)

        if user:
            self.dao.update(login=user.email, user_data=user_data)
        return user

    def update_password(self, user_data, refresh_token):
        user = self.get_user_by_token(refresh_token)
        password = user.password
        old_password = user_data.get('old_password')

        if user:
            if compare_passwords(password, old_password):
                self.dao.update_password(login=user.email, user_data=user_data)
            else:
                raise InvalidPassword('Неверный пароль')
