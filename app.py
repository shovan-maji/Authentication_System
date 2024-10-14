from flask import Flask, request, jsonify
import bcrypt
import jwt
import random
import string
import time
# import datetime
from datetime import datetime, timedelta
import mysql.connector
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
CORS(app)
# Secret key for JWT
SECRET_KEY = 'your_secret_key'

otp_time = datetime.now()

# Database connection (MySQL)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pantua@6",
    database="authentication"
)
cursor = conn.cursor()

# Creating the users table if it doesn't exist
cursor.execute( '''
    CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    otp VARCHAR(6),
    token TEXT
)'''
)
conn.commit()
# print("Users table created successfully.")

# Function to generate OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

# Function to create JWT tokens
def create_jwt_token(user_id, email):
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.now() + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# Function to send OTP via email
def send_otp_email(recipient_email, otp):
    sender_email = "shovanmaji55@gmail.com"  # Replace with your email
    sender_password = "pgri bhic apyn hozm"  # Replace with your email password
    
    subject = "Your OTP Code"
    body = f"Your OTP code is: {otp}. Please use it to complete your login."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Enable security
            server.login(sender_email, sender_password)  # Log in to your email account
            server.send_message(msg)  # Send email
            print("OTP sent successfully!")
    except Exception as e:
        print(f"Failed to send OTP email: {e}")

# def delete_expired_otps():
#     expiration_time = datetime.datetime.now() - datetime.timedelta(minutes=5)
#     cursor.execute("DELETE FROM users WHERE otp_created_at < %s AND otp IS NOT NULL", (expiration_time,))
#     conn.commit()
#     print("Expired OTPs deleted.")

# scheduler = BackgroundScheduler()
# scheduler.add_job(delete_expired_otps, 'interval', minutes=1)
# scheduler.start()


# User signup 
@app.route('/signup', methods=['GET','POST'])
def signup():
    data = request.json
    email = data['email']
    password = data['password']
    
    # print(email)
    # print(password)

    # Hashing the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        print(f"Error: {e}")  # Print the error for debugging
        return jsonify({"message": "User already exists"}), 400
# try:
#     cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
#     conn.commit()
#     return jsonify({"message": "User registered successfully"}), 201
# except Exception as e:
#     print(f"Error: {e}")  # Print the error for debugging
#     return jsonify({"message": "User already exists"}), 400


# User login
@app.route('/login', methods=['GET','POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password'].encode('utf-8')

    cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password, user[1].encode('utf-8')):
        # Generate OTP and store it in the database
        otp = generate_otp()
        otp_time = datetime.now()
        
        cursor.execute("UPDATE users SET otp = %s WHERE id = %s", (otp, user[0]))
        conn.commit()
        
        # Send OTP via email
        send_otp_email(email, otp)  # Call the email sending function


        # (In real application, send the OTP via email or SMS)
        print(f"Generated OTP: {otp}")

        return jsonify({"success": True, "message": "OTP sent"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid email or password"}), 401

# OTP validation
@app.route('/validate_otp', methods=['GET','POST'])
def validate_otp():
    data = request.json
    otp = data['otp']
    
    

    cursor.execute("SELECT id, email FROM users WHERE otp = %s", (otp,))
    user = cursor.fetchone()

    if user:
    #     # Clear OTP after successful validation
    #     cursor.execute("UPDATE users SET otp = NULL WHERE id = %s", (user[0],))
    #     conn.commit()

        current_time = datetime.now()
        expiration_time =  otp_time + timedelta(seconds=300)
        if current_time > expiration_time:
            return jsonify({"success": False, "message": "OTP Expired"}), 400
        
        
        # Create JWT token
        token = create_jwt_token(user[0], user[1])
        cursor.execute("UPDATE users SET token = %s WHERE id = %s", (token, user[0]))
        conn.commit()

        return jsonify({"success": True, "message": "OTP validated", "token": token}), 200
    else:
        return jsonify({"success": False, "message": "Invalid OTP"}), 400

# Password reset
@app.route('/reset_password', methods=['GET','POST'])
def reset_password():
    data = request.json
    email = data['email']
    new_password = data['newPassword']

    # Hash the new password
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user:
        try:
            # Update the user's password
            cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
            conn.commit()
            return jsonify({"success": True, "message": "Password updated successfully"}), 200
        except Exception as e:
            return jsonify({"success": False, "message": "Error updating password"}), 500
    else:
        return jsonify({"success": False, "message": "Email not found"}), 404


if __name__ == '__main__':
    # try:
    #     app.run(host='0.0.0.0', port=5000, debug=True)
    # finally:
    #     scheduler.shutdown()
    app.run(host='0.0.0.0',port=5000,debug=True)
