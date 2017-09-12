"""
Users endpoints tests.
"""

import json
import unittest
from api import app
from .utils import TestConfigLoaderMixin


class TestCaseUser(unittest.TestCase, TestConfigLoaderMixin):
    def __init__(self, *args, **kwargs):
        super(TestCaseUser, self).__init__(*args, **kwargs)
        self.load_test_config()

    def setUp(self):
        app.config.from_object('config.TestConfig')
        self.client = app.test_client()

    def test_correct_login_and_password(self):
        post_data = {'login': self.test_config_data.get('login'),
                     'password': self.test_config_data.get('password')}
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

    def test_get_followers(self):
        number_of_elements = 2
        page_number = 3
        response = self.client.get(
            "/users/followers/gvanrossum?page={}&per_page={}".format(page_number, number_of_elements))

        data = json.loads(response.data).get('data')
        self.assertNotEqual(data, None)
        self.assertTrue(len(data) <= number_of_elements)
        self.assertEqual(response.status_code, 200)
