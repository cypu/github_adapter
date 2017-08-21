"""
Project configuration.
"""


class Config(object):

    #  Github Api settings
    GITHUB_API_USER_DETAILS = "https://api.github.com/users/{}"
    GITHUB_API_USER_FOLLOWERS = "https://api.github.com/users/{}/followers"
    GITHUB_API_CREATE_PULL_REQUEST = "https://api.github.com/repos/{owner}/{repos}/pulls"
    GITHUB_API_CREATE_REVIEW_REQUEST = "https://api.github.com/repos/{owner}/{repo}/pulls/{number}/requested_reviewers"
    GITHUB_USER_LOGIN_ENDPOINT = "https://api.github.com/user"
    GITHUB_API_UPDATE_PULL_REQUEST = "https://api.github.com/repos/{owner}/{repo}/pulls/{number}"


class TestConfig(Config):
    TESTING = True
