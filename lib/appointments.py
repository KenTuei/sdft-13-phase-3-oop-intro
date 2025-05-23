from __init__ import connection, cursor

class Appointment:
    all = []

    def __init__(self, doctor_id, patient_id, date):
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.date = date
        self.all.append(self)

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS appointments(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_id INTEGER,
                patient_id INTEGER,
                date TEXT,
                FOREIGN KEY(doctor_id) REFERENCES doctors(id),
                FOREIGN KEY(patient_id) REFERENCES patients(id)
            );
        """
        cursor.execute(sql)
        connection.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS appointments;"
        cursor.execute(sql)
        connection.commit()

    def save(self):
        sql = """
            INSERT INTO appointments(doctor_id, patient_id, date)
            VALUES(?, ?, ?);
        """
        cursor.execute(sql, (self.doctor_id, self.patient_id, self.date))
        connection.commit()
        self.id = cursor.lastrowid

    @classmethod
    def find_by_id(cls, appointment_id):
        sql = "SELECT * FROM appointments WHERE id = ?"
        cursor.execute(sql, (appointment_id,))
        row = cursor.fetchone()
        if row:
            appointment = cls(row[1], row[2], row[3])  # doctor_id, patient_id, date
            appointment.id = row[0]
            return appointment
        return None

    @classmethod
    def all_appointments(cls):
        sql = "SELECT * FROM appointments"
        cursor.execute(sql)
        rows = cursor.fetchall()
        appointments = []
        for row in rows:
            appointment = cls(row[1], row[2], row[3])
            appointment.id = row[0]
            appointments.append(appointment)
        return appointments

    def __repr__(self):
        return f"<Appointment id={self.id} doctor_id={self.doctor_id} patient_id={self.patient_id} date='{self.date}'>"
