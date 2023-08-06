Web radio expandable collection
---
 * organize your web radios, delete and update 
 * upload your favorite pictures and comments to the local SQLite database
 * this guy is a REST API application on blueprints and app factory of the flask framework
 * Android: download to mobile (link below .-apk), rename *WHL to *ZIP, extract with Android _file_ manager
 * https://pypi.org/project/eisenradio-apk/ , uses Python Kivy library for multi-touch on start-up `https://pypi.org/project/Kivy/#files`
 * Linux SNAP user find uninstall information at the bottom
 
pip install
-
	""" xxs Linux xxs """
    $ pip3 install eisenradio
    $ python3 -m eisenradio.wsgi  # watch flask

    """ xxm Windows xxm """
    > pip install eisenradio
    > python -m eisenradio.wsgi

    """ xxl big company xxl """
    $$$ pip3 install eisenradio
    $$$ python3 -m eisenradio.app  # serve flask
    """ for the sake of completeness, a python
        production server 'waitress' is started """
---
Pytest
---
> ~ ... /test/functional$ python3 -m pytest -s    # -s print to console

find the modified test db in ./app_writable/db

Uninstall
---
Python user:

* find module location
* uninstall and then remove remnants

>$ pip3 show eisenradio

>$ pip3 uninstall eisenradio

Location: ... /python310/site-packages

Android user:
* press long (select) the icon, uninstall



SNAP user:

* remove the snap
* delete the database folder in their home; on startup shown in [SNAP_USER_COMMON] 
>SNAP_USER_COMMON (your Database lives here, backup if you like): /home/osboxes/snap/eisenradio/common

You only want a fresh database? Remove the database. Start from scratch.