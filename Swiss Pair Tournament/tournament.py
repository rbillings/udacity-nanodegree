#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    query = 'INSERT INTO players (name, wins, matches) VALUES (%s, 0, 0);'
    cursor.execute(query, (name,))
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    query = 'SELECT count(*) from players;'
    cursor.execute(query)
    count = cursor.fetchall()
    db.commit()
    db.close()
    return count[0][0]


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    query = 'DELETE FROM players;'
    cursor.execute(query)
    db.commit()
    db.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    """ Update matches table with winner and loser """
    db = connect()
    cursor = db.cursor()

    query = 'INSERT INTO matches (winner, loser) VALUES (%s, %s);'
    cursor.execute(query, ((winner,), (loser,)))

    """ Increment wins for winner in players table """
    query = 'UPDATE players SET wins = wins + 1 WHERE id = (%s);'
    cursor.execute(query, (winner,))

    """ Increment matches for both winner and loser in players table """
    query = 'UPDATE players SET matches = matches + 1 WHERE id = (%s);'
    cursor.execute(query, (winner,))

    query = 'UPDATE players SET matches = matches + 1 WHERE id = (%s);'
    cursor.execute(query, (loser,))

    db.commit()
    db.close()


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    query = 'DELETE from matches;'
    cursor.execute(query)
    db.commit()
    db.close()


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

    db = connect()
    cursor = db.cursor()
    query = 'SELECT * FROM players ORDER BY players.wins DESC, players.matches ASC;'
    cursor.execute(query)
    standings = cursor.fetchall()
    db.commit()
    db.close()
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
    i = 0
    c = countPlayers()
    while i < c:
        pairs = player[i] + player[i+1]
        SwissPairList.append(pairs)
        i = i+2
    return SwissPairList
