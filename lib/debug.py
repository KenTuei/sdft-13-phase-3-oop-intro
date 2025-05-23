from __init__ import connection, cursor
from specialty import Specialty
from doctors import Doctor
from patients import Patient
from appointments import Appointment

import ipdb

# Ensure tables exist without dropping existing data
Specialty.create_table()
Doctor.create_table()
Patient.create_table()
Appointment.create_table()

# Seed initial specialties if they don't already exist
specialty_names = [
    "Oncologist", "Neurologist", "Endocrinologist",
    "Radiologist", "Urologist", "Psychiatrist"
]
for name in specialty_names:
    if not Specialty.find_by_name(name):
        Specialty(name).save()

# Seed initial doctors if they don't already exist
doctor_data = [
    ("Dr. Smith", "Oncologist"),
    ("Dr. Adams", "Neurologist"),
]
for doc_name, spec_name in doctor_data:
    if not Doctor.find_by_name(doc_name):
        Doctor.create(doc_name, spec_name)

# Seed initial patients if they don't already exist
patient_names = ["John Doe", "Jane Smith"]
for name in patient_names:
    if not Patient.find_by_name(name):
        Patient(name).save()

# Seed initial appointments if they don't already exist
appointment_data = [
    ("Dr. Smith", "John Doe", "2025-06-22"),
    ("Dr. Adams", "Jane Smith", "2025-06-23"),
]
for doc_name, pat_name, date in appointment_data:
    doc = Doctor.find_by_name(doc_name)
    pat = Patient.find_by_name(pat_name)
    cursor.execute(
        "SELECT 1 FROM appointments WHERE doctor_id=? AND patient_id=? AND date=?;",
        (doc.id, pat.id, date)
    )
    if not cursor.fetchone():
        Appointment(doc.id, pat.id, date).save()

# Drop into debugger for final inspection
ipdb.set_trace()
