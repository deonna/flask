from flask import jsonify, Blueprint, abort

from flask.ext.restful import (Resource, Api, reqparse, inputs, fields,
                               url_for, marshal, marshal_with)

import models

user_fields = {
    'username': fields.String,
    'email': fields.String,
    'password': fields.String
}

def user_or_404(user_id):
    try:
        user = models.User.get(models.User.id==user_id)
    except models.User.DoesNotExist:
        abort(404)
    else:
        return user

class UserList(Resource):
    def __init__:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_resource(
            'username',
            required=True,
            help='No username provided.'
            location=['form', 'json']
        )
        self.reqparse.add_resource(
            'email',
            required=True,
            help='No email provided.',
            location=['form', 'json']
        )
        self.reqparse.add_resource(
            'password',
            required=True,
            help='No password provided.',
            location=['form', 'json']
        )
    
    @marshal_with(user_fields)
    def post(self):
        args = self.reqparse.parse_args()
        user = models.User.create(**args)
        return (
            user, 
            200,
            {'Location': url_for('resources.users.user', id=user.id)}
            )

class User(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        return user_or_404(id)            

users_api = Blueprint('resources.users', __name__)

api = Api(users_api)
api.add_resource(
    UserList,
    '/users',
    endpoint='users'
)
api.add_resource(
    User,
    '/users/<int:id>',
    endpoint='user'
)