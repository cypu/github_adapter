"""
Repos endpoints tests.
"""

import requests
import json
from flask import Flask
from flask_testing import TestCase
from flask_restful import Api
from api.repos import CreatePullRequest


class TestCaseRepo(TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config.from_object('config.TestConfig')
        api = Api(app)
        api.add_resource(CreatePullRequest, '/repos/create_pull_request/')

        return app

    def test_pull_request_without_auth_token(self):
        post_data = {}
        response = self.client.post("/repos/create_pull_request/", data=post_data)
        self.assertEqual(response.status_code, 401)
        json.loads(response.data)
        self.assertEqual(json.loads(response.data), {'message': 'Missing authorization token'})

    def test_pull_request_correct_data(self):

        post_data = {
            'changeset': '',
            'repository': '',
            'title': '',
            'base': 'master',
            'token': '',
            'reviewers': ''
        }
        response = self.client.post("/repos/create_pull_request/", data=post_data)
        self.assertEqual(response.status_code, 201)
