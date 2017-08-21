"""
Repos endpoints tests.
"""

import requests
import json
import os
from flask import Flask
from flask_testing import TestCase
from flask_restful import Api
from api.repos import CreatePullRequest
from api.users import Login


class TestCaseRepo(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCaseRepo, self).__init__(*args, **kwargs)
        self.load_test_config()

    def create_app(self):
        app = Flask(__name__)
        app.config.from_object('config.TestConfig')
        api = Api(app)
        api.add_resource(CreatePullRequest, '/repos/create_pull_request/')
        api.add_resource(Login, '/users/login/')
        return app

    def load_test_config(self):
        test_config = os.path.join(os.getcwd(), 'test_config')
        self.credentials = {}

        with open(test_config, 'r') as f:
            for line in f.readlines():
                k, v = line.split(':')
                self.credentials.update({k.strip(): v.strip()})

    def close_pull_request(self, number, token):
        patch_url = self.app.config.get('GITHUB_API_UPDATE_PULL_REQUEST').format(owner=self.credentials['login'],
                                                                                 repo=self.credentials['repository'],
                                                                                 number=number)
        headers = {'Authorization': 'Basic ' + token}
        requests.patch(patch_url, data=json.dumps({'state': 'closed'}), headers=headers)

    def test_pull_request_without_required_specific_param(self):
        post_data = {'login': self.credentials.get('login'),
                     'password': self.credentials.get('password')}
        login_response = self.client.post("/users/login/", data=post_data)
        token = json.loads(login_response.data)['token']

        for argument in CreatePullRequest.REQUIRED_ARGUMENTS:
            post_data = {arg: arg for arg in CreatePullRequest.REQUIRED_ARGUMENTS if arg != argument}
            post_data.update({'token': token})
            response = self.client.post("/repos/create_pull_request/", data=post_data)
            self.assertEqual(response.status_code, 422)
            self.assertEqual(json.loads(response.data), {'message': 'Missing required arguments : ' + argument})

    def test_pull_request_without_all_required_params(self):
        post_data = {'login': self.credentials.get('login'),
                     'password': self.credentials.get('password')}
        login_response = self.client.post("/users/login/", data=post_data)
        token = json.loads(login_response.data)['token']

        post_data = {'token': token}
        response = self.client.post("/repos/create_pull_request/", data=post_data)
        self.assertEqual(response.status_code, 422)
        missing_args = sorted(list(CreatePullRequest.REQUIRED_ARGUMENTS))
        self.assertEqual(json.loads(response.data),
                         {'message': 'Missing required arguments : ' + ','.join(missing_args)})

    def test_pull_request_without_token(self):
        post_data = {}
        response = self.client.post("/repos/create_pull_request/", data=post_data)
        self.assertEqual(json.loads(response.data), {'message': 'Missing authorization token'})

    def test_pull_request_correct_data(self):
        post_data = {'login': self.credentials.get('login'),
                     'password': self.credentials.get('password')}
        login_response = self.client.post("/users/login/", data=post_data)
        token = json.loads(login_response.data)['token']

        post_data = {
            'changeset': 'test',
            'repository': '{}/{}'.format(self.credentials.get('login'), self.credentials.get('repository')),
            'title': 'example pull request',
            'base': 'master',
            'token': token,
            'reviewers': 'notempty'
        }
        response = self.client.post("/repos/create_pull_request/", data=post_data)

        self.assertEqual(response.status_code, 201)

        number = json.loads(response.data)['number']
        self.close_pull_request(number, token)
