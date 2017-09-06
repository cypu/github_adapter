"""
API endpoints related to users.
"""

import requests
import base64
from flask_restful import Resource, reqparse
import flask


class GetFollowers(Resource):
    """
    Provide tha ability to get github user followers.
    """

    def get(self, user):
        """Request for a list of followers for specific user.
        
        :param user: github login
        :return: json object with list of followers 
        """
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int)
        parser.add_argument('per_page', type=int)

        args = parser.parse_args()
        page = args.get('page') or 1
        per_page = args.get('per_page') or 10
        followers = requests.get(
            flask.current_app.config['GITHUB_API_USER_FOLLOWERS'].format(user, page, per_page)).json()
        follower_fields = ('login', 'email', 'location', 'public_repos')

        for index, follower in enumerate(followers):
            follower_details = requests.get(flask.current_app.config['GITHUB_API_USER_DETAILS'].format(follower['login'])).json()
            followers[index] = {x: follower_details[x] for x in follower_fields}

        response = {
            'data': followers,
            'next_page': flask.current_app.config['SERVER_URL'] + '/users/followers/{}?page={}&per_page={}'.format(user, page + 1,
                                                                                                     per_page),
            'prev_page': flask.current_app.config['SERVER_URL'] + '/users/followers/{}?page={}&per_page={}'.format(user, page - 1,
                                                                                                     per_page),
        }

        return response


class Login(Resource):
    """
    Provide authorisation to API.
    """

    def post(self):
        """Handling log in operation  
        
        :return: json with message about authorisation status, response status code.
                 returns authorisation token when credentials are correct
        """
        parser = reqparse.RequestParser()
        parser.add_argument('login')
        parser.add_argument('password')
        args = parser.parse_args()

        login = args.get('login')
        password = args.get('password')

        if login and password:
            token = base64.urlsafe_b64encode(bytes("%s:%s" % (login, password), 'utf-8')).decode('ascii')
            headers = {'Authorization': 'Basic ' + token}

            # Confirm that credentials are correct
            r = requests.get(flask.current_app.config['GITHUB_USER_LOGIN_ENDPOINT'], headers=headers)

            if r.status_code == requests.codes.ok:
                return {'token': token}, requests.codes.ok
            else:
                return r.json(), r.status_code

        else:
            return {'message': 'Missing password or login'}, 401
