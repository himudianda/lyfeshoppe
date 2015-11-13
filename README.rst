What is this project?
^^^^^^^^^^^^^^^^^^^^^

CheerMonk


Installation instructions
^^^^^^^^^^^^^^^^^^^^^^^^^

Install Virtualenv
''''''''''''''''''

- https://virtualenv.pypa.io/en/latest/installation.html

Install Docker
''''''''''''''

- https://docs.docker.com/installation (docker itself)
- https://github.com/docker/compose/releases (docker-compose tool for development)

Make sure you get ``docker-compose v1.4.0+``.

Install nodejs
''''''''''''''

- https://nodejs.org/download/ (runtime dependency for assets)


Clone the repo and install all dependencies
-------------------------------------------

- Clone this repo ``https://github.com/himudianda/cheermonk.git``
- Type ``cd cheermonk``
- Activate your virtualenv
- Type ``pip install -r requirements.txt`` to install dependencies
- Type ``pip install --editable .`` to create the Cheermonk.egg-info which helps us easily run console scripts.
- Type ``npm install`` to install the asset dependencies


Set up docker-compose
---------------------

- Edit ``docker-compose.yml`` and `setup a local volume for Postgres/`__
- Type ``docker-compose pull`` to create a docker image
- Type ``docker-compose up`` to start Postgres

Initialize everything and view the app
--------------------------------------

- Type ``run assets build`` to create the build directory and manifest file
- Type ``run`` to see a list of what's available
- Type ``run db reset cheermonk cheermonk_test`` to initialize the databases
- Type ``run server gunicorn`` OR ``run server debug`` to start server
- Visit http://localhost:5000 in your browser
- If you wish to login, email: ``dev@localhost.com`` / password: ``password``

How do I shut everything down?
''''''''''''''''''''''''''''''

- Hit CTRL+C a few times to stop everything
- Type ``docker-compose stop`` to ensure all containers are stopped
- Confirm no containers are running by typing ``docker ps``


Can I quickly change my schema without migrating?
'''''''''''''''''''''''''''''''''''''''''''''''''

Yep, just be warned that this will completely purge your database but doing
this early on in development can sometimes be reasonable while you tinker with
your schema very frequently.

- Shut everything down
- Type ``docker-compose run postgres``
- Type ``run db reset cheermonk cheermonk_test``
- Type ``run add all``

This will drop your database, create a new one and seed it with fake data.


Apply flake8 fixes
--------------------------------------

- Type ``flake8 cheermonk`` to list all PEP8 & python lint errors


About the author
^^^^^^^^^^^^^^^^

- Harshit Imudianda | | `GitHub <https://github.com/himudianda>`_
