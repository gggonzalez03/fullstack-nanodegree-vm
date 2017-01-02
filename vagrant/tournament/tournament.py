#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name = "tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        database = psycopg2.connect("dbname={}".format(database_name))
        cursor = database.cursor()
        return database, cursor
    except:
        print("Connection error occured.")


def deleteMatches():
    """Remove all the match records from the database."""
    # delete from matches/standings
    dbconnection, cursor = connect()
    cursor.execute("DELETE FROM MATCH")
    dbconnection.commit()
    dbconnection.close()
    


def deletePlayers():
    """Remove all the player records from the database."""
    # delete from player
    dbconnection, cursor = connect()
    cursor.execute("DELETE FROM PLAYER")
    dbconnection.commit()
    dbconnection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    # select count from player
    dbconnection, cursor = connect()
    cursor.execute("SELECT COUNT(*) FROM PLAYER")

    player_count = cursor.fetchone()[0]
    
    dbconnection.close()

    return player_count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    # insert into players
    dbconnection, cursor = connect()
    cursor.execute("INSERT INTO PLAYER(NAME) VALUES(%s)", (name,))
    dbconnection.commit()
    
    dbconnection.close()
    


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    # select from standing
    dbconnection, cursor = connect()
    cursor.execute("SELECT Player.id, Player.name, "
                   "COALESCE(sv.wins, 0) AS wins, "
                   "COALESCE(sv.losses, 0) + COALESCE(sv.wins, 0) AS matches "
                   "FROM Player "
                   "LEFT JOIN Standings_View AS sv "
                   "ON Player.id = sv.winnerid "
                   "OR Player.id = sv.loserid "
                   "ORDER BY wins DESC, sv.losses ASC")

    player_list = cursor.fetchall()
    
    dbconnection.close()

    return player_list
    


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Insert into standings table
    dbconnection, cursor = connect()
    cursor.execute("INSERT INTO Match(winner, loser) VALUES(%s, %s)", (winner, loser))
    dbconnection.commit()

    dbconnection.close()
 
 
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
    # select from  standings
    # return players who have equal
    # or nearly equal wins
    dbconnection, cursor = connect()
    cursor.execute("SELECT COUNT(*) FROM Match")
    matches = cursor.fetchone()

    # if there is no any rankings yet,
    # randomly set pairs
    if int(matches[0]) == 0:
        match = ()
        matches = []
        cursor.execute("SELECT row_number() OVER(ORDER BY random()) AS row_order, * "
                       "FROM Player")
        random_ordered_players = cursor.fetchall()
        dbconnection.close()

        for(row_number, player_id, player_name) in random_ordered_players:
            if row_number % 2 != 0:
                match += (player_id, player_name)
            else:
                match += (player_id, player_name)
                matches.append(match)
                match = ()
    else:
        match = ()
        matches = []
        count = 1

        player_standings = playerStandings()
        
        for(player_id, player_name, player_wins, player_matches) in player_standings:
            if count % 2 != 0:
                match += (player_id, player_name)
                count += 1
            else:
                match += (player_id, player_name)
                matches.append(match)
                match = ()
                count = 1

    return matches
