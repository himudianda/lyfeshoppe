# Use the barebones version of Python 2.7.10.
MAINTAINER Harshit Imudianda <harshit.himudianda@gmail.com>

# Install any packages that must be installed.
RUN apt-get update && apt-get install -qq -y build-essential libpq-dev postgresql-client-9.4 --fix-missing --no-install-recommends

# Setup the install path for this service.
ENV INSTALL_PATH /cheermonk
RUN mkdir -p $INSTALL_PATH

# Update the workdir to be where our app is installed.
WORKDIR $INSTALL_PATH

# Ensure packages are cached and only get updated when necessary.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Give access to the CLI script.
RUN pip install --editable .

# The default command to run if no command is specified.
CMD gunicorn -b 0.0.0.0:8000 "cheermonk.app:create_app()"
