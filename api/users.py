"""
API endpoints related to users.
"""

import requests
import base64
from flask_restful import Resource, reqparse
from . import app


class GetFollowers(Resource):
    """
    Provide tha ability to get github user followers.
    """

    def get(self, user):
        """Request for a list of followers for specific user.
        
        :param user: github login
        :return: json object with list of followers 
        """
        followers = requests.get(app.config['GITHUB_API_USER_FOLLOWERS'].format(user)).json()
        follower_fields = ['login', 'email', 'location', 'public_repos']

        for index, follower in enumerate(followers):
            follower_details = requests.get(app.config['GITHUB_API_USER_DETAILS'].format(follower['login'])).json()
            followers[index] = {x: follower_details[x] for x in follower_fields}

        return followers


class Login(Resource):
    """
    Provide login.
    """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('login')
        parser.add_argument('password')
        args = parser.parse_args()
        username = args['login']
        password = args['password']

        url = 'https://api.github.com/user'
        passanduser = base64.urlsafe_b64encode(bytes("%s:%s" % (username, password), 'utf-8')).decode('ascii')

        headers = {'Authorization': 'Basic ' + passanduser}

        r = requests.get(url, headers=headers)

        return
