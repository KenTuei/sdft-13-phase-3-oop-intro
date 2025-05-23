import sqlite3

CONN = sqlite3.connect('doctors_appointment.db')
CURSOR = CONN.cursor()