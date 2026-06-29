import sqlite3

conn = sqlite3.connect('carparks.db')
cur = conn.cursor()

cur.execute('SELECT COUNT(*) FROM carpark_availability')
total_rows = cur.fetchone()[0]

cur.execute('SELECT COUNT(DISTINCT fetched_at) FROM carpark_availability')
total_runs = cur.fetchone()[0]

cur.execute('SELECT MIN(fetched_at), MAX(fetched_at) FROM carpark_availability')
first, last = cur.fetchone()

cur.execute('SELECT COUNT(*) FROM carparks')
static_count = cur.fetchone()[0]

print(f"Total rows in carpark_availability: {total_rows}")
print(f"Total distinct runs: {total_runs}")
print(f"First run: {first}")
print(f"Last run: {last}")
print(f"Static carparks loaded: {static_count}")

conn.close()