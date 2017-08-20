"""
API endpoints related to repositories.
"""

import requests
import base64
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

        args = parser.parse_args()
        repo_owner, repo_name = args['repository'].split('/')  # full repository name format : 'owner/repo_name'

        userandpasw = base64.urlsafe_b64encode(bytes("%s:%s" % ('', ''), 'utf-8')).decode('ascii')

        post_data = {"title": args['title'] or "This is a title of pull request",
                     "body": args.get('body') or "This is a pull request.",
                     "head": '{}:{}'.format(repo_owner,args['changeset']),  # Regards to Github API documentation, changeset is the branch name
                     "base": "master"}

        headers = {'Authorization': 'Basic ' + userandpasw}
        r = requests.post(app.config['GITHUB_API_CREATE_PULL_REQUEST'].format(owner=repo_owner, repos=repo_name), data=json.dumps(post_data), headers=headers)

        return