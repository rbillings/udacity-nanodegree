#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from contextlib import contextmanager


@contextmanager
def get_cursor():
    """
    Query helper function using context lib. Creates a cursor from a database
    connection object, and performs queries using that cursor.
    """
    DB = connect()
    cursor = DB.cursor()
    try:
        yield cursor
    except:
        raise
    else:
        DB.commit()
    finally:
        cursor.close()
        DB.close()


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        return psycopg2.connect("dbname=tournament")
    except:
        print("Connection failed")


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.

    Args:
      name: the player's full name (need not be unique).
    """
    with get_cursor() as cursor:
        query = 'INSERT INTO players (name) VALUES (%s);'
        cursor.execute(query, (name,))


def countPlayers():
    """Returns the number of players currently registered."""
    with get_cursor() as cursor:
        cursor.execute('SELECT count(*) FROM players;')
        count = cursor.fetchall()
    return count[0][0]


def deletePlayers():
    """Remove all the player records from the database."""
    with get_cursor() as cursor:
        cursor.execute("DELETE FROM players;")


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    """ Update matches table with winner and loser """
    with get_cursor() as cursor:
        query = 'INSERT INTO matches (winner, loser) VALUES (%s, %s);'
        cursor.execute(query, ((winner,), (loser,)))


def deleteMatches():
    """Remove all the match records from the matches table."""
    with get_cursor() as cursor:
        cursor.execute('DELETE FROM matches;')


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    with get_cursor() as cursor:
        query = """SELECT id, name, wins, matches FROM standings_list;"""
        cursor.execute(query)
        standings = cursor.fetchall()
    return standings


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    player = [item[0:2] for item in standings]
    """
    Loop through players from index 0 until index < player count,
    create new pairs and append to Swiss Pair List.
    """
    SwissPairList = []
    for i in xrange(0, countPlayers() , 2): 
        pairs = player[i] + player[i+1]
        SwissPairList.append(pairs)
    return SwissPairList
