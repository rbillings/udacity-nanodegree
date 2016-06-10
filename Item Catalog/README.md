# Item Catalog

This repository contains code for the Udacity Fullstack Web Developer Nanodegree. This project contains a fully functional full-stack python web app.
The project contains elements of Flask, Vagrant, HTML, CSS, and more. The goal was to have a fully functioning app that utilizes
OAuth, and CRUD functionality.

This project contains a list of different plant families, which include a description, image and which hemisphere they live in. Users are able to explore
the families and see a sample of plants belonging to them. Users can authenticate using Google+ or Facebook to create their own Plant Families and Plants.

This project fulfills the Item Catalog assignment of the Udacity's [Full-Stack Web Developer Nanodegree.][nano]

## Requirements
You'll need a version of each of these installed:

* [Python 2.7][python]

* [Vagrant][vagrant] 

* [PostgreSQL][postgresql] 

* You will also need to have SQLAlchemy and Flask-Uploads. If they are not installed they can be installed using "pip install".

## Clone the project
You will need to clone this repo to get started. If you do not know how to clone a GitHub
repository, check out this [help page][git-clone] from GitHub.

To clone, open the working directory location and enter:
```
    $ git clone https://github.com/rbillings/udacity-nanodegree.git
```
Alternately you can download a .zip file here:
```
    https://github.com/rbillings/udacity-nanodegree/archive/master.zip
```
This will give you access to all of the required files and functionality for this project inside
the Item Catalog folder.

## Set up
You will need to open a terminal, and navigate to the Item-Catalog project folder where the Vagranfile exists. Then
you will need to enter the following commands to get vagrant up and running:

```
vagrant up
vagrant ssh
cd /vagrant
```

At this point it will be necessary to create the database and then populate it with pre-loaded data. After
that you can start the web application running and interact with it on your local instance. You can do all
of this by entering the following commands:

```
python plants_db_setup.py
python plant_list.py
python plants_project.py
```

Open **http://localhost:8000/** in your browser, and start exploring the Plant Application website!

## Learning Resources, License

* Additional learning and help found here:
    * Udacity forums and learning modules
    * http://www.w3schools.com/ for help with HTML and CSS
    * http://stackoverflow.com/ for questions on how to align CSS, upload photos, OAuth info for Facebook
    * https://www.youtube.com/watch?v=Exf8RbgKmhM A great tutorial on Flask-Upload!
    * https://pythonhosted.org/Flask-Uploads/ The official source for Flask-Uploads

* License
[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png)](http://creativecommons.org/publicdomain/zero/1.0/)

* Images are all from https://commons.wikimedia.org with CC licenses

[nano]: https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004
[python]: https://www.python.org/download/releases/2.7/
[git-clone]: https://help.github.com/articles/cloning-a-repository/
[vagrant]: https://www.vagrantup.com/
[postgresql]: http://www.postgresql.org/download
