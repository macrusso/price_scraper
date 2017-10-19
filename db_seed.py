import sqlite3 as lite

# user have to manualy add part numbers to fill in the db
parts = (
    ('6ES7215-1HF40-0XB0', 0, 0),
    ('6ES7414-3XM07-0AB1', 0, 0),
    ('6ES7221-1BF32-0XB0', 0, 0)
)

con = lite.connect('test.db')

with con:
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS Parts")
    cur.execute("CREATE TABLE Parts(Part_no TEXT, Our_price INT, List_price INT)")
    cur.executemany("INSERT INTO Parts VALUES(?, ?, ?)", parts)

    cur.execute("SELECT Part_no FROM Parts")
    rows = cur.fetchall()

    for row in rows:
        print(row[0])
        New_Our_price = 300
        New_list_price = 500
        cur.execute("UPDATE Parts SET Our_price=?, List_price=? WHERE Part_no=?", (New_Our_price, New_list_price, row[0]))
        # con.commit()
