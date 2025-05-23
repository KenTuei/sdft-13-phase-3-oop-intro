from __init__ import CURSOR, CONN

class Specialty:
    all = []
    def __init__(self, name):
        self.name = name
        self.all.append(self)

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS specialties (
                id INTEGER PRIMARY KEY,
                name TEXT
            );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS specialties;
        """
        CURSOR.execute(sql)
        CONN.commit()


    def save(self):
        sql = """
                 INSERT INTO specialties (name)VALUES (?, ?)
            """

        CURSOR.execute(sql, (self.name))
        CONN.commit()

        self.id = CURSOR.lastrowid

        print(self.id)