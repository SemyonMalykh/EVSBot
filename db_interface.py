from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import datetime
import configparser

def get_event_info(id):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "SELECT * FROM event WHERE event_id =" + str(id)
        cursor.execute(query)
        row = cursor.fetchone()
        while row is not None:
            cursor.close()
            conn.close()
            return(row)
  #          row = cursor.fetchone()
  #  except Error as e:
  #      print(e)
    finally:
         cursor.close()
         conn.close()
  #  return(event)

def get_event_name(id):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "SELECT name FROM event WHERE event_id =" + str(id)
        cursor.execute(query)
        row = cursor.fetchone()
        while row is not None:
            cursor.close()
            conn.close()
            return(row[0])
  #          row = cursor.fetchone()
  #  except Error as e:
  #      print(e)
    finally:
         cursor.close()
         conn.close()
  #  return(event)

def is_user_in_db(tg_id):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "SELECT * FROM tg_user WHERE tg_id =" + str(tg_id)
        cursor.execute(query)
        row = cursor.fetchone()
        user = []
        while row is not None:
            return(1)
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return(0)

def is_user_registred(tg_id, event_id):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "SELECT * FROM enrollments WHERE tg_id =" + str(tg_id) + " AND event_id =" + str(event_id)
        cursor.execute(query)
        row = cursor.fetchone()
        user = []
        while row is not None:
            return(1)
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return(0)

def events_tomorrow():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        date = datetime.date.today() + datetime.timedelta(days=1)
        query = "SELECT event_id FROM event WHERE start_date BETWEEN '" + str(datetime.date.today()) + "' AND '" + str(date) + "'"
        cursor.execute(query)
        row = cursor.fetchone()
        events = []
        while row is not None:
            events.append(row[0])
            row = cursor.fetchone()
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return (events)

def enrolled_users(event_id):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "SELECT tg_id FROM enrollments WHERE event_id=" + str(event_id)
        cursor.execute(query)
        row = cursor.fetchone()
        users = []
        while row is not None:
            users.append(row[0])
            row = cursor.fetchone()
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return (users)

def add_new_user(message_id, user_name):
    query = "INSERT INTO tg_user(tg_id,name) VALUES(%s,%s)"
    args = (message_id, user_name)
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()

def get_event_info_by_name(tg_name):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "SELECT * FROM event WHERE tg_name ='" + str(tg_name) + "'"
        cursor.execute(query)
        row = cursor.fetchone()
        while row is not None:
            cursor.close()
            conn.close()
            print(type(row))
            return(row)
  #          row = cursor.fetchone()
  #  except Error as e:
  #      print(e)
    finally:
         cursor.close()
         conn.close()
  #  return(event)

def get_event_id_by_name(tg_name):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "SELECT event_id FROM event WHERE tg_name ='" + str(tg_name) + "'"
        cursor.execute(query)
        row = cursor.fetchone()
        while row is not None:
            cursor.close()
            conn.close()
            print(row)
            return(row)[0]
  #          row = cursor.fetchone()
  #  except Error as e:
  #      print(e)
    finally:
         cursor.close()
         conn.close()
  #  return(event)

def get_forthcoming_events():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "SELECT event_id FROM event WHERE start_date >=" + str(datetime.date.today())
        cursor.execute(query)
        row = cursor.fetchone()
        events = []
        while row is not None:
            events.append(row[0])
            row = cursor.fetchone()
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return(events)

def get_user_enrollments(user_id):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "SELECT * FROM enrollments WHERE tg_id =" + str(user_id)
        cursor.execute(query)

        row = cursor.fetchone()
        events = []
        while row is not None:
            events.append(row)
            print(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
    return(events)

def enroll_user_to_event(user_id, tg_name):
    event_id = get_event_id_by_name(tg_name)
    query = "INSERT INTO enrollments(tg_id,event_id) VALUES(%s,%s)"
    args = (user_id, event_id)
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()

def turn_notification_on(user_id, event_id, days):
    # read database configuration
    db_config = read_db_config()
    # prepare query and dat1a
    query = "UPDATE enrollments SET notification =" + str(days) +" WHERE tg_id = %s AND event_id = %s"
    data = (user_id, event_id)
    try:
        conn = MySQLConnection(**db_config)
        # update book title
        cursor = conn.cursor()
        cursor.execute(query, data)
        # accept the changes
        conn.commit()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()

def turn_notification_off(user_id, event_id):
    # read database configuration
    db_config = read_db_config()
    # prepare query and dat1a
    query = "UPDATE enrollments SET notification = 0 WHERE tg_id = %s AND event_id = %s"
    data = (user_id, event_id)
    try:
        conn = MySQLConnection(**db_config)
        # update book title
        cursor = conn.cursor()
        cursor.execute(query, data)
        # accept the changes
        conn.commit()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()

def event_is_in_db(tg_name):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "SELECT * FROM event WHERE tg_name ='" + str(tg_name)+ "'"
        cursor.execute(query)
        row = cursor.fetchone()
        while row is not None:
            cursor.close()
            conn.close()
            return (1)
    finally:
        cursor.close()
        conn.close()
    return(0)

def get_event_organizer(event_id):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "SELECT tg_id FROM organizer WHERE event_id =" + str(event_id)
        cursor.execute(query)
        row = cursor.fetchone()
        while row is not None:
            cursor.close()
            conn.close()
            return (row)[0]
    #          row = cursor.fetchone()
    #  except Error as e:
    #      print(e)
    finally:
        cursor.close()
        conn.close()
#  return(event)