from flask import request
from flask_restx import Namespace, Resource
from project.container import user_service
from project.setup.api.models import user


api = Namespace('user')


@api.route('/')
class UserView(Resource):
    @api.marshal_with(user, code=200, description='OK')
    def get(self):
        """
        Get user by login.
        """
        req_json = request.json
        header = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')

        return user_service.get_user_by_token(refresh_token=header), 200

    @api.marshal_with(user, code=204, description='OK')
    def patch(self):
        """
        Patch user by login.
        """
        data = request.json
        header = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')

        return user_service.update_user(user_data=data, refresh_token=header), 204


@api.route('/password/')
class PasswordView(Resource):
    def put(self):
        """
        Change users password by login.
        """
        data = request.json
        header = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')

        return user_service.update_password(user_data=data, refresh_token=header), 204
