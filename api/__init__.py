"""
Github API adapter.
"""

from flask import Flask
from flask_restful import Api


app = Flask(__name__)
app.config.from_object('config.Config')
api = Api(app)

#  http://flask.pocoo.org/docs/0.12/patterns/packages/  -> Circular Imports
from .users import GetFollowers
from .repos import CreatePullRequest

api.add_resource(GetFollowers, '/users/<string:user>')
api.add_resource(CreatePullRequest, '/repos/create_pull_request/')
