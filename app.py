import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
import razorpay 

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/ACER/Documents/Anuj/Python/Backend With Flask/Razorpay1/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)


class User ( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(15))
    name = db.Column(db.String(50))
    amount = db.Column(db.String(80))

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        amount = request.form.get("amount")

        user = User(email=email, name=name, amount=amount)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for("pay", id = user.id))



    return render_template("index.html")


@app.route("/pay/<id>", methods=["GET", "POST"])
def pay(id):
    user = User.query.filter_by(id=id).first()

    client = razorpay.Client(auth = ("rzp_test_llt8cDdBzQUFhA", "DWhDK5zDindwS9hpM3vDCYxW"))
    payment = client.order.create({"amount" : (int(user.amount) * 100), "currency" : "INR", "payment_capture" : "1"})


    return render_template("pay.html", payment = payment)


@app.route("/success", methods=["GET", "POST"])
def success():
    return render_template("success.html")

