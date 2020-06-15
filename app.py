from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
# ###########################
# Database Configuration
# 
# Note: Kindly make sure the status is any one of the following: Active, Closed, Pending <Some Activity> 
# ###########################

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer.db'
db = SQLAlchemy(app)


class Customer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    ssnid = db.Column(db.Integer(), unique=True, nullable=False)
    accountId = db.Column(db.Integer(), nullable=False)
    accountBalance = db.Column(db.Integer(), nullable=False)
    account_type = db.Column(db.String(1), nullable=False)
    status = db.Column(db.Text, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    message = db.Column(db.Text, nullable=False)


    def __init__(self, ssnid, accountId, accountBalance, account_type, status, message):
        self.ssnid = ssnid
        self.accountId = accountId
        self.accountBalance = accountBalance
        self.account_type = account_type
        self.status = status
        self.message = message
        

    def __repr__(self):
        return "Customer id: "+str(self.id)

# ###########################
# Initializing Dummy Data (Run in Python Terminal)
# ###########################

# from app import db
# from app import Customer
# db.create_all()

# db.session.add(Customer(ssnid=518612602, accountId=553794213, accountBalance=10000, account_type='S', status='Pending Approval', message='Just Created'))
# db.session.add(Customer(ssnid=372781404, accountId=310556749, accountBalance=2000, account_type='C', status='Active', message='Nothing'))
# db.session.add(Customer(ssnid=177513079, accountId=500864310, accountBalance=500000, account_type='S', status='Pending Approval', message='NA'))
# db.session.add(Customer(ssnid=196751448, accountId=546723186, accountBalance=1000000, account_type='S', status='Pending Approval', message='NA'))
# db.session.add(Customer(ssnid=388288542, accountId=620951719, accountBalance=10, account_type='C', status='Closed', message='Closed due to low balance'))

# db.session.commit()

# ###########################
# Routing
# ###########################

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/CustomerStatus')
def CustomerStatus():
    all_customer = Customer.query.all()
    return render_template('customer-Status.html', rows=all_customer)

@app.route('/AccountStatus')
def AccountStatus():
    all_account = Customer.query.all()
    return render_template('account-Status.html', rows=all_account)

@app.route('/CustomerSearch', methods=['GET', 'POST'])
def CustomerSearch():
    if request.method == 'POST':
       
        if 'cid' in request.form:
            cid = request.form['cid']
            results = db.session.query(Customer).filter(Customer.id == cid)
            return render_template('customer-Search.html', result=results)
        else:
            ssnid = request.form['ssnid']
            results = db.session.query(Customer).filter(Customer.ssnid == ssnid)
            return render_template('customer-Search.html', result=results)
    else:   
        return render_template('customer-Search.html')

@app.route('/AccountSearch', methods=['GET', 'POST'])
def AccountSearch():
    if request.method == 'POST':
       
        if 'accid' in request.form:
            accid = request.form['accid']
            results = db.session.query(Customer).filter(Customer.accountId == accid)
            return render_template('account-Search.html', result=results)
        else:
            cid = request.form['cid']
            results = db.session.query(Customer).filter(Customer.id == cid)
            return render_template('account-Search.html', result=results)
    else:   
        return render_template('account-Search.html')

@app.route('/Deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        accid = request.form['accid']
        results = db.session.query(Customer).filter(Customer.accountId == accid)
        return render_template('Deposit.html',result=results)

@app.route("/update", methods=["GET","POST"])
def update():
    if request.method == 'POST':
        newb = request.form.get("dep")
        oldb = request.form.get("oldbalance")
        accid=request.form.get("accid")
        cust = Customer.query.filter_by(accountId=accid).first()
        cust.accountBalance = (int)(oldb)+(int)(newb)
        db.session.commit()
    all_account = Customer.query.all()
    return redirect("/AccountStatus")


@app.route('/withdraw')
def withdraw():
    return render_template('withdraw.html')

if __name__ == '__main__':
    app.run(debug=True)
