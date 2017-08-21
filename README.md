## Github adapter

## About project
This is the web-service which exposes some of github.com's functionalities to its clients. They are exposed via RESTful API and provide:
1. Getting details of followers for given user
1. Creating pull request and requesting reviewers in one time
1. User authentication 

## Project installation

To setup project it is required to have Docker installed.
Installation steps:
1. Set up 'test_config' - desribed below
1. Being at project root run in terminal run :  `docker build -t github-adapter .` to build docker image 
1. Run docker image with commnand : `docker run -d -p 5000:5000 github-adapter`

Alternatively it is possible to install project locally through:
pip3 install -r requirements.txt


## Setting 'test_config'
test_config file is should contain data related to github account testing
Each line must contain `key:value` structure.
Mandatory keys : `login` , `password`, `repository`, `reviewers`

Example:
`login:mylogin
password:mypassword
repository:myrepository
branch:mybranch
reviewers:reviewer1,reviewer2,reviewer3`

Please note that reviewers is a CSV structure
And branch should contain changes compared to master


## Running tests

When you install project locally :
`python3 run_test.py'

Please remember to have changes on your branch, because system does not create them for tests.
It is also required to run this command from the root of project.

## Other notes

This application requires to set it on HTTPS server to be more safe.
I also tried set memcache for caching responses with followers details.
I think it also may improve speed of response in some cases.


