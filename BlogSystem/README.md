# RESTful Blog System with Flask

This project is a fully functional RESTful blog system built with Flask. It allows users to create, read, update, and delete blog posts, as well as add comments to posts. Additionally, it includes user registration, login functionality, and route protection to ensure secure access to certain features. The system also utilizes relational databases to manage users, blog posts, and comments.

## Features

### 1. **Blog Post Management**
   - **GET Blog Posts**: Retrieve all blog posts or a specific post by its ID.
   - **POST New Blog Post**: Create a new blog post.
   - **Edit Existing Blog Posts**: Update the content of an existing blog post.
   - **DELETE Blog Posts**: Remove a blog post from the system.

### 2. **User Authentication**
   - **Register New Users**: Allow new users to create an account.
   - **Login Registered Users**: Authenticate users and manage sessions.
   - **Protect Routes**: Restrict access to certain routes (e.g., creating, editing, or deleting posts) to authenticated users only.

### 3. **Relational Database**
   - Create and manage relationships between:
     - **Users** and **Blog Posts** (one-to-many relationship).
     - **Blog Posts** and **Comments** (one-to-many relationship).
   - Store user credentials, blog posts, and comments in a structured database.

### 4. **Comments**
   - Allow any user (authenticated or not) to add comments to blog posts.
   - Retrieve comments associated with a specific blog post.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flask-restful-blog.git
   cd flask-restful-blog
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

4. Configure the database:
   - Set up your database connection in `config.py`.
   - Run migrations to create the database schema:
     ```bash
     flask db init
     flask db migrate
     flask db upgrade
     ```

5. Run the application:
   ```bash
   flask run
   ```

---

## API Endpoints

### Blog Posts
- **GET `/api/posts`**: Retrieve all blog posts.
- **GET `/api/posts/<int:post_id>`**: Retrieve a specific blog post by ID.
- **POST `/api/posts`**: Create a new blog post (requires authentication).
- **PUT `/api/posts/<int:post_id>`**: Update an existing blog post (requires authentication).
- **DELETE `/api/posts/<int:post_id>`**: Delete a blog post (requires authentication).

### Comments
- **GET `/api/posts/<int:post_id>/comments`**: Retrieve all comments for a specific blog post.
- **POST `/api/posts/<int:post_id>/comments`**: Add a new comment to a blog post.

### Users
- **POST `/api/register`**: Register a new user.
- **POST `/api/login`**: Authenticate a user and return a session token.

---

## Code Examples

### Database Models
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    posts = db.relationship('BlogPost', backref='author', lazy=True)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)
```

### Creating a New Blog Post (Protected Route)
```python
from flask import request, jsonify
from flask_login import login_required, current_user

@app.route('/api/posts', methods=['POST'])
@login_required
def create_post():
    data = request.get_json()
    new_post = BlogPost(
        title=data['title'],
        content=data['content'],
        user_id=current_user.id
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post created successfully!"}), 201
```

### Adding a Comment to a Blog Post
```python
@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    data = request.get_json()
    new_comment = Comment(
        content=data['content'],
        post_id=post_id
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"message": "Comment added successfully!"}), 201
```

### User Registration
```python
from werkzeug.security import generate_password_hash

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(
        username=data['username'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201
```

---

## Frontend Integration

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

### Displaying Blog Posts and Comments
```html
{% for post in posts %}
  <div class="post">
    <h2>{{ post.title }}</h2>
    <p>{{ post.content }}</p>
    <h3>Comments:</h3>
    {% for comment in post.comments %}
      <p>{{ comment.content }}</p>
    {% endfor %}
  </div>
{% endfor %}
```

---

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This RESTful blog system is designed to be scalable and secure, with features that cater to both users and administrators. For more details, refer to the code and documentation in the repository.