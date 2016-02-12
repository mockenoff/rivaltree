# rivaltree
-----------

Let's make a bracket app.

## Structure

Most of this is just a Django app, but there is also a self-contained Ember app called `tourf`. The idea is that any non-bracket stuff is all inside Django and served through its usual views/templating stuff with `apps.account` and the `/templates/` directory.

Then the dashboard stuff is all Ember interfacing with the Django-driven API through `apps.bracketr`. A consequence is that any static assets will get thrown into `/tourf/public/` and then get built into the `.gitignore`'d `/static/` directory but will also be used for the Django stuff pages.

## Ember Setup

From the outset, you'll need `Node > v4.2.1`, so install that however you need to [install it](https://nodejs.org/en/download/package-manager/).

```
$ npm install -g ember-cli
$ npm install -g bower
$ brew install watchman # https://facebook.github.io/watchman/docs/install.html
```

You'll also need to make sure `which mysql_config` does _something_ so that `pip install` doesn't blow up on `mysqlclient`. (This means `brew install mysql` on OS X.)

```
$ cd /rivaltree/tourf/
$ npm install
$ bower install
```

## Django Setup

The only dependency is `Python > v3.4.2`. Also something with `MySQL` so that `pip install` doesn't blow up on `mysqlclient`.

```
$ brew install python3
$ pyenv virtualenv --python=/usr/local/bin/python3 rivaltree
```

```
$ cd /rivaltree/
$ pip install -r requirements.txt
```

## Local development

The best way to go about running these things is to run the Django server and the Ember server simultaneously even though you'll only be accessing the Django app. This is so Ember's watcher will continually build its changes as needed and then you'll just have to refresh your browser.

```
$ python manage.py runserver
$ cd tourf/
$ ember s --output-path ../static/ --live-reload=false
```
