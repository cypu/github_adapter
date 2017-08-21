"""
Github API adapter.
"""

from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app.config.from_object('config.DevConfig')
api = Api(app)

#  http://flask.pocoo.org/docs/0.12/patterns/packages/  -> Circular Imports
from .users import GetFollowers, Login
from .repos import CreatePullRequestWithReviews

api.add_resource(GetFollowers, '/users/followers/<string:user>')
api.add_resource(Login, '/users/login/')
api.add_resource(CreatePullRequestWithReviews, '/repos/create_pull_request/')
