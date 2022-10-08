from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.container import auth_service
from project.setup.api.models import user

api = Namespace('auth')


@api.route('/register/')
class RegisterView(Resource):
    @api.marshal_with(user, code=201, description='OK')
    def post(self):
        req_json = request.json
        login = req_json.get('email')
        password = req_json.get('password')
        if not login or not password:
            return "Введите логин и пароль", 400
        return user_service.create(req_json), 201


@api.route('/login/')
class LoginView(Resource):
    @api.response(404, 'Not Found')
    def post(self):
        req_json = request.json
        login = req_json.get('email')
        password = req_json.get('password')
        if not login or not password:
            return "Не введен логин или пароль", 400

        tokens = auth_service.generate_tokens(login, password)
        if tokens:
            return tokens, 201
        return "Ошибка в запросе", 401

    @api.response(404, 'Not Found')
    def put(self):
        req_json = request.json
        access_token = req_json.get('access_token')
        refresh_token = req_json.get('refresh_token')

        if not access_token or not refresh_token:
            return "Нужны access и refresh токены", 400
        return auth_service.approve_refresh_token(refresh_token), 201
