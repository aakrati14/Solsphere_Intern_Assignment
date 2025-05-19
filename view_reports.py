import sqlite3

conn = sqlite3.connect('reports.db')
c = conn.cursor()

c.execute('SELECT * FROM reports')
rows = c.fetchall()

print("📋 Saved System Reports:\n")
for row in rows:
    print(row)

conn.close()
