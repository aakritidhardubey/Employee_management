from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)

# Use environment variable for database URL in production, fallback to SQLite for development
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', 'sqlite:///employee.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Employee(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    

@app.route('/', methods=['GET','POST'])
def home():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        employee=Employee(name= name,email=email)
        db.session.add(employee)
        db.session.commit()
    employees = Employee.query.all()
    return render_template("home.html", employees=employees)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contacts')
def contacts():
    return render_template("contacts.html")

@app.route('/delete/<int:sno>')
def delete(sno):
    employee=Employee.query.filter_by(sno=sno).first()
    db.session.delete(employee)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    employee = Employee.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.email = request.form['email']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', employee=employee)


# Initialize database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)