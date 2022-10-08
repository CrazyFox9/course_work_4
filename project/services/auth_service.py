from flask_restx import abort

from project.dao import UsersDAO
from project.tools.security import compare_passwords

import calendar
import datetime
import jwt

from flask import current_app


class AuthService:
    def __init__(self, dao: UsersDAO):
        self.dao = dao

    def get_user_by_login(self, login):
        return self.dao.get_user_by_login(login)

    def generate_tokens(self, login, password, is_refresh=False):
        user = self.get_user_by_login(login)

        if not user:
            abort(404)

        if not is_refresh:
            if not compare_passwords(user.password, password):
                return "Введите верный логин или пароль"

        data = {
            "email": user.email,
            "password": user.password
        }

        # 15 min for access_token
        min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
        data["exp"] = calendar.timegm(min15.timetuple())
        access_token = jwt.encode(data, key=current_app.config['SECRET_KEY'], algorithm=current_app.config['JWT_ALG'])

        # 130 days for refresh_token
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, key=current_app.config['SECRET_KEY'], algorithm=current_app.config['JWT_ALG'])

        return {"access_token": access_token, "refresh_token": refresh_token}

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=current_app.config['SECRET_KEY'],
                          algorithms=[current_app.config['JWT_ALG']])
        login = data['email']
        user = self.get_user_by_login(login)

        if not user:
            abort(404)

        return self.generate_tokens(login, user.password, is_refresh=True)
