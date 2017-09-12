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
`pip3 install -r requirements.txt`
and
`python3 run.py`

## API endpoints

This adapter provide endpoints described below :

1. `/users/followers/<string:user>`

    Allows user to get details of its followers.
    
    It is accesable via GET reqest and there are optional pagination params `page` and `per_page`

1. `/users/login/`
    
    Allows user to get authentication TOKEN
    
    It is accesable via POST request and user need to provide `login` and `password`
1. `/repos/create_pull_request/`  

    Allows user to create a pull request and request reviews to reviewers
    
    It is accesable via POST request and all required parameteers are described here https://developer.github.com/v3/pulls/#create-a-pull-request
    
    Moreover it also requires auth TOKEN
    

## Setting 'test_config'
test_config file is should contain data related to github account testing
Each line must contain `key:value` structure.
Mandatory keys : `login` , `password`, `repository`, `reviewers`

Example: 

`login:mylogin`

`password:mypassword`

`repository:myrepository`

`branch:mybranch`

`reviewers:reviewer1,reviewer2,reviewer3`

Please note that reviewers is a CSV structure
And branch should contain changes compared to master


## Running tests

When you install project locally :
`pytest`

Please remember to have changes on your branch, because system does not create them for tests.
It is also required to run this command from the root of project.

It is also possible to run test via docker : 

1. `docker exec -i -t <container_id> /bin/bash`
1. `pytest`

Remeber that you need to create your test_config firstly befor you build the docker image.

## Other notes

This application requires to set it on HTTPS server to be more safe.
I also tried set memcache for caching responses with followers details.
I think it also may improve speed of response in some cases.

I am also aware that in complete solution there should be more tests covering edge cases and exception handling in API endpoints.
I hope that implemented tests cover basic functionality of github_adapter and are enough to present how that adapter works.


