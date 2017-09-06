"""
Github API adapter.
"""

from flask import Flask
from flask_restful import Api
from .users import GetFollowers, Login
from .repos import CreatePullRequestWithReviews


app = Flask(__name__)
app.config.from_object('config.DevConfig')
api = Api(app)

api.add_resource(GetFollowers, '/users/followers/<string:user>')
api.add_resource(Login, '/users/login/')
api.add_resource(CreatePullRequestWithReviews, '/repos/create_pull_request/')
