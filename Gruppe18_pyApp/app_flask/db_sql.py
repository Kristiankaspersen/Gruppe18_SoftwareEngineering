import sqlite3

con = sqlite3.connect('users.db')

cur = con.cursor()

# Create table
# cur.execute('''CREATE TABLE users
#                (name text, type text)''')

# Insert a row of data
# cur.execute("INSERT INTO users VALUES ('Per','buyer')")
# cur.execute("INSERT INTO users VALUES ('Arne','seller')")

# Save (commit) the changes
# con.commit()

# To retrive data
for row in cur.execute('SELECT * FROM users ORDER BY name'):
        print(row)

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()

