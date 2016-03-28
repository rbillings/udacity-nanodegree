# Swiss Style Tournament
This repository shows an example of a Swiss Pairing Tournament. This game system uses the [Swiss system][swiss] for pairing
up players in each round: players are not eliminated, and each player should be paired with another player with the
same number of wins, or as close as possible.

This project fulfills the Swiss Pairs Tournament assignment of the Udacity's [Full-Stack Web Developer Nanodegree.][nano]

## Requirements
You'll need a version of [Python 2.7][python] installed.

You'll need a working [Vagrant][vagrant] virtual environment.

You'll need to have [PostgreSQL][postgresql] installed.


## Clone the project
You will need to clone this repo to get started. If you do not know how to clone a GitHub
repository, check out this [help page][git-clone] from GitHub.

To clone open the working directory location and enter:
```
    $ git clone https://github.com/rbillings/udacity-nanodegree.git
```
Alternately you can download a .zip file here:
```
    https://github.com/rbillings/udacity-nanodegree/archive/master.zip
```
This will give you access to all of the required files and functionality for this project inside
the Swiss Pairs Tournament folder.


## Set up

1. Clone this repository 
2. Get Vagrant up and running
3. Import the tournament.sql file using psql to create and explore the database tables and views
4. Use a python interpreter to run the functions in tournament.py
5. Use a terminal to run the code in test_tournament.py by typing:
```
    $ python test_tournament.py
```

Instructions are for a OSX environment and may vary with different operating systems.

## Learning Resources, License

* Additional learning and help found here:
    * Udacity forums and learning modules
    * http://stackoverflow.com/questions/6454894/reference-an-element-in-a-list-of-tuples/6456580#6456580
    * http://www.w3schools.com/sql/sql_func_count.asp
    * http://stackoverflow.com/questions/9293900/how-to-increment-integer-columns-value-by-1-in-sql
    * http://stackoverflow.com/questions/4501636/creating-sublists
    * http://www.tutorialspoint.com/sql/sql-using-views.htm
    * https://docs.python.org/2/library/functions.html#xrange

* License

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png)](http://creativecommons.org/publicdomain/zero/1.0/)

[swiss]: https://en.wikipedia.org/wiki/Swiss-system_tournament
[nano]: https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004
[python]: https://www.python.org/download/releases/2.7/
[git-clone]: https://help.github.com/articles/cloning-a-repository/
[vagrant]: https://www.vagrantup.com/
[postgresql]: http://www.postgresql.org/download