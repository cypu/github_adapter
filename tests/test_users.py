"""
Users endpoints tests.
"""

import requests
from flask import Flask
from flask_testing import TestCase
from api.users import GetFollowers, Login
from flask_restful import Api


class TestCaseUser(TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config.from_object('config.TestConfig')
        api = Api(app)
        api.add_resource(GetFollowers, '/users/<string:user>')
        api.add_resource(Login, '/users/login/')

        return app

    def test_correct_login_and_password(self):
        post_data = {'login': '',
                     'password': ''}
        response = self.client.post("/users/login/", data=post_data)
        self.assertEqual(response.status_code, 200)

    def test_correct_login_incorrect_password(self):
        post_data = {'login': 'cypu',
                     'password': 'pass1'}
        response = self.client.post("/users/login/", data=post_data)
        self.assertEqual(response.status_code, 401)

    def test_incorrect_login_and_password(self):
        post_data = {'login': 'this_is_incorrect_login',
                     'password': 'this_is_incorrect_password'}
        response = self.client.post("/users/login/", data=post_data)
        self.assertEqual(response.status_code, 401)

    def test_request_without_login(self):
        post_data = {'password': 'this_is_incorrect_password'}
        response = self.client.post("/users/login/", data=post_data)
        self.assertEqual(response.status_code, 401)

    def test_request_without_password(self):
        post_data = {'login': 'cypu'}
        response = self.client.post("/users/login/", data=post_data)
        self.assertEqual(response.status_code, 401)

    def test_request_without_login_password(self):
        post_data = {}
        response = self.client.post("/users/login/", data=post_data)
        self.assertEqual(response.status_code, 401)