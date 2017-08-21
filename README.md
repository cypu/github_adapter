## Github adapter

## About project
This is the web-service which exposes some of github.com's functionalities to its clients. They are exposed via RESTful API and provide:
1. Getting details of followers for given user
1. Creating pull request and requesting reviewers in one time
1. User authentication 

## Project instalation

To setup project it is required to have Docker installed.
Instalation steps:
1. Set up 'test_config' - desribed below
1. Being at project root run in terminal run :  `docker build -t github-adapter .` to build docker image 
1. Run dorcker image with commnand : `docker run -d -p 5000:5000 github-adapter`
1.


## Setting 'test_config'

## Running tests
