python_webapp
=============

Generic Docker image for Python Flask webapp.

Installs Python 2.7, Flask and Apache. Virtualenv is intentionally avoided - 
Docker is used to encapsulate python version and dependencies. 

The app will be available on port 5000 in the docker container - this is
expected to be mapped to port 80 on the host. If you want to run on port 80,
just edit the Dockerfile.
