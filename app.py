from flask import Flask, render_template, redirect, url_for, request
from config import Config
from models import db, User, Image, Vote
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@login_required
def index():
    images = Image.query.all()
    data = []
    for image in images:
        likes = Vote.query.filter_by(image_id=image.id, value=1).count()
        dislikes = Vote.query.filter_by(image_id=image.id, value=-1).count()
        data.append({"image": image, "likes": likes, "dislikes": dislikes})
    return render_template("index.html", data=data)

@app.route("/vote/<int:image_id>/<int:value>")
@login_required
def vote(image_id, value):
    existing = Vote.query.filter_by(user_id=current_user.id, image_id=image_id).first()
    if existing:
        existing.value = value
    else:
        vote = Vote(user_id=current_user.id, image_id=image_id, value=value)
        db.session.add(vote)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash = generate_password_hash(password)
        user = User(username=username, password=hash)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if Image.query.count() == 0:
            images = [
                Image(filename="img1.jpg"),
                Image(filename="img2.jpg"),
                Image(filename="img3.jpg"),
            ]
            db.session.add_all(images)
            db.session.commit()
    app.run(debug=True)
