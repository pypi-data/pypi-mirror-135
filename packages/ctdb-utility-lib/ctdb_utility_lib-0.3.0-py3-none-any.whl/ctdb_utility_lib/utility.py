import psycopg2
import re
from datetime import datetime


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


def batch_add_people(conn, people: list):
    pass


def _execute_statement(conn, statement):
    """
    Executes a PSQL statement with a given connection.

    Returns a cursor with the response of the statement.
    """
    cursor = conn.cursor()
    cursor.execute(statement)
    conn.commit()

    return cursor


# add a scan to the scans table in db
# returns errro message in case of an invalid email format
# throws exception in case of error accessing db
def add_scan(email: str, room_id: str, conn):

    # Invalid email format
    if not validate_email_format(email):
        return -1

    # create current datetime obj
    current_date_time = datetime.now()

    # add scan info to scans table
    cur = _execute_statement(
        conn,
        f"INSERT INTO scans (scan_id, person_email,scan_time,room_id) \
            VALUES (DEFAULT,'{email}',TIMESTAMP '{current_date_time}','{room_id}')",
    )

    # success
    return 0


# retrieves scan info
# returns -1 if no match found
def get_scan(scan_id: int, conn):

    cur = _execute_statement(conn, f"SELECT * FROM scans WHERE scan_id = '{scan_id}'")

    result = cur.fetchone()

    cur.close()

    return result


# Checks if a person with the specified email exists in the people table
def exists_in_people(email: str, conn):

    cur = _execute_statement(conn, f"SELECT COUNT(*) FROM PEOPLE WHERE email = '{email}'")
    result = cur.fetchone()

    # person exists in people table
    if result[0] != 0:
        return True
    # person doesn't exist in people table
    else:
        return False


# add person to people table
def add_person(first: str, last: str, id: int, conn):

    # generate email
    email = first + last + str(datetime.now().timestamp()) + "@fake.com"

    # person exists in the people table
    if exists_in_people(email, conn):
        return None

    name = first + " " + last

    # add person info to people table
    cur = _execute_statement(
        conn,
        f"INSERT INTO PEOPLE (email,name,student_id) \
        VALUES ('{email}','{name}',{id})",
    )
    return email


# retrieves info for person with email from db
# returns -1 if no match found
def get_person(email: str, conn):

    cur = _execute_statement(conn, f"SELECT * FROM PEOPLE WHERE email = '{email}'")
    # person row
    result = cur.fetchone()

    return result[0]


# Checks if room with room_id already exists
def exists_in_rooms(room_id: str, conn):

    cur = _execute_statement(conn, f"SELECT COUNT(*) FROM ROOMS WHERE room_id = '{room_id}'")
    result = cur.fetchone()

    # room exists in rooms table
    if result[0] != 0:
        return True
    # rooms doesn't exist in rooms table
    else:
        return False


# add room entry to room table
def add_room(room_id: str, capacity: int, building_name: str, conn):
    # cursor
    if not (room_id and building_name):
        return -1

    # person exists in the people table
    if exists_in_rooms(room_id, conn):
        return -1

    # add room to rooms table
    cur = _execute_statement(
        conn,
        f"INSERT INTO ROOMS (room_id,capacity,building_name) \
        VALUES ('{room_id}','{capacity}','{building_name}')",
    )
    return 0


# retrieves room info
# returns -1 if no match found
def get_room(room_id: str, conn):

    cur = _execute_statement(conn, f"SELECT * FROM ROOMS WHERE room_id = '{room_id}'")
    # room row
    result = cur.fetchone()

    return result


# retrieves all users from people table
def get_all_users(conn):

    # execute query
    cur = _execute_statement(conn, f"SELECT * FROM PEOPLE")
    # rows
    result = cur.fetchall()

    return result
