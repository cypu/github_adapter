"""
API endpoints related to repositories.
"""

import requests
import json
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
        parser.add_argument('token')

        args = parser.parse_args()

        if args.get('token'):
            repo_owner, repo_name = args['repository'].split('/')  # full repository name format : 'owner/repo_name'

            post_data = {"title": args.get('title') or "This is a title of pull request",
                         "body": args.get('body') or "This is a pull request.",
                         "head": '{}:{}'.format(repo_owner, args['changeset']),
                         # Regards to Github API documentation, changeset is the branch name
                         "base": "master"}

            headers = {'Authorization': 'Basic ' + userandpasw}
            r = requests.post(app.config['GITHUB_API_CREATE_PULL_REQUEST'].format(owner=repo_owner, repos=repo_name),
                              data=json.dumps(post_data), headers=headers)

            return r.json(), r.status_code
        else:
            return {'message': 'Missing authorization token'}, 401
