import sqlite3

def get_db_connection():
    conn = sqlite3.connect('trendstoday.db')
    # conn.row_factory = sqlite3.Row # get results as python dictionarie
    return conn

# conn = get_db_connection()    
# cursor = conn.cursor()


# sql = "INSERT INTO trend(title, tweet, category, datetime) VALUES(?,?,?,?);"
# cursor.execute(sql, ("test", "test", "test", "2022-09-16 10:26"))
# conn.commit()

# cursor.execute("select * from trend")

# rows = cursor.fetchall()
# for row in rows:
#     print(row)

