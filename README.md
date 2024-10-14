# User Authentication System

This is a user authentication system built with a frontend using HTML, CSS, and JavaScript, and a backend using Python (Flask) with MySQL as the database. The system supports user signup, login with OTP validation, and password reset functionality.

## Features

1. **Signup**:  
   Users can register with their email and password. The credentials are securely stored in the MySQL database after password hashing with bcrypt.

2. **Login with OTP**:  
   After entering their email and password during login, an OTP is generated and sent to the user's email. The user must validate the OTP to successfully log in.

3. **Password Reset**:  
   Users can reset their password if they forget it by entering their email and a new password. The new password is securely stored in the database after being hashed.

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **Database**: MySQL
- **OTP**: OTP is sent via email using Python's `smtplib`

## Pages

1. **Signup Page (`index.html`)**:  
   Allows users to register by entering their email and password.

2. **Login Page (`login.html`)**:  
   Users enter their email and password. If the credentials are correct, an OTP is sent to the registered email.

3. **OTP Page (`otp.html`)**:  
   Users enter the OTP sent to their email. If the OTP is correct, the user is successfully logged in.

4. **Reset Password Page (`reset_password.html`)**:  
   Allows users to reset their password by entering their email and new password.

## How to Run the Project

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    ```

2. **Navigate to the Project Directory**:
    ```bash
    cd your-repo-name
    ```

3. **Set Up the MySQL Database**:
    - Create a MySQL database and a `users` table by running the following query:
      ```sql
      CREATE DATABASE authentication;
      USE authentication;
      
      CREATE TABLE IF NOT EXISTS users (
          id INT AUTO_INCREMENT PRIMARY KEY,
          email VARCHAR(255) UNIQUE NOT NULL,
          password VARCHAR(255) NOT NULL,
          role VARCHAR(50) DEFAULT 'user',
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          otp VARCHAR(6),
          token TEXT
      );
      ```

4. **Set Up Python Environment**:
    - Install dependencies:
      ```bash
      pip install flask bcrypt jwt mysql-connector-python flask-cors
      ```

5. **Run the Flask Server**:
    ```bash
    python app.py
    ```

6. **Access the Application**:
    - Open the web browser and navigate to `http://localhost:5000` to use the signup, login, OTP, and password reset pages.

## Environment Variables

- **SECRET_KEY**: Add your secret key for JWT encryption.
- **Email Credentials**: Update the email and password used for sending OTP emails in `app.py`:
    ```python
    sender_email = "your-email@gmail.com"
    sender_password = "your-email-password"
    ```

## Future Improvements

- Implement token-based session management after OTP validation.
- Add email verification during signup.
- Secure password reset with OTP or security questions.
