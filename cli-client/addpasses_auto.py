import time
import random
import tempfile
import csv
import requests
import mysql.connector
from datetime import datetime

# Ρυθμίσεις για το API και τη βάση δεδομένων
BASE_URL = "http://localhost:5000/api/addpasses"
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "newpassword",  # Αντικατέστησε με τον κωδικό σου
    "database": "easygo",  # Αντικατέστησε με το όνομα της βάσης σου
}

# Συνάρτηση για τη δημιουργία τυχαίας διέλευσης
def create_random_pass():
    try:
        # Σύνδεση με τη βάση δεδομένων
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Ανάκτηση ενός τυχαίου tollid και τιμής χρέωσης
        cursor.execute("SELECT tollid, Price1, Price2, Price3 FROM tolls ORDER BY RAND() LIMIT 1;")
        toll_data = cursor.fetchone()
        tollid = toll_data['tollid']
        charge = random.choice([toll_data['Price1'], toll_data['Price2'], toll_data['Price3']])

        # Ανάκτηση ενός τυχαίου χρήστη (tagref και taghomeid)
        cursor.execute("SELECT TagID, IDHome FROM Users ORDER BY RAND() LIMIT 1;")
        user_data = cursor.fetchone()
        tagref = user_data['TagID']
        taghomeid = user_data['IDHome']

        # Δημιουργία της τρέχουσας ημερομηνίας και ώρας
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Η τιμή "calculated" είναι πάντα 0
        calculated = 0

        # Δημιουργία λεξικού με τα δεδομένα
        pass_data = {
            "timestamp": timestamp,
            "tollID": tollid,
            "tagRef": tagref,
            "tagHomeID": taghomeid,
            "charge": charge,
            "calculated": calculated
        }
        return pass_data

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Συνάρτηση για την αποστολή δεδομένων στο API
def send_pass_to_api(pass_data):
    try:
        # Δημιουργία προσωρινού αρχείου CSV
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp_file:
            writer = csv.DictWriter(tmp_file, fieldnames=["timestamp", "tollID", "tagRef", "tagHomeID", "charge", "calculated"])
            writer.writeheader()  # Προσθήκη επικεφαλίδων
            writer.writerow(pass_data)  # Προσθήκη των δεδομένων
            tmp_file_path = tmp_file.name  # Αποθηκεύουμε το path του αρχείου

        # Αποστολή του αρχείου στο API
        with open(tmp_file_path, 'rb') as f:
            files = {'file': (tmp_file_path, f, 'text/csv')}  # Ορισμός τύπου αρχείου
            response = requests.post(BASE_URL, files=files)

        # Έλεγχος απάντησης API
        if response.status_code == 200:
            print(f"Pass uploaded successfully: {pass_data}")
        else:
            print(f"Failed to upload pass. Status code: {response.status_code}, Info: {response.text}")

    except Exception as e:
        print(f"Error sending data to API: {e}")

# Κύρια συνάρτηση που εκτελεί την ατέρμονη λειτουργία
def main():
    print("Starting infinite CLI loop to generate and upload random passes every 30 seconds...")
    while True:
        pass_data = create_random_pass()
        if pass_data:
            send_pass_to_api(pass_data)
        else:
            print("Failed to create pass data.")
        time.sleep(30)  # Καθυστέρηση 30 δευτερολέπτων

if __name__ == "__main__":
    main()

