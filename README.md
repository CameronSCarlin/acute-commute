# Acute Commute
## Solving the first / last mile problem for travelers and commuters
Google Maps and other apps that recommend routes based on start and end location tend to fail when the middle leg of the trip involves public transit. Getting to and from the endpoints of the public transit route is known as the first mile last mile problem. By default, Google only gives walking as an option to get to and from a transit stop. Our application considers all forms of travel to and from the transit stops to provide additional options and give the shortest possible travel time for the trip.

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
$ docker-machine create --driver amazonec2 aws-docker
$ eval $(docker-machine env aws-docker)

# build the image & run in a container
$ docker build -t acute .
$ docker run --name acute -p 80:80 acute

# requires correct security-group permissions
# on AWS but should be able to use at this point
```

## Team
* Connor Ameres - cameres@usfca.edu
* Cameron Carlin - cscarlin@usfca.edu
* Melanie Palmer - mapalmer2@usfca.edu
* Will Young - wjyoung@usfca.edu
# wjyoung-viz
