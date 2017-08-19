"""
API endpoints related to repositories.
"""

import requests
from flask_restful import Resource, reqparse
from . import app


class CreatePullRequest(Resource):
    """
    Provide the ability to create pull request.
    """

    def post(self):
        """
        
        :return: 
        """
        parser = reqparse.RequestParser()
        parser.add_argument('changeset')
        parser.add_argument('repository')
        parser.add_argument('title')

        args = parser.parse_args()
        repo_owner, repo_name = args['repository'].split('/')  # full repository name format : 'owner/repo_name'

        post_data = {"title": args['title'] or "This is a title of pull request",
                     "body": args.get('body') or "This is a pull request.",
                     "head": 'cypu:'+args['changeset'],  # Regards to Github API documentation, changeset is the branch name
                     "base": "master"}

        r = requests.post(app.config['GITHUB_API_CREATE_PULL_REQUEST'].format(owner=repo_owner, repos=repo_name), data=post_data)

        return