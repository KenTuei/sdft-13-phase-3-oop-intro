from __init__ import connection, cursor

class Patient:
    all = []

    def __init__(self, name):
        self.name = name
        self.all.append(self)

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS patients(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            );
        """
        cursor.execute(sql)
        connection.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS patients;"
        cursor.execute(sql)
        connection.commit()

    def save(self):
        sql = "INSERT INTO patients(name) VALUES(?);"
        cursor.execute(sql, [self.name])
        connection.commit()
        self.id = cursor.lastrowid

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM patients WHERE name = ?"
        cursor.execute(sql, (name,))
        row = cursor.fetchone()
        if row:
            patient = cls(row[1])  # row[1] is the name
            patient.id = row[0]    # row[0] is the id
            return patient
        return None
