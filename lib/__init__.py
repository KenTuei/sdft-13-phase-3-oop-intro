import sqlite3

#connection string: it's a statement that defines the details of the database:
# path(URL/IP address), database name, username, password

connection = sqlite3.connect('lib/doctors_appointment.db') # conection string
cursor = connection.cursor()