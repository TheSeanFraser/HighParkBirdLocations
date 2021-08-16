import re
import config
from datetime import datetime
import mysql.connector
from mysql.connector import Error


# Connect to MySQL database
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("----------------------------------------------------------")
        print("         MySQL Database connection successful")
        print("----------------------------------------------------------")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


# Perform a READ query on the database
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


# Inserts the collected data into the database
def insert_data_to_sql(data, checklistID, date, time, duration, location):
    connection = create_db_connection(config.my_host, config.my_user, config.my_pwd, config.my_db)

    # Creating a cursor object using the cursor() method
    cursor = connection.cursor()

    insert_effort_stmt = (
        "INSERT INTO EFFORT(CHECKLISTID, DATE, TIME, LOCATION, DURATION)"
        "VALUES (%s, %s, %s, %s, %s)"
    )
    # Preparing SQL query to INSERT a record into the database.
    insert_birds_stmt = (
        "INSERT INTO BIRDS(ID, SPECIES, EFFORT, LATITUDE, LONGITUDE, SURFACE)"
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )

    date = adjustDate(date)
    duration = adjustDuration(duration
                              )
    # Add the effort details to the database
    effortDetails = (checklistID, date, time, location, duration)

    try:
        # Executing the SQL command
        cursor.execute(insert_effort_stmt, effortDetails)

        # Commit your changes in the database
        connection.commit()
        print("Checklist inserted")

    except:
        # Rolling back in case of error
        connection.rollback()
        print("Checklist not inserted. Most likely already exists.")

    # Go through each bird and add it to the database
    for row in data:
        entry = row
        try:
            # Executing the SQL command
            cursor.execute(insert_birds_stmt, entry)
            # Commit your changes in the database
            connection.commit()

        except:
            # Rolling back in case of error
            connection.rollback()
            print("Data not inserted")
    print("Birds inserted")

    connection.close()

###############################################################################
#   HELPER FUNCTIONS
###############################################################################

# Adjusts the format of the date from Mmm D, YYYY to YYYY-MM-DD
def adjustDate(date):
    datetime_object = datetime.strptime(date,"%b %d, %Y")
    adjustedDate = datetime_object.strftime("%Y-%m-%d")

    return adjustedDate

# Adjusts the format of the duration from X hour(s), yy minute(s) to XXX minutes
def adjustDuration(duration):
    # Search the string for the digits, then do hour to minute calculation
    m = re.findall ('(?:\d+)', duration)
    if m:
        if (len(m) > 1):
            hours = int(m[0])
            minutes = int(m[1])
            totalMinutes = (hours * 60) + minutes
        else:
            totalMinutes = int(m[0])

    return totalMinutes