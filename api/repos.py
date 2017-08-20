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
        arguments = ('changeset', 'repository', 'title', 'base', 'token', 'reviewers')
        # branch name
        # full repository name format : 'owner/repo_name'
        parser = reqparse.RequestParser()
        [parser.add_argument(arg) for arg in arguments]
        args = parser.parse_args()

        if args.get('token') and args.get('title') and args.get('changeset') and args.get('base'):

            repo_owner, repo_name = args['repository'].split('/')

            post_data = {"title": args.get('title'),
                         "body": args.get('body') or "This is a pull request.",
                         "head": '{}:{}'.format(repo_owner, args['changeset']),
                         # Regards to Github API documentation, changeset is the branch name
                         "base": "master"}

            headers = {'Authorization': 'Basic ' + args.get('token')}
            r = requests.post(app.config['GITHUB_API_CREATE_PULL_REQUEST'].format(owner=repo_owner, repos=repo_name),
                              data=json.dumps(post_data), headers=headers)

            if r.status_code == requests.codes.ok:
                # request the reviews to reviewers
                pass

            return r.json(), r.status_code
        else:

            return {'message': 'Missing authorization token'}, 401

    def request_reviews(self):
        pass
