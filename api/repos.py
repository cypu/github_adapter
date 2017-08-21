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

    REQUIRED_ARGUMENTS = ('changeset', 'repository', 'title', 'base', 'reviewers')

    def post(self):
        """
        
        :return: 
        """
        # branch name
        # full repository name format : 'owner/repo_name'
        parser = reqparse.RequestParser()
        [parser.add_argument(arg) for arg in self.REQUIRED_ARGUMENTS]
        parser.add_argument('token')
        args = parser.parse_args()

        if not args.get('token'):
            return {'message': 'Missing authorization token'}, 401

        if all(args.get(key) for key in self.REQUIRED_ARGUMENTS):
            repo_owner, repo_name = args['repository'].split('/')

            post_data = {"title": args.get('title'),
                         "body": args.get('body') or "This is a pull request.",
                         "head": '{}:{}'.format(repo_owner, args['changeset']),
                         # Regards to Github API documentation, changeset is the branch name
                         "base": args.get('base')}

            headers = {'Authorization': 'Basic ' + args.get('token')}
            r = requests.post(app.config['GITHUB_API_CREATE_PULL_REQUEST'].format(owner=repo_owner, repos=repo_name),
                              data=json.dumps(post_data), headers=headers)

            if r.status_code == requests.codes.ok:
                # request the reviews to reviewers
                pass

            return r.json(), r.status_code
        else:

            missing_args = set(self.REQUIRED_ARGUMENTS) - {key for key in args.keys() if args.get(key)}
            return {'message': 'Missing required arguments : ' + ','.join(sorted(list(missing_args)))}, 422

    def request_reviews(self):
        pass
