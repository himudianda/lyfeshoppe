Unreleased
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Error templates - 404, 500 & 502 are served from build/public directory

Version 0.0.3 (2015-11-12)
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Used Flask-Webpack to bundle all assets together.
- Very basic Jinja2 Templating done - used template inheritance & macros.
- Wrote the CHANGES.rst file

Version 0.0.2 (2015-11-10)
^^^^^^^^^^^^^^^^^^^^^^^^^^

- App now supports PostgreSQL database. The DB runs under a docker container
- gunicorn used to run the app & honcho Procfile used for automation.

Version 0.0.1 (2015-11-08)
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Bootstrapped a simple Flask App with CLI
