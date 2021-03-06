"""
API endpoints related to repositories.
"""

import requests
import json
from flask_restful import Resource, reqparse
import flask


class CreatePullRequestWithReviews(Resource):
    """
    Provide the ability to create pull request with requesting reviews.
    """

    REQUIRED_ARGUMENTS = ('changeset', 'repository', 'title', 'base', 'reviewers')

    def post(self):
        """Handler of POST resquest for creating pull request.
        
        :return: JSON with data , status code
        """
        parser = reqparse.RequestParser()
        for arg in self.REQUIRED_ARGUMENTS:
            parser.add_argument(arg)
        parser.add_argument('token')  # token is also required but it is checking separately
        args = parser.parse_args()

        if not args.get('token'):
            return {'message': 'Missing authorization token'}, 401

        if all(args.get(key) for key in self.REQUIRED_ARGUMENTS):
            repo_owner, repo_name = args['repository'].split('/')  # full repository name format : 'owner/repo_name'

            post_data = {"title": args.get('title'),
                         "body": args.get('body') or "This is a pull request.",
                         "head": '{}:{}'.format(repo_owner, args['changeset']),
                         # Regards to Github API documentation, changeset is the branch name
                         "base": args.get('base')}

            headers = {'Authorization': 'Basic ' + args.get('token')}
            r = requests.post(flask.current_app.config['GITHUB_API_CREATE_PULL_REQUEST'].format(owner=repo_owner, repos=repo_name),
                              data=json.dumps(post_data), headers=headers)

            if r.status_code == 201:
                number = r.json().get('number')
                resp = self._request_reviews(args.get('token'), repo_owner, repo_name, number, args.get('reviewers'))

                return resp.json(), r.status_code

            return r.json(), r.status_code
        else:
            missing_args = set(self.REQUIRED_ARGUMENTS) - {key for key in args.keys() if args.get(key)}
            return {'message': 'Missing required arguments : ' + ','.join(sorted(list(missing_args)))}, 422

    def _request_reviews(self, token, owner, repo, number, reviewers):
        """Method responsible for requesting pull request review to reviewers.
        
        :param token: Authentication token
        :param owner: repository owner
        :param repo: repository name
        :param number: number of pull request
        :param reviewers: reviewers (CSV format)
        :return: HTTP response object
        """
        post_data = {'reviewers': reviewers.split(',')}
        headers = {'Authorization': 'Basic ' + token}
        response = requests.post(
            flask.current_app.config['GITHUB_API_CREATE_REVIEW_REQUEST'].format(owner=owner, repo=repo, number=number),
            data=json.dumps(post_data), headers=headers)

        return response
