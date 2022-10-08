from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия')
})

director: Model = api.model('Директор', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Квентин Тарантино')
})

movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=255, example='Джанго Освобождённый'),
    'description': fields.String(required=True, max_length=255, example='Описание фильма'),
    'trailer': fields.String(required=True, max_length=255, example='//https://www.какойтосайт.com/watch?v'),
    'year': fields.Integer(required=True, example=2022),
    'rating': fields.Float(required=True, example=8.6),
    'genre': fields.Nested(genre),
    'director': fields.Nested(director)
})

user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, max_length=100, example='kljsdnvjnf@mail.ru'),
    'name': fields.String(required=True, max_length=100, example='Eduard'),
    'surname': fields.String(required=True, max_length=100, example="Kozhukhov"),
    'genre': fields.Nested(genre)
})
