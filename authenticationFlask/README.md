# Flask Authentication System

This project implements a secure authentication system using Flask, featuring password encryption, hashing, and salting. It also includes user authentication with Flask-Login, flash messages for user feedback, and passing authentication status to templates.

## Features

### 1. **Encryption and Hashing**
   - Passwords are securely encrypted and hashed to ensure data protection.
   - Hashing is performed using the Werkzeug security library, which provides robust password hashing utilities.

### 2. **Salting Passwords**
   - Each password is salted with a unique random value before hashing to prevent rainbow table attacks and enhance security.

### 3. **Hashing and Salting with Werkzeug**
   - The `werkzeug.security` module is used to hash and salt passwords securely.
   - Key functions:
     - `generate_password_hash(password)` - Generates a salted and hashed password.
     - `check_password_hash(hashed_password, password)` - Verifies a password against its hashed version.

### 4. **User Authentication with Flask-Login**
   - Flask-Login is used to manage user sessions and authentication.
   - Key features:
     - User login and logout functionality.
     - Protection of routes with the `@login_required` decorator.
     - Session management for authenticated users.

### 5. **Flask Flash Messages**
   - Flash messages are used to provide feedback to users during authentication processes (e.g., successful login, invalid credentials, etc.).
   - Messages are displayed in templates using Flask's `flash()` function.

### 6. **Passing Authentication Status to Templates**
   - The authentication status of the user (logged in or not) is passed to templates.
   - This allows for dynamic rendering of content based on the user's authentication state (e.g., displaying a "Logout" button for authenticated users).

## Installation

1. Clone the repository:
   ```bash
   git clone url
   cd flask-authentication-system
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Create a `.env` file and add your secret key:
     ```plaintext
     SECRET_KEY=your_secret_key_here
     ```

5. Run the application:
   ```bash
   flask run
   ```

## Usage

- **Register a new user**: Visit `/register` to create a new account.
- **Login**: Visit `/login` to authenticate.
- **Protected routes**: Access protected routes only after logging in.
- **Logout**: Visit `/logout` to end the session.

## Code Example

### Hashing and Salting Passwords
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hashing a password
hashed_password = generate_password_hash('user_password')

# Verifying a password
is_valid = check_password_hash(hashed_password, 'user_password')
```

### Flask-Login Integration
```python
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

login_manager = LoginManager(app)

class User(UserMixin):
    # User model implementation
    pass

@login_manager.user_loader
def load_user(user_id):
    # Load user from database
    return User.get(user_id)

@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(username=request.form['username']).first()
    if user and check_password_hash(user.password, request.form['password']):
        login_user(user)
        flash('Logged in successfully!')
        return redirect(url_for('dashboard'))
    flash('Invalid credentials')
    return redirect(url_for('login'))
```

### Flash Messages in Templates
```html
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <div class="flash-messages">
      {% for message in messages %}
        <p>{{ message }}</p>
      {% endfor %}
    </div>
  {% endif %}
{% endwith %}
```

### Passing Authentication Status to Templates
```html
{% if current_user.is_authenticated %}
  <p>Welcome, {{ current_user.username }}!</p>
  <a href="{{ url_for('logout') }}">Logout</a>
{% else %}
  <a href="{{ url_for('login') }}">Login</a>
  <a href="{{ url_for('register') }}">Register</a>
{% endif %}
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This README provides a comprehensive overview of the Flask Authentication System. For further details, refer to the code and documentation in the repository.