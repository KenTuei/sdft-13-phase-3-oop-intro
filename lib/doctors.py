from __init__ import connection, cursor
from specialty import Specialty

class Doctor:
    all = []

    def __init__(self, name, specialty_id, id=None):
        self.name = name
        self.specialty_id = specialty_id
        self.id = id
        self.all.append(self)

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS doctors(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                specialty_id INTEGER NOT NULL,
                FOREIGN KEY(specialty_id) REFERENCES specialties(id)
            );
        """
        cursor.execute(sql)
        connection.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS doctors;"
        cursor.execute(sql)
        connection.commit()

    def save(self):
        if self.id:
            return self.update()
        sql = "INSERT INTO doctors(name, specialty_id) VALUES(?, ?);"
        cursor.execute(sql, (self.name, self.specialty_id))
        connection.commit()
        self.id = cursor.lastrowid

    def update(self):
        sql = "UPDATE doctors SET name=?, specialty_id=? WHERE id=?;"
        cursor.execute(sql, (self.name, self.specialty_id, self.id))
        connection.commit()

    def delete(self):
        sql = "DELETE FROM doctors WHERE id=?;"
        cursor.execute(sql, (self.id,))
        connection.commit()
        Doctor.all.remove(self)

    @classmethod
    def create(cls, name, specialty_name):
        """
        Create and save a doctor by specialty name.
        Raises ValueError if specialty not found.
        """
        spec = Specialty.find_by_name(specialty_name)
        if not spec:
            raise ValueError(f"Specialty '{specialty_name}' not found.")
        doctor = cls(name, spec.id)
        doctor.save()
        return doctor

    @classmethod
    def all_from_db(cls):
        cursor.execute("SELECT id, name, specialty_id FROM doctors;")
        rows = cursor.fetchall()
        cls.all = [cls(name=row[1], specialty_id=row[2], id=row[0]) for row in rows]
        return cls.all

    @classmethod
    def find_by_name(cls, name):
        cursor.execute("SELECT id, name, specialty_id FROM doctors WHERE name=?;", (name,))
        row = cursor.fetchone()
        if row:
            return cls(name=row[1], specialty_id=row[2], id=row[0])
        return None

    def __repr__(self):
        return f"<Doctor id={self.id} name={self.name} specialty_id={self.specialty_id}>"
