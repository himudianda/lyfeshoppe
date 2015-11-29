Unreleased
^^^^^^^^^^^^^^^^^^^^^^^^^^
- All Admin pages styled to dashboard theme


Version 0.4 (2015-11-27)
^^^^^^^^^^^^^^^^^^^^^^^^^^
- Admin dashboard now has ability to view all Businesses & Products
- You can also bulk delete, edit & add new products/businesses from the admin view


Version 0.3 (2015-11-26)
^^^^^^^^^^^^^^^^^^^^^^^^^^
- Modified all the to-be-used views of Cheermonk to either dashboard or frontend theme layout.
- Extensive frontend work - login, signup, home, FAQs, Support etc pages are all modified with new layout.
- Surfing through Cheermonk should give a nice monolithic experience.


Version 0.2 (2015-11-21)
^^^^^^^^^^^^^^^^^^^^^^^^^^
- Added 2 new themes for frontend & dashboard
- Added sample templates & views for the dashboard & frontend theme demos.
- These themes were transformed using cheermonk_private/scripts/transform_themes.py version 0.1


Version 0.1 (2015-11-14)
^^^^^^^^^^^^^^^^^^^^^^^^^^
- Major features & infrastructure work has been implemented as follows.

Features:
- Implemented User roles, subscriptions, Issue tracking, Coupons, Credit Card Handling, etc.
- Stripe API used for billing
- All subscribed users can receive tweets about cats :)
- Unit Tests have been implemented for testing core features.
- Issue tracking & support has also been added & can be viewed on Admin interface
- Tools like flower, cAdvisor used for better system tracking.

Packages:
- Flask-Mail used to send out emails
- Redis is used for multiple things: pub-sub part in websocket server, to back celery & to back flask-cache as the backend.
- Celery is the background task queue & Flower is the front end to view celery tasks
- Flask-Cache helps caching an entire flask view OR a jinja2 snippet.
- flask-bouncer is used for handling permissions - i.e. showing diff data for different User roles
- Subscription service implemented using Stripe APIs
- Tweepy is used for getting realtime tweets
- Unit Tests implemented using pytest, pytest-cov does coverage testing
- mock is used to mock the stripe APIs for our test
- fake-factory package used Faker underneath to generate fake data
- Flask-DebugToolbar is super useful - helps figure whats happening under the hood in your app.


Version 0.0.4 (2015-11-13)
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Added CSRF protection.
- Added styles, fonts, images - beautified the frontend pages
- Added more frontend pages - faq, terms, privacy, learnmore etc.
- Implemented User models with complete user authentication - signup, login, password reset, change credentials etc
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
