# Acute Commute
## Solving the first / last mile problem for travelers and commuters
Google Maps and other apps that recommend routes based on start and end location tend to fail when the middle leg of the trip involves public transit. Getting to and from the endpoints of the public transit route is known as the first mile last mile problem. By default, Google only gives walking as an option to get to and from a transit stop. Our application considers all forms of travel to and from the transit stops to provide additional options and give the shortest possible travel time for the trip.

## Deployed Instance
http://ec2-34-205-89-106.compute-1.amazonaws.com/

## File Breakdown
### Front-end
- /static/index.html
  - served by the **root** url for the deployed website
  - contains an html form that the user can interact with
- /static/index.js
  - overrides the default submission of the html form
  - handles animation between the submission of the form and the given response
  - requests a json response from the server based on the given form
  - updates html json response has come back from the server

### Back-end
- /server.py
  - interface between the web front-end and backend logic
  - flask handles root route with html response
  - flask handles a post request for /trip route w/ a search
- /requirements.txt
  - installs all necessary python libraries
- Dockerfile
  - creates a docker image for deployment to AWS


## Install Dependencies
```bash
$ pip install -r requirements.txt
```

## Deployment
```bash
# install front-end dependencies
$ cd static
$ bower install
$ cd ..

# setup a docker aws instance
# REQUIRES AWS CREDENTIALS
$ docker-machine create --driver amazonec2 acute
$ eval $(docker-machine env acute)

# build the image & run in a container
$ docker build -t acute .
# -d flag for detached
$ docker run --name acute -p 80:80 -d acute

# requires correct security-group permissions
# on AWS but should be able to use at this point
```

## Team
* Connor Ameres - cameres@usfca.edu
* Cameron Carlin - cscarlin@usfca.edu
* Melanie Palmer - mapalmer2@usfca.edu
* Will Young - wjyoung@usfca.edu
# wjyoung-viz
