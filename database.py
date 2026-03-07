import sqlite3

conn = sqlite3.connect("moto.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS mantenimiento (
id INTEGER PRIMARY KEY AUTOINCREMENT,
fecha TEXT,
km INTEGER,
servicio TEXT,
costo INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS gasolina (
id INTEGER PRIMARY KEY AUTOINCREMENT,
fecha TEXT,
km INTEGER,
litros REAL,
precio INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT
)
""")

conn.commit()
conn.close()

print("Base de datos creada")