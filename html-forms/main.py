import requests
from flask import Flask, render_template
from flask import request
import smtplib

from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)

my_email = "pythonstudytian@gmail.com"
password = "vhuhyfewasurzrpv"

posts = requests.get(url="https://api.npoint.io/c790b4d5cab58020d391",verify=False).json()
@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    title = "Contact Me"
    return render_template("contact.html",title=title)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


def send_mail(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(my_email, password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=my_email,
                            msg=email_message)

@app.post("/form-entry")
def receive_data():
    data=request.form
    send_mail(data["name"], data["email"], data["phone"], data["message"])
    title = "Successfully sent your message"
    return render_template("contact.html", title=title)

class loginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField(label="Log In")
    app.secret_key = "some secret string"

@app.route("/login", methods=["GET","POST"])
def login():
    form = loginForm()
    if form.validate_on_submit():
       if form.email.data == "admin@email.com" and form.password.data=="12345678":
           return render_template("login.html")


    return render_template("login.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5001)

