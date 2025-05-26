from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import db, Cycle, User

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    if not User.query.first():
        db.session.add(User(email='admin@cycles.com', password='123456'))
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.password == request.form['password']:
            session['user'] = user.email
            return redirect(url_for('dashboard'))
        return "Login failed"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    cycles = Cycle.query.all()
    return render_template('dashboard.html', cycles=cycles)

@app.route('/add_cycle', methods=['POST'])
def add_cycle():
    if 'user' not in session:
        return redirect('/')
    new_cycle = Cycle(
        brand=request.form['brand'],
        model=request.form['model'],
        quantity=int(request.form['quantity']),
        price=float(request.form['price'])
    )
    db.session.add(new_cycle)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete/<int:id>')
def delete_cycle(id):
    if 'user' not in session:
        return redirect('/')
    Cycle.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
