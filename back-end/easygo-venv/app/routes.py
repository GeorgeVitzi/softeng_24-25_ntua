from app import app
import os 
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
import pandas as pd
import mysql.connector
import uuid
from functools import wraps
import csv
from io import StringIO
from flask import Response



db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'newpassword',
    'database': 'easygo'
}


def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection


#users = {
#    "user": "password	
#    "alex" : "1234"  # Replace with secure storage in production
#}

app.secret_key = 'your_secret_key'  
con = get_db_connection()
cursor = con.cursor(dictionary=True)

@app.before_request
def clear_session_on_restart():
    if 'app_started' not in session:
        session.clear()
        session['app_started'] = True

@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        tagid = request.form['tag_id'] ## changes the http name 
        #con.commit()
        # Process the data (e.g., save to the database or validate)
        #print(username, password, email, tagid)
        try :
            cursor.execute('select * from Users where username= %s', (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                flash('Username already taken!','danger')
                return render_template('register.html')
            
            q2 = 'INSERT INTO Users (username, password, email, tagid,user_balance) VALUES (%s, %s, %s, %s,%s)'
            cursor.execute(q2, (username, password, email, tagid,0))
            con.commit()  # Commit the transaction to save changes
            session['username'] = username 
            flash('Registration successful! ', 'success')
            return render_template('welcome_user.html')
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            flash('An error occurred while processing your request. Please try again.', 'danger')


        # Redirect to the welcome page after successful registratio
    
    # Render the registration form on GET request
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            # Check in Operators table
            q1 = 'SELECT * FROM Operators WHERE username = %s AND password = %s'
            cursor.execute(q1, (username, password))
            res = cursor.fetchone()

            if res is not None:  # If found in Operators
                session['username'] = username
                #flash('Login successful!', 'success')
                cursor.execute('select distinct Operator from tolls inner join Operators on Operators.OpID = tolls.OpID where Operators.username = %s',(session['username'],))
                opid = cursor.fetchone()
                opid = opid['Operator']
                return render_template('welcome_operator.html', username=username, opid=opid)
            
            # Check in Users table if not found in Operators
            q3 = 'SELECT * FROM Users WHERE username = %s AND password = %s'
            cursor.execute(q3, (username, password))
            res2 = cursor.fetchone()

            if res2 is not None:  # If found in Users
                session['username'] = username
                #flash('Login successful!', 'success')
                return render_template('welcome_user.html', username=username)
            else:
                flash('Username or password incorrect!', 'danger')
        
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            flash('An error occurred during login. Please try again.', 'danger')
        
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/welcome_user')
def welcome_user():
    # Your logic for the welcome user page
    return render_template('welcome_user.html')

@app.route('/partners')
def partners():
    if 'username' not in session:
        flash('You need to log in first!', 'error')
        return redirect(url_for('login'))
    return render_template('partners.html')

@app.route('/account')
def account():
    if 'username' not in session:
        flash('You need to log in first!', 'error')
        return redirect(url_for('login'))
    
    username = session['username']
    
    # Retrieve user details from the database
    cursor.execute('SELECT username, password, email, tagid, user_balance FROM Users WHERE username = %s', (username,))
    user_details = cursor.fetchone()
    
    if not user_details:
        flash('Error fetching user details.', 'danger')
        return redirect(url_for('welcome_user'))
    
    return render_template('account.html', user_details=user_details)


@app.route('/users_balance', methods=['GET', 'POST'])
def users_balance():
    # Ensure the user is logged in
    if 'username' not in session:
        flash("Please log in to view your balance.", "danger")
        return redirect(url_for('login'))

    # Initialize variables
    balance = None
    tag_id = None
    username = session['username']  # Username από το session

    # Retrieve user details from the database
    cursor.execute('SELECT user_balance, tagid FROM Users WHERE username = %s', (username,))
    result = cursor.fetchone()
    
    if result:
        balance = result['user_balance']
        tag_id = result['tagid']
    else:
        balance = 0  # Default balance
        tag_id = "Unknown"  # Default TagID

    if request.method == 'POST':
        # Process the form submission to load money
        amount = request.form.get('amount', type=float)
        if amount and amount > 0:
            cursor.execute('UPDATE Users SET user_balance = user_balance + %s WHERE username = %s', (amount, username))
            con.commit()

            # Refresh balance after update
            cursor.execute('SELECT user_balance FROM Users WHERE username = %s', (username,))
            result = cursor.fetchone()
            balance = result['user_balance'] if result else 0
        else:
            flash("Invalid amount. Please enter a positive value.", 'danger')

    # Check if "Load the target" button was clicked
    show_form = request.args.get('load_target') == 'true'

    return render_template('users_balance.html', balance=balance, show_form=show_form, username=username, tag_id=tag_id)

@app.route('/welcome_operator')
def welcome_operator():
    # Your logic for the welcome user page
    return render_template('welcome_operator.html')



@app.route('/partners_op')
def partners_op():
    if 'username' not in session:
        flash('You need to log in first!', 'error')
        return redirect(url_for('login'))
    return render_template('partners_op.html')

@app.route('/account_op')
def account_op():
    if 'username' not in session:
        flash('You need to log in first!', 'error')
        return redirect(url_for('login'))
    
    username = session['username']
    
    # Retrieve user details from the database
    cursor.execute('SELECT username, password, OpID FROM Operators WHERE username = %s', (username,))
    operator_details = cursor.fetchone()
    
    if not operator_details:
        flash('Error fetching user details.', 'danger')
        return redirect(url_for('welcome_operator'))
    
    return render_template('account_op.html', operator_details=operator_details)

@app.route('/opbal', methods=['GET', 'POST'])
def opbal():
    tool_log_data = None
    balance_data = None  # Αρχικοποίηση μεταβλητής για τα δεδομένα του ισοζυγίου
    payment_processed = False  # Για να δείξουμε αν έγινε επιτυχής πληρωμή

    try:
        # Εκτέλεση του SQL query για να πάρουμε τους distinct operators για το dropdown
        cursor.execute('SELECT DISTINCT BrandName, TRIM(OpID) AS OpID FROM Operators;')
        res = cursor.fetchall()  # Λίστα με τους operators
        print("Operators fetched:", res)  # Προσθήκη για debugging
    except mysql.connector.Error as err:
        print(f"Error fetching operators: {err}")
        res = []  # Κενή λίστα αν υπάρχει σφάλμα στη φόρτωση των operators

    try:
        # Λήψη του OpID του χρήστη από το session username
        cursor.execute('SELECT TRIM(OpID) AS OpID FROM Operators WHERE TRIM(username) = %s;', (session['username'].strip(),))
        usid = cursor.fetchone()
        usid = usid['OpID'] if usid else None
    except mysql.connector.Error as err:
        print(f"Error fetching OpID: {err}")
        usid = None

    if request.method == 'POST':
        if 'submit_debt' in request.form:  # Διαχείριση πληρωμής χρέους
            try:
                opid = request.form['opid'].strip()
                startdate = request.form['startdate'].strip()
                enddate = request.form['enddate'].strip()

                # Ενημέρωση διελεύσεων του χρήστη από δρόμους του επιλεγμένου operator
                cursor.execute('''
                    UPDATE tollog
                    SET calculated = 1
                    WHERE TRIM(taghomeid) = %s
                    AND LEFT(TRIM(tollid), %s) = %s
                    AND calculated = 0
                    AND DATE(timestamp) BETWEEN %s AND %s;
                ''', (usid, len(opid), opid, startdate, enddate))

                # Ενημέρωση διελεύσεων του επιλεγμένου operator από δρόμους του χρήστη
                cursor.execute('''
                    UPDATE tollog
                    SET calculated = 1
                    WHERE TRIM(taghomeid) = %s
                    AND LEFT(TRIM(tollid), %s) = %s
                    AND calculated = 0
                    AND DATE(timestamp) BETWEEN %s AND %s;
                ''', (opid, len(usid), usid, startdate, enddate))

                con.commit()  # Επιβεβαίωση αλλαγών στη βάση δεδομένων
                payment_processed = True
                print("Debt payment processed successfully.")
            except mysql.connector.Error as err:
                con.rollback()  # Ακύρωση αλλαγών σε περίπτωση σφάλματος
                print(f"Error processing debt payment: {err}")

        else:  # Υπολογισμός ισοζυγίου
            opid = request.form.get('opid').strip()
            startdate = request.form.get('startdate').strip()
            enddate = request.form.get('enddate').strip()
            print("Selected operator ID:", opid)

            try:
                opid_length = len(opid)
                usid_length = len(usid)
                print(opid_length, usid_length, opid, usid, startdate, enddate)

                # Εντοπισμός διελεύσεων του χρήστη από δρόμους του επιλεγμένου operator
                cursor.execute('''
                    SELECT charge, timestamp, tollid, TRIM(tagref) AS tagref
                    FROM tollog
                    WHERE TRIM(taghomeid) = %s
                    AND LEFT(TRIM(tollid), %s) = %s
                    AND calculated = 0
                    AND DATE(timestamp) BETWEEN %s AND %s;
                ''', (usid, opid_length, opid, startdate, enddate))
                user_charges_records = cursor.fetchall()

                # Εντοπισμός διελεύσεων του operator από δρόμους του χρήστη
                cursor.execute('''
                    SELECT charge, timestamp, tollid, TRIM(tagref) AS tagref
                    FROM tollog
                    WHERE TRIM(taghomeid) = %s
                    AND LEFT(TRIM(tollid), %s) = %s
                    AND calculated = 0
                    AND DATE(timestamp) BETWEEN %s AND %s;
                ''', (opid, usid_length, usid, startdate, enddate))
                operator_charges_records = cursor.fetchall()

                # Υπολογισμός συνολικών χρεώσεων
                user_total = sum(record['charge'] for record in user_charges_records)
                operator_total = sum(record['charge'] for record in operator_charges_records)

                # Δημιουργία balance_data με τις εγγραφές και τα συνολικά ποσά
                balance_data = {
                    'user_total': round(user_total, 3),
                    'operator_total': round(operator_total, 3),
                    'user_charges_records': user_charges_records,
                    'operator_charges_records': operator_charges_records,
                    'difference': round(user_total - operator_total, 3),
                    'message': "You owe" if user_total > operator_total else "Selected Operator owes you"
                }

            except mysql.connector.Error as err:
                print(f"Error fetching balance data: {err}")

    return render_template(
        'opbal.html',
        username=session.get('username', 'Guest'),
        operators=res,
        tool_log_data=tool_log_data,
        balance_data=balance_data,
        payment_processed=payment_processed
    )


@app.route('/stat')
def stat():
    return render_template('stat.html')


@app.route('/api/statistics/crossings', methods=['GET'])
def api_statistics_crossings():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    company = request.args.get('company')  # Παίρνουμε την εταιρεία από το query
    year = request.args.get('year')  # Παίρνουμε το έτος από το query

    if not company or not year:
        return jsonify({"error": "Invalid parameters"}), 400

    try:
        # Υπολογισμός μήκους του company ID
        company_length = len(company)

        # Εκτέλεση SQL ερωτήματος
        cursor.execute('''
            SELECT 
                MONTH(timestamp) AS month,
                COUNT(*) AS crossings
            FROM tollog
            WHERE LEFT(tollid, %s) = %s
            AND YEAR(timestamp) = %s
            GROUP BY MONTH(timestamp)
            ORDER BY month;
        ''', (company_length, company, year))
        data = cursor.fetchall()

        # Μετατροπή σε λεξικό για απλοποίηση
        crossings_per_month = {row['month']: row['crossings'] for row in data}

        # Επιστροφή δεδομένων για όλους τους μήνες (αν δεν υπάρχουν, είναι 0)
        result = {month: crossings_per_month.get(month, 0) for month in range(1, 13)}

        return jsonify(result)

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500


@app.route('/api/statistics/providers', methods=['GET'])
def api_statistics_providers():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        # Λήψη παραμέτρων από το αίτημα
        year = request.args.get('year')
        operator_id = request.args.get('operator_id')

        if not year or not operator_id:
            return jsonify({"error": "Invalid parameters"}), 400

        # Υπολογισμός μήκους του operator ID
        opid_length = len(operator_id)

        # SQL query για υπολογισμό διελεύσεων από διαφορετικούς providers
        cursor.execute('''
            SELECT 
                MONTH(timestamp) AS month,
                COUNT(*) AS crossings
            FROM tollog
            WHERE LEFT(tollid, %s) = %s
              AND taghomeid != %s
              AND YEAR(timestamp) = %s
            GROUP BY MONTH(timestamp)
            ORDER BY month;
        ''', (opid_length, operator_id, operator_id, year))

        data = cursor.fetchall()

        # Μορφοποίηση αποτελεσμάτων σε JSON
        result = {row['month']: row['crossings'] for row in data}

        return jsonify(result)

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500

@app.route('/api/statistics/operators_crossings', methods=['GET'])
def api_statistics_operators_crossings():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        # Λήψη παραμέτρων από το αίτημα
        year = request.args.get('year')

        if not year:
            return jsonify({"error": "Invalid parameters"}), 400

        # SQL query για υπολογισμό διελεύσεων σε διαφορετικές εταιρείες
        cursor.execute('''
            SELECT 
                CASE
                    WHEN LEFT(tollid, 3) = 'NAO' THEN LEFT(tollid, 3)
                    ELSE LEFT(tollid, 2)
                END AS operator_id, 
                COUNT(*) AS crossings
            FROM tollog
            WHERE 
                (CASE
                    WHEN LEFT(tollid, 3) = 'NAO' THEN LEFT(tollid, 3)
                    ELSE LEFT(tollid, 2)
                END) != taghomeid
                AND YEAR(timestamp) = %s
            GROUP BY operator_id
            ORDER BY crossings DESC;
        ''', (year,))


        data = cursor.fetchall()

        # Μορφοποίηση αποτελεσμάτων σε JSON
        result = {row['operator_id']: row['crossings'] for row in data}

        return jsonify(result)

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500

@app.route('/api/statistics/top3_crossings', methods=['GET'])
def api_statistics_top3_crossings():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        # SQL query για να υπολογίσουμε τις 3 κορυφαίες εταιρείες ανά εταιρεία διοδίων
        cursor.execute('''
            SELECT toll_operator, 
                   taghomeid AS source_operator, 
                   total_crossings
            FROM (
                SELECT LEFT(tollid, 
                            CASE 
                                WHEN LEFT(tollid, 3) = 'NAO' THEN 3
                                ELSE 2
                            END) AS toll_operator,
                       taghomeid,
                       COUNT(*) AS total_crossings,
                       ROW_NUMBER() OVER (
                           PARTITION BY LEFT(tollid, 
                                             CASE 
                                                 WHEN LEFT(tollid, 3) = 'NAO' THEN 3
                                                 ELSE 2
                                             END)
                           ORDER BY COUNT(*) DESC
                       ) AS ranking
                FROM tollog
                WHERE LEFT(tollid, 
                           CASE 
                               WHEN LEFT(tollid, 3) = 'NAO' THEN 3
                               ELSE 2
                           END) != taghomeid
                GROUP BY toll_operator, taghomeid
            ) AS ranked_data
            WHERE ranking <= 3
            ORDER BY toll_operator, total_crossings DESC;
        ''')

        # Λήψη δεδομένων από το query
        data = cursor.fetchall()
        print(data)
        # Ομαδοποίηση των αποτελεσμάτων σε δομή λεξικού για απλό χειρισμό
        result = {}
        for row in data:
            toll_operator = row['toll_operator']
            if toll_operator not in result:
                result[toll_operator] = []
            result[toll_operator].append({
                "source_operator": row['source_operator'],
                "crossings": row['total_crossings']
            })

        return jsonify(result)

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500

@app.route('/api/statistics/average_payment', methods=['GET'])
def api_statistics_average_payment():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    year = request.args.get('year')  # Παίρνουμε το έτος από το query

    if not year:
        return jsonify({"error": "Invalid parameters"}), 400

    try:
        # SQL query για υπολογισμό του συνολικού charge ανά μήνα και για κάθε χρήστη (tagref)
        cursor.execute('''
            SELECT 
                MONTH(timestamp) AS month,
                SUM(charge) / COUNT(DISTINCT tagref) AS avg_payment_per_user
            FROM tollog
            WHERE YEAR(timestamp) = %s
            GROUP BY MONTH(timestamp)
            ORDER BY month;
        ''', (year,))
        data = cursor.fetchall()

        # Μετατροπή των δεδομένων σε λεξικό με τον μήνα ως key
        result = {row['month']: float(row['avg_payment_per_user']) for row in data}

        # Επιστροφή δεδομένων για όλους τους μήνες (αν δεν υπάρχουν, μέσος όρος = 0)
        full_result = {month: result.get(month, 0) for month in range(1, 13)}

        return jsonify(full_result)

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500


@app.route('/api/statistics/export_data', methods=['GET'])
def export_data():
    # Ελέγχουμε αν ο χρήστης είναι συνδεδεμένος (αν χρησιμοποιείται session)
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        # Εκτέλεση του query για να πάρουμε τα δεδομένα από τη βάση
        cursor.execute('SELECT * FROM tollog')  # Παράδειγμα query
        data = cursor.fetchall()

        # Δημιουργία CSV
        output = StringIO()
        csv_writer = csv.DictWriter(output, fieldnames=data[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(data)
        output.seek(0)

        # Επιστροφή CSV αρχείου
        return Response(output.getvalue(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=data.csv"})
    except Exception as e:
        print(f"Error exporting data: {e}")
        return jsonify({"error": "An error occurred while exporting data"}), 500


@app.route('/admin/healthcheck', methods=['GET'])
def healthcheck():
    connection_string = f"mysql://{db_config['user']}@{db_config['host']}/{db_config['database']}"
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)  # Create new cursor
        
        # Fetch station count
        cursor.execute("SELECT COUNT(*) AS station_count FROM tolls;")
        n_stations = cursor.fetchone()["station_count"]

        # Fetch distinct tag count
        cursor.execute("SELECT COUNT(DISTINCT tagref) AS tag_count FROM tollog;")
        n_tags = cursor.fetchone()["tag_count"]

        # Fetch pass count
        cursor.execute("SELECT COUNT(*) AS pass_count FROM tollog;")
        n_passes = cursor.fetchone()["pass_count"]

        # Close cursor and connection
        cursor.close()
        connection.close()

        return jsonify({
            "status": "OK",
            "dbconnection": connection_string,
            "n_stations": n_stations,
            "n_tags": n_tags,
            "n_passes": n_passes
        }), 200

    except mysql.connector.Error as er:
        return jsonify({"status": "error", "message": str(er)}), 500



@app.route('/admin/resetstations', methods=['POST'])
def resetstations():
    try:
        # Clear the previous results from the cursor
        #cursor.execute('SELECT 1')  # Dummy query to clear unread results
        #cursor.fetchall()  # Consume any unread results

        # Delete all rows in the `tolls` table
        cursor.execute('DELETE FROM tolls;')
        con.commit()

        # Load the CSV data
        script_dir = os.path.dirname(__file__)
        # Δημιουργούμε την απόλυτη διαδρομή για το αρχείο CSV
        csv_file_path = os.path.join(script_dir, 'tollstations2024.csv')
        # Διαβάζουμε το αρχείο CSV
        df = pd.read_csv(csv_file_path)
        # Ensure correct mapping between CSV columns and DB columns
        db_columns = ['Lat', 'Longt', 'Nameid', 'Locality', 'Road', 'Operator', 'OpID', 'Email', 'Price1', 'Price2', 'Price3', 'Price4', 'tollid', 'pm']
        df = df[['Lat', 'Long', 'Name', 'Locality', 'Road', 'Operator', 'OpID', 'Email', 'Price1', 'Price2', 'Price3', 'Price4', 'TollID', 'PM']]

        # Insert rows from the CSV into the database
        for _, row in df.iterrows():
            query = f"INSERT INTO tolls ({', '.join(db_columns)}) VALUES ({', '.join(['%s'] * len(db_columns))})"
            cursor.execute(query, tuple(row))

        # Commit the transaction
        con.commit()
        return jsonify({"status": "OK"}), 200

    except Exception as e:
        # Rollback on failure
        con.rollback()
        return jsonify({"status": "failed", "info": str(e)}), 500


@app.route('/admin/resetpasses', methods =['POST']) #prepei na ftiaxtei kai na kanei reset ta users
def resetpasses():
    try:
        cursor.execute('delete from tollog')
        con.commit()
        script_dir = os.path.dirname(__file__)
        # Δημιουργούμε την απόλυτη διαδρομή για το αρχείο CSV /home/alex/Documents/softeng24-02/back-end/easygo-venv/app/passes-sample.csv
        csv_file_path = os.path.join(script_dir, 'passes-sample.csv')
        # Διαβάζουμε το αρχείο CSV
        df = pd.read_csv(csv_file_path)
        query = "insert into tollog values(%s,%s,%s,%s,%s,%s)"
        for _,row in df.iterrows():
            cursor.execute(query,tuple(row))
        
        con.commit()
        return jsonify({"status":'OK'}),200
    except Exception as e:
        con.rollback()
        return jsonify({
                        "status":"failed",
                        "info":str(e)}),500
   
@app.route('/admin/addpasses', methods=['POST'])
def add_passes():
    if 'file' not in request.files:
        return jsonify({"status": "failed", "info": "no file attached"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "failed", "info": "No file selected"}), 400

    file_path = os.path.join("/tmp", file.filename)
    file.save(file_path)
    
    try:
        df = pd.read_csv(file_path)
        required_columns = ['timestamp', 'tollID', 'tagRef', 'tagHomeID', 'charge']

        # Check if all required columns exist
        if not all(col in df.columns for col in required_columns):
            return jsonify({"status": "failed", "info": "wrong type of form"}), 400

        # Add 'calculated' column if it does not exist, setting all values to 0
        df['calculated'] = 0

        for _, row in df.iterrows():
            tag_ref = str(row['tagRef']).strip()
            tag_home_id = str(row['tagHomeID']).strip()
            charge = float(row['charge'])
            calculated = int(row['calculated'])  # Always 0

            cursor = con.cursor(dictionary=True, buffered=True)
            
            # Fetch user balance
            cursor.execute("SELECT user_balance FROM Users WHERE TRIM(TagID) = %s", (tag_ref,))
            result = cursor.fetchone()
            cursor.fetchall()  # Ensure all results are consumed

            if not result:
                cursor.close()
                return jsonify({"status": "failed", "info": f"User with tagRef {tag_ref} not found"}), 404

            user_balance = result['user_balance']
            new_balance = user_balance - charge

            if new_balance < 0:
                cursor.close()
                return jsonify({"status": "failed", "info": f"FAIL TO PASS. PLEASE LOAD YOUR TARGET (tagRef: {tag_ref})"}), 400

            # Update user balance
            cursor.execute("UPDATE Users SET user_balance = %s WHERE TRIM(TagID) = %s", (new_balance, tag_ref))
            con.commit()

            # Insert into tollog with calculated = 0
            query = "INSERT INTO tollog (timestamp, tollID, tagRef, tagHomeID, charge, calculated) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (row['timestamp'], row['tollID'], tag_ref, tag_home_id, charge, calculated))
            con.commit()

            cursor.close()  # Close cursor after each loop iteration

        return jsonify({"status": "OK", "info": "Passes processed successfully"}), 200

    except Exception as e:
        con.rollback()
        return jsonify({"status": "failed", "info": str(e)}), 500

    except Exception as e:
        con.rollback()
        print(f"Error: {str(e)}")
        return jsonify({"status": "failed", "info": str(e)}), 500


@app.route('/tollStationPasses/<string:tollStationID>/<string:date_from>/<string:date_to>', methods=['GET'])
def get_toll_station_passes(tollStationID, date_from, date_to):
    try:
        from datetime import datetime

        # Convert date format
        try:
            date_from = datetime.strptime(date_from, "%Y%m%d").strftime("%Y-%m-%d")
            date_to = datetime.strptime(date_to, "%Y%m%d").strftime("%Y-%m-%d")
        except ValueError:
            return jsonify({"status": "failed", "info": "Invalid date format. Use YYYYMMDD."}), 400

        # Create a new cursor
        cursor = con.cursor(dictionary=True)

        # Query for station details
        cursor.execute("SELECT Nameid, Operator FROM tolls WHERE tollid = %s", (tollStationID,))
        station_data = cursor.fetchone()
        cursor.fetchall()  # ✅ Clears unread results

        if not station_data:
            return jsonify({"status": "failed", "info": "Toll station not found"}), 404

        station_operator = station_data["Operator"]

        # Query for toll passes
        cursor.execute("""
            SELECT timestamp, tollID, tagRef, charge
            FROM tollog
            WHERE tollID = %s AND timestamp BETWEEN %s AND %s
            ORDER BY timestamp
        """, (tollStationID, date_from, date_to))
        passes = cursor.fetchall()
        cursor.fetchall()  # ✅ Clears unread results

        if not passes:
            return jsonify({
                "status": "failed",
                "info": "No passes found for this station in the given period"
            }), 404

        # Query for station operator ID
        cursor.execute("SELECT OpID FROM tolls WHERE tollid = %s", (tollStationID,))
        stop = cursor.fetchone()
        cursor.fetchall()  # ✅ Clears unread results

        if not stop:
            return jsonify({"status": "failed", "info": "Operator ID not found"}), 404

        stop_opid = stop["OpID"]

        pass_list = []
        for index, pass_record in enumerate(passes, start=1):
            cursor.execute("SELECT IDHome FROM Users WHERE TagID = %s", (pass_record["tagRef"],))
            tag_home = cursor.fetchone()
            cursor.fetchall()  # ✅ Clears unread results

            tag_home_id = tag_home["IDHome"] if tag_home else "UNKNOWN"

            timestamp_str = pass_record["timestamp"].strftime("%Y-%m-%d %H:%M")
            pass_id = f"{timestamp_str.replace(' ', '_')}_{tollStationID}"
            pass_list.append({
                "passIndex": index,
                "passID": pass_id,
                "timestamp": timestamp_str,
                "tagID": pass_record["tagRef"],
                "passType": "home" if tag_home_id.strip() == stop_opid.strip() else "visitor",
                "passCharge": float(pass_record["charge"]),
            })

        cursor.close()  # ✅ Close cursor after using it

        response_data = {
            "stationID": tollStationID,
            "stationOperator": station_operator,
            "requestTimestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "periodFrom": date_from,
            "periodTo": date_to,
            "nPasses": len(pass_list),
            "passList": pass_list,
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"status": "failed", "info": str(e)}), 500



@app.route('/passAnalysis/<string:stationOpID>/<string:tagOpID>/<string:date_from>/<string:date_to>', methods=['GET'])
def passanalysis(stationOpID, tagOpID, date_from, date_to):
    try:
        from datetime import datetime
        try:
            date_from = datetime.strptime(date_from, "%Y%m%d").strftime("%Y-%m-%d")
            date_to = datetime.strptime(date_to, "%Y%m%d").strftime("%Y-%m-%d")
        except ValueError:
            return jsonify({"status": "failed", "info": "Invalid date format. Use YYYYMMDD."}), 400
        
        # Fetch all records that match the given date range, toll station operator, and tag home operator
        query = """
            SELECT tollog.tollid AS stationID, 
                   tollog.timestamp AS timestamp, 
                   tollog.tagref AS tagID, 
                   tollog.charge AS passCharge
            FROM tollog
            WHERE LEFT(tollog.tollid, %s) = %s  -- Ensure stationOpID matches the toll station's operator prefix
              AND tollog.taghomeid = %s  -- Ensure the tag belongs to tagOpID
              AND tollog.timestamp BETWEEN %s AND %s
            ORDER BY tollog.timestamp ASC;
        """
        cursor.execute(query, (len(stationOpID), stationOpID, tagOpID, date_from, date_to))
        passes = cursor.fetchall()

        if not passes:
            return jsonify({"status": "failed", "info": "No passes found for the given parameters."}), 404

        pass_list = []
        for index, pass_record in enumerate(passes, start=1):
            pass_list.append({
                "passIndex": index,
                "passID": f"pass-{index}",  # Synthetic ID if none exists
                "stationID": pass_record['stationID'],
                "timestamp": pass_record['timestamp'].strftime("%Y-%m-%d %H:%M"),  # Format datetime
                "tagID": pass_record['tagID'],
                "passCharge": float(pass_record['passCharge'])
            })

        response_data = {
            "stationOpID": stationOpID,
            "tagOpID": tagOpID,
            "requestTimestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "periodFrom": date_from,
            "periodTo": date_to,
            "nPasses": len(pass_list),
            "passList": pass_list
        }

        # CSV Format
        response_format = request.args.get('format', 'json').lower()
        if response_format == 'csv':
            csv_headers = ["passIndex", "passID", "stationID", "timestamp", "tagID", "passCharge"]
            csv_data = [",".join(csv_headers)]
            csv_data += [",".join(map(str, [
                pass_item["passIndex"],
                pass_item["passID"],
                pass_item["stationID"],
                pass_item["timestamp"],
                pass_item["tagID"],
                pass_item["passCharge"]
            ])) for pass_item in pass_list]
            csv_output = "\n".join(csv_data)
            response = app.response_class(
                csv_output,
                mimetype='text/csv',
            )
            response.headers['Content-Disposition'] = f'attachment; filename=passAnalysis_{stationOpID}_{tagOpID}_{date_from}_{date_to}.csv'
            return response

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"status": "failed", "info": str(e)}), 500

    
    
@app.route('/passesCost/<string:tollOpID>/<string:tagOpID>/<string:date_from>/<string:date_to>',methods=['GET'])
def passescost(tollOpID,tagOpID,date_from,date_to):
    try:    
        from datetime import datetime
        try:
            date_from = datetime.strptime(date_from, "%Y%m%d").strftime("%Y-%m-%d")
            date_to = datetime.strptime(date_to, "%Y%m%d").strftime("%Y-%m-%d")
        except ValueError:
            return jsonify({"status": "failed", "info": "Invalid date format. Use YYYYMMDD."}), 400
        
        query = """
                select count(*), sum(charge) from tollog where taghomeid = %s and tollid like %s
                """
        cursor.execute(query,(f'{tollOpID}',f"%{tagOpID}%"))
        res = cursor.fetchone()
        response_data = {
            "tollOpID":tollOpID,
            "tagOpID":tagOpID,
            "requestTimestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "periodFrom":date_from,
            "periodTo":date_to,
            "nPasses":res['count(*)'],
            "passesCost":res['sum(charge)']
        }
        response_format = request.args.get('format','json').lower()
        if response_format == 'csv':
            csv_headers = ["tollOpID","tagOpID","requestTimestamp","periodFrom","periodTo","nPasses","passesCost"]
            csv_data = [",".join(csv_headers)]
            csv_data.append(",".join(map(str, [
                response_data["tollOpID"],
                response_data["tagOpID"],
                response_data["requestTimestamp"],
                response_data["periodFrom"],
                response_data["periodTo"],
                response_data["nPasses"],
                response_data["passesCost"]
            ])))
            csv_output = "\n".join(csv_data)
            response = app.response_class(
                csv_output,
                mimetype='text/csv',
            )
            response.headers['Content-Disposition'] = f'attachment; filename=passesCost_{tollOpID}_{tagOpID}_{date_from}_{date_to}.csv'
            return response
        return jsonify(response_data),200
    except Exception as e:
        return jsonify({"status":"failed", "info":str(e)}),500


@app.route('/chargesBy/<string:tollOpID>/<string:date_from>/<string:date_to>',methods = ['GET'])
def chargesby(tollOpID,date_from,date_to):
    try:
        from datetime import datetime
        try:
            date_from = datetime.strptime(date_from, "%Y%m%d").strftime("%Y-%m-%d")
            date_to = datetime.strptime(date_to, "%Y%m%d").strftime("%Y-%m-%d")
        except ValueError:
            return jsonify({"status": "failed", "info": "Invalid date format. Use YYYYMMDD."}), 400
        query = '''
            select taghomeid,count(taghomeid) as count ,sum(charge) as sum from tollog where tollid like %s and taghomeid !=%s group by taghomeid;
                '''
        cursor.execute(query,(f"%{tollOpID}%",tollOpID))
        charges = cursor.fetchall()
        print(charges)

        charge_list = []
        for charge_record in charges:
            charge_list.append({
                "visitingOpID":charge_record['taghomeid'],
                "nPasses":charge_record['count'],
                "passesCost":charge_record['sum']
            })
        
        response_data = {
            "tollOpID":tollOpID,
            "requesTimestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "periodFrom":date_from,
            "periodTo":date_to,
            "vOpList":charge_list
        }

        response_format = request.args.get('format','json').lower()
        if response_format == 'csv':
            csv_headers = ['visitingOpID','nPasses','passesCost']
            csv_data = [','.join(csv_headers)]
            csv_data +=[",".join(map(str, [
                pass_item["visitingOpID"],
                pass_item["nPasses"],
                pass_item['passesCost']
            ])) for pass_item in charge_list]
            csv_output = "\n".join(csv_data)
            response = app.response_class(
                csv_output,
                mimetype='text/csv'
            )
            response.headers['Content-Disposition'] = f'attachment; filename=chargesBy_{tollOpID}_{date_from}_{date_to}.csv'
            return response
        
        return jsonify(response_data),200

    except Exception as e:
        return jsonify({"status":"failed","info":str(e)})


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    app.run(debug=True)