import os
import mysql.connector
from mysql.connector.connection import MySQLConnectionAbstract
from mysql.connector import Error as DB_error
from dotenv import load_dotenv
from pathlib import Path

connection: MySQLConnectionAbstract


def create_database_connection() -> None | DB_error:
    """
    Establishes connection to the database using environment variables.

    :returns: None if connection is established successfully and mysql.connector.Error if error occur
    """

    dotenv_path = Path('./config/.env')
    load_dotenv(dotenv_path=dotenv_path)

    try:
        global connection
        
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_DATABASE'),
            port=os.getenv('DB_PORT'),
            username=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            autocommit=bool(os.getenv('DB_AUTOCOMMIT'))
        )

        return None
    except DB_error as error:
        return error


def fetch_10_random_airports_from_db() -> list | DB_error:
    """
    Fetches 10 random airports from database.

    :returns: List of airports as tuples or mysql.connector.Error if the database fetch fails
    :rtype: [(string, string, float, float)] or DB_error
    """

    sql = ("SELECT airport.name, country.name, airport.latitude_deg, airport.longitude_deg "
           "FROM airport, country WHERE airport.iso_country = country.iso_country AND NOT airport.ident = 'EFHK' "
           "ORDER BY RAND() LIMIT 10")
    # The 'AND NOT airport.ident' is used to strip 'Helsinki Vantaa Airport'
    # out of the query, because it is the start airport

    cursor = connection.cursor()

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

        return result

    except DB_error as error:
        return error


def fetch_10_random_parcels_from_db() -> list | DB_error:
    """
    Fetches 10 random parcels from database.

    :returns: List of parcels as tuple or mysql.connector.Error if the database fetch fails
    :rtype: [(string, int, int, string)] or DB_error
    """

    sql = "SELECT item, item_co2, item_type, item_info FROM parcel ORDER BY RAND() LIMIT 10"

    cursor = connection.cursor()

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

        return result

    except DB_error as error:
        return error


def fetch_last_game_id_from_db() -> int | DB_error:
    """
    Fetches the last stored game_id from the database

    :returns: Last stored game_id from database or mysql.connector.Error if the last game_id cannot be fetched from the
    database
    :rtype: int or DB_error
    """

    sql = "SELECT MAX(game_id) FROM highscore"

    cursor = connection.cursor()

    try:
        cursor.execute(sql)
        result = cursor.fetchone()

        if result[0]:
            return result[0]    # Get the int value out from the result tuple
        else:
            return 0    # This happens on the first running time, because no highscore is stored to database yet

    except DB_error as error:
        return error


def insert_new_player_scores_in_to_db(players: list[dict]) -> None | KeyError | DB_error:
    """
    Insert new player scores in to the database

    :param players: List of player dictionaries
    :type players: list[dict]
    :returns: None if inserting is successful, KeyError If the given dictionary doesn't contain needed key and
    mysql.connector.Error If the database insert fails or the last game_id couldn't be fetched
    :rtype: None or KeyError or DB_error
    """

    cursor = connection.cursor()

    try:
        last_game_id = fetch_last_game_id_from_db()

        if type(last_game_id) is not int:
            # Check if error had occur in the fetch_last_game_id_from_db().
            # In case of an error the error is returned to the caller
            return last_game_id

        current_game_id = last_game_id + 1  # If the last game_id fetch was successful then add +1 to it
        for player in players:
            sql = (f"INSERT INTO highscore (game_id, player_name, player_highscore) "
                   f"VALUES ({current_game_id}, '{player['name']}', {player['score']})")

            cursor.execute(sql)

        connection.commit()  # Commit the transaction. (Makes sure that the just inserted values will be stored permanently)

        return None
    except KeyError as error:
        return error
    except DB_error as error:
        return error


def fetch_player_highscores_from_db(count: int) -> list | DB_error:
    """
    Fetch top highscores from database.

    :param count: Specifies how many highscores wanted (query limit).
    :type count: int
    :return: List of highscores or mysql.connector.Error if any error occur in the fetch
    :rtype: [(int, string, int)] or DB_error
    """

    sql = f"SELECT game_id, player_name, player_highscore FROM highscore ORDER BY player_highscore DESC LIMIT {count}"

    cursor = connection.cursor()

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

        return result

    except DB_error as error:
        return error
