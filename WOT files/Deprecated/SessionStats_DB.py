import psycopg2
from dotenv import load_dotenv
import os
import datetime

load_dotenv() # load enviroment variables

# INSERT SQL query statement for individual battle
def insertBattle(battle_time, tank_id, tank_name, damage, wn8, kills, xp, win):

    # string must follow EXACT format of the SQL query
    return f"""
    INSERT INTO session_stats(battle_time, tank_id, tank_name, damage, wn8, kills, xp, win)

    VALUES('{battle_time}', {tank_id}, '{tank_name}', {damage}, {wn8}, {kills}, {xp}, {win})

    RETURNING *;
    """

def selectBattle():
    pass

# UPDATE SQL query statement for overall session
def updateOverall():
    pass

# CONNECT to postgres databse and execute SQL query
def connect(query, table):
    """ Connect to the PostgreSQL database server """

    try: 

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user = "postgres",
            password=os.getenv("POSTGRESS_PW"))
		
        # create a cursor
        cur = conn.cursor()
        
        cur.executemany(query, (table,))

        conn.commit()
       
	# close the communication with the PostgreSQL
        cur.close()
    
    except (Exception, psycopg2.DatabaseError) as error:
        print("-----------------------------------")
        print(error)
        print("-----------------------------------")

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


#if __name__ == '__main__':
    
    #time = datetime.datetime.now()
    #print(time.strftime("%c"))
    #insert = insertBattle(time.strftime("%c"), 123, "chieftian", 156, 200, 403, 303, 1)
