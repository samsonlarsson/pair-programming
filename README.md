# PEAR
__A Pair Programming Platform App.__

__PEAR__ is a platform that facilitates collaboration for programmers.

## Technology Used

* [Flask micro-framework](http://flask.pocoo.org) to host the web interface.
* [Jinja2](http://jinja.pocoo.org/docs/) to template web pages based on Python objects.
* [Sqlite](https://sqlite.org/) to link the web framework to the SQL database.
* [Pure CSS](http://purecss.io/) to simplify making the pages look ‘pretty.’
* [JavaScript](https://www.javascript.com/) simplified adding handy interface features such as a javascript to integrate the firebase sessions and firepad.
* [Heroku](http://heroku.com/) for a free hosting solution easily managed by git and ssh.
* [Firepad](https://firepad.io) Firepad is an open source real-time collaborative text editor. 
* [Slack](https://api.slack.com/docs/oauth-test-tokens) Slack API testing token


## Main Features
* Allow users to create pair programming session
* Allow users to edit or delete a pair programming session
* Allow users to  invite other users into their pair programming session
* Integrate a real time editor
* Allow users in a pair programming session to chat

## Check it out at a glance
![alt tag](https://raw.githubusercontent.com/samsonpaul/pair-programming/master/app/static/img/test.png)

## Getting your own instance of PEAR app

1. Clone this repository

   `$ git clone https://github.com/samsonpaul/bc-12-pair-programming.git`

2. Install project dependencies via `pip`. It's recommended that you do this in a `virtualenv`

    `$ pip install -r requirements.txt`

3. Initialize your development database.

    `$ python manage.py db init`

4. Construct the database and migrate the database models.

    `$ python manage.py db upgrade`

5. Run a development server.

    `$ python manage.py runserver`

## Curren
* Implementation of slack

## Issues
* When you send an invite, the current user has to copy and paste the link
  manually. One needs to just pick the session link from the url tab.
* When viewing all sessions, the table displays the session unique key instead
  of the session name

## Milestone/Backlog
* Fully intergrate the chat sessions into the app
* Ability to view users who are currently online
* Ability to implement public sessions where one can share publicly
  without authentication.
