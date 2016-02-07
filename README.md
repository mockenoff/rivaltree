# rivaltree
-----------

Let's make a bracket app.

## Structure

Most of this is just a Django app, but there is also a self-contained Ember app called `tourf`. The idea is that any non-bracket stuff is all inside Django and served through its usual views/templating stuff with `apps.account` and the `/templates/` directory.

Then the dashboard stuff is all Ember interfacing with the Django-driven API through `apps.bracketr`. A consequence is that any static assets will get thrown into `/tourf/public/` and then get built into the `.gitignore`'d `/static/` directory but will also be used for the Django stuff pages.

## Local development

The best way to go about running these things is to run the Django server and the Ember server simultanously even though you'll only be accessing the Django app. This is so Ember's watcher will continually build its changes as needed and then you'll just have to refresh your browser.

```bash
$ python manage.py runserver
$ cd tourf/
$ ember s --output-path ../static/ --live-reload=false
```