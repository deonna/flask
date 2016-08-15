from flask import jsonify, Blueprint
from flask.ext.restful import (
            Resource, Api, reqparse, 
            inputs, fields, marshal, 
            marshal_with, url_for, abort
            )

import models

course_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'url': fields.String,
    'reviews': fields.List(fields.String)
}

def add_reviews(course):
    course.reviews = [url_for('resources.reviews.review', id=review.id)
                      for review in course.review_set]
    return course                    

def course_or_404(course_id):
    try:
        course = models.Course.get(models.Course.id==course_id)
    except models.Course.DoesNotExist:
        abort(404, message="Course {} does not exist.".format(course_id))
    else:
        return course

class CourseList(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required=True,
            help='No course title provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'url',
            required=True,
            help='No course URL provided.',
            location=['form', 'json'],
            type=inputs.url
        )
        super().__init__()
        
    def get(self): 
        # Handles GET, returns json response with application/json content type
        courses = [marshal(add_reviews(course), course_fields)
            for course in models.Course.select()]
        return {'courses': courses}
    
    def post(self):
        args = self.reqparse.parse_args()
        models.Course.create(**args)
        return jsonify({'courses': {'title': 'Python Basics'}})

class Course(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required=True,
            help='No course title provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'url',
            required=True,
            help='No course URL provided',
            location=['form', 'json'],
            type=inputs.url
        )

    @marshal_with(course_fields)        
    def get(self, id):
        return add_reviews(course_or_404(id))      

    @marshal_with(course_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Course.update(**args).where(mdoels.Course.id==id)
        query.execute()
        return (add_reviews(models.course.get(models.Course.id==id), 200, 
                {'Location': url_for('resources.courses.course', id=id)}
            )       
        )

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