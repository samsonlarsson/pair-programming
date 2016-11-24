# PEAR
__A Pair Programming Platform App.__

__PEAR__ is a platform that facilitates collaboration for programmers.

## Main Features
* Allow users to create pair programming session
* Allow users to edit or delete a pair programming session
* Allow users to  invite other users into their pair programming session
* Integrate a real time editor
* Allow users in a pair programming session to chat

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

## Issues
* When you send an invite, the current user has to copy and paste the link
  manually. One needs to just pick the session link from the url tab.
* When viewing all sessions, the table displays the session unique key instead
  of the session name

## Milestone
* Fully intergrate the chat sessions into the app
* Ability to view users who are currently online
* Ability to implement public sessions where one can share publicly
  without authentication.
