from os import stat
import psycopg2
import re
from datetime import datetime, timedelta
import sys


def connect_to_db():
    """
    Connects to the database and returns a connection object.
    """
    return psycopg2.connect(
        database="Contact_Tracing_DB",
        user="postgres",
        password="password",
        host="34.134.212.102",
    )


# check email format
def validate_email_format(email: str):
    regex = "^[A-Za-z0-9]+[\._]?[A-Za-z0-9]+[@]\w+[.]\w{2,3}$"

    return re.search(regex, email) != None


def _execute_statement(conn, statement):
    """
    Executes a PSQL statement with a given connection.

    Returns a cursor with the response of the statement.
    """
    cursor = conn.cursor()
    cursor.execute(statement)
    conn.commit()

    return cursor


#retreives records for every scan made
def retrieve_records(limit:int,conn):

    if(limit != 0):
        statement = f"SELECT * FROM scans ORDER BY scan_time LIMIT '{limit}'"
    else:
        statement = "SELECT * FROM scans" 
     
    #cursor
    cur = _execute_statement(conn, statement)
    
    #executing SQL statement failed
    if(cur == None):
        raise LookupError("Error occured while executing the SQL statement")
    
    #fetch query results
    result = cur.fetchall()
    
    cur.close()

    return result

#retreives records for every scan made by a specific user
def retrieve_user_records(email:str,limit:int,conn):

    if not validate_email_format(email):
        return -1
    
    if(limit != 0):
        statement = f"SELECT * FROM scans WHERE person_email = '{email}' ORDER BY scan_time LIMIT '{limit}'"
    else:
        statement = f"SELECT * FROM scans WHERE person_email = '{email}'"

    #cursor
    cur = _execute_statement(conn, statement)
    
    #executing SQL statement failed
    if(cur == None):
        raise LookupError("Error occured while executing the SQL statement")
    
    #fetch query results
    result = cur.fetchall()
    
    cur.close()

    return result



#Retrieve people who were in contact with the person reporting a positive covid test
def retrieve_contacts(email:str,date:datetime,conn):

    #validate email format
    if not validate_email_format(email):
        return -1
    
    #validate that the passed in date is no more than 14 days before today's date
    if(datetime.now() - date > timedelta(days=14)):
        return -1 

    #query all the students the infected student has been in contact with 
    cur = _execute_statement(conn, f"""
        WITH rooms_attended AS(
            SELECT room_id,scan_time
            FROM scans
            WHERE scan_time > TIMESTAMP'{date}' - INTERVAL'7 days' AND person_email = '{email}'
        )
        SELECT scans.*
        FROM rooms_attended, scans
        WHERE scans.person_email != '{email}' AND scans.room_id = rooms_attended.room_id AND (scans.scan_time BETWEEN rooms_attended.scan_time - INTERVAL'1 hour' AND rooms_attended.scan_time + INTERVAL'1 hour'); 
    """) 

    #list of contacts 
    contacts = cur.fetchall()
    
    cur.close()

    return contacts

#retreive all people and the amount of scans they have
def get_people(conn):

    cur = _execute_statement(conn, 
        f"""SELECT email,name,student_id,
        (
            SELECT COUNT(*)
            FROM scans
            WHERE scans.person_email = people.email 
        )
        FROM people 
        """)

    if cur is None:
        raise LookupError("Error occured while executing the SQL statement")
    
    result = cur.fetchall()

    cur.close()

    return result

#retreive records count
def get_records_count(conn):

    cur = _execute_statement(conn, f"SELECT COUNT(*) FROM scans")

    if cur is None:
        raise LookupError("Error occured while executing the SQL statement")
    
    result = cur.fetchone()

    cur.close()

    return result[0]

#retreives room id, capacity, building, count of unique students that have scanned in the room, and the total number of scans that happened in the room 
def get_rooms(conn):

    cur = _execute_statement(conn, 
    f"""
        SELECT *,
        (
            SELECT COUNT (DISTINCT person_email)
            FROM scans
            WHERE room_id = rooms.room_id
        ),
        (
            SELECT COUNT(*)
            FROM scans
            WHERE room_id = rooms.room_id
        )
        
        FROM rooms
    """)
    
    if cur is None:
        raise LookupError("Error occured while executing the SQL statement")
    # room row
    result = cur.fetchall()

    return result

#retreives building name, # of rooms in that building, # of scans that has been made in that building, and the total number of unique students that scanned in that building 
def get_buildings(conn):

    cur = _execute_statement(conn, 
    f"""
        SELECT DISTINCT building_name,
        (
            SELECT COUNT (*)
            FROM rooms AS rooms_2
            WHERE rooms_2.building_name = rooms_1.building_name
        ),
        (
            SELECT COUNT(*)
            FROM scans AS scans_1, rooms AS rooms_3
            WHERE scans_1.room_id = rooms_3.room_id AND rooms_1.building_name = rooms_3.building_name
        ),
        (
            SELECT COUNT(DISTINCT person_email)
            FROM scans as scans_2, rooms AS rooms_4
            WHERE scans_2.room_id = rooms_4.room_id AND rooms_1.building_name = rooms_4.building_name
        )
        
        FROM rooms AS rooms_1
    """)
    
    if cur is None:
        raise LookupError("Error occured while executing the SQL statement")
    # room row
    result = cur.fetchall()

    return result    
    
