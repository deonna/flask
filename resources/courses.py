from flask import jsonify, Blueprint
from flask.ext.restful import Resource, Api

import models

class CourseList(Resource):
    def get(self): 
        # Handles GET, returns json response with application/json content type
        return jsonify({'courses': {'title': 'Python Basics'}})

class Course(Resource):
    def get(self, id):
        return jsonify({'title': 'Python Basics'})        

    def put(self, id):
        return jsonify({'title': 'Python Basics'})        

    def delete(self, id):
        return jsonify({'title': 'Python Basics'})        

# proxy to the module that sort-of acts like an apply
# all the actions on the Blueprint don't happen until registered
courses_api = Blueprint('resources.courses', __name__)
api = Api(courses_api)
api.add_resource(
    CourseList,
    '/courses',
    endpoint='courses'
)
api.add_resource(
    Course,
    '/course/<int:id>',
    endpoint='course'
)