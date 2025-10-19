# Semester Project for 'Software Engineering' course at ECE, NTUA 2024-2025#
# EasyGo SoftEng 2024

# Team Members
- **Alexandros Papadakos**
- **Georgios Vitzilaios**

## 🚀 Overview
EasyGo is a  system developed for managing toll stations, users, and transactions efficiently. The project is built using Flask and MySQL and provides APIs for authentication, toll passes, statistics, and administrative operations.


## 🛠️ Technologies Used
- **Backend**: Python (Flask)
- **Database**: MySQL
- **Libraries**: Pandas, Flask, MySQL Connector, CSV, UUID
- **Testing**: Postman
- **Frontend**:HTML

## 🔥 Installation & Setup
### 1️⃣ Clone the repository
```sh
$ git clone https://github.com/ntua/softeng24-02
$ cd easygo
```

### 2️⃣ Set up a virtual environment
```sh
$ python3 -m venv venv
$ source venv/bin/activate  # On macOS/Linux
$ venv\Scripts\activate     # On Windows
```

### 3️⃣ Install dependencies
```sh
$ pip install -r requirements.txt
```

### 4️⃣ Configure MySQL Database

Ensure MySQL is installed and running. Insert the db.sql file as said in backend .Update `db_config` in `routes.py`:
```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yourpassword',
    'database': 'easygo'
}
```

### 5️⃣ Run the Flask application
```sh
$ flask run
```
The application should be running on `http://127.0.0.1:5000/`

## 🔑 API Endpoints
### 🔹 Authentication
- `POST /login` - User login
- `POST /register` - User registration

### 🔹 User Actions
- `GET /account` - View user details
- `GET /users_balance` - Get user balance

### 🔹 Toll Stations & Passes
- `GET /tollStationPasses/<tollStationID>/<date_from>/<date_to>` - Retrieve passes for a specific station
- `POST /admin/resetstations` - Reset station data from CSV
- `POST /admin/addpasses` - Upload new pass data

### 🔹 Statistics
- `GET /api/statistics/crossings` - Get monthly crossing statistics
- `GET /api/statistics/top3_crossings` - Get top 3 crossing stations

### 🔹 Admin Actions
- `GET /admin/healthcheck` - Database & server health check
- `POST /admin/resetpasses` - Reset passes from CSV

## 🧪 Testing with Postman
1. Import the provided Postman collection.
2. Ensure the server is running (`flask run`).
3. Execute API requests to verify responses.

## 🤝 Contributing
Pull requests are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit changes and push to your fork.
4. Submit a pull request.



