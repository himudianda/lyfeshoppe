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

Clone the repo and install all dependencies
-------------------------------------------

- Clone this repo ``https://github.com/himudianda/cheermonk.git``
- Type ``cd cheermonk``
- Activate your virtualenv
- Type ``pip install -r requirements.txt`` to install dependencies
- Type ``pip install --editable .`` to create the Cheermonk.egg-info which helps us easily run console scripts.

Set up docker-compose
---------------------

- Edit ``docker-compose.yml`` and `setup a local volume for Postgres/`__
- Type ``docker-compose pull`` to create a docker image
- Type ``docker-compose up`` to start Postgres

Initialize everything and view the app
--------------------------------------

- Type ``run server debug`` OR ``run server gunicorn`` to start server
- Visit http://localhost:5000 in your browser


How do I shut everything down?
''''''''''''''''''''''''''''''

- Hit CTRL+C a few times to stop everything
- Type ``docker-compose stop`` to ensure all containers are stopped
- Confirm no containers are running by typing ``docker ps``


Apply flake8 fixes
--------------------------------------

- Type ``flake8 cheermonk`` to list all PEP8 & python lint errors


About the author
^^^^^^^^^^^^^^^^

- Harshit Imudianda | | `GitHub <https://github.com/himudianda>`_
