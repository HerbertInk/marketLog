from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
import pyodbc

# payments.py file handles interactions; add, retrieve and  update
# of the pay table in the MsAccess database
# it renders paymentsadd.html and paymentsupdate.html in templates/payments

# main.py coordination
payments_blueprint = Blueprint('payments', __name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'payments2024'

# db driver
DB_DRIVER = '{Microsoft Access Driver (*.mdb, *.accdb)}'

# database file path
DB_FILE = r'C:\Users\lenovo\Desktop\MarketJournal\marketLog\database\data\data.accdb'  

# establish a connection to the database
conn_str = f'DRIVER={DB_DRIVER};DBQ={DB_FILE}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# coordinated index route for payments
@payments_blueprint.route('/payments')
def index():
    # displays the list of records from the pay table
    cursor.execute('SELECT * FROM pay')
    records = cursor.fetchall()
    return render_template('payments/paymentsadd.html', records=records)

# coordinated route for adding records
@payments_blueprint.route('/payments/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        payID = request.form['payID']
        paymentDate = request.form['paymentDate']
        userName = request.form['userName']
        paymentAmount = request.form['paymentAmount']
        paymentReason = request.form['paymentReason']

        try:
            # check if payID already exists
            cursor.execute(f"SELECT * FROM pay WHERE payID='{payID}'")
            existing_record = cursor.fetchone()

            if existing_record:
                flash(f'Payment with similar ID {payID} exists.\nChange Payment ID!', 'warning')
            else:
                # Insert the new record
                cursor.execute("INSERT INTO pay (payID, paymentDate, userName, paymentAmount, paymentReason) "
                               f"VALUES ('{payID}', '{paymentDate}', '{userName}', '{paymentAmount}', '{paymentReason}')")
                conn.commit()
                flash(f'Payment {payID} added', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('payments.index'))

# coordinated route for retrieval of records by ID
@payments_blueprint.route('/payments/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        payID = request.form['payID']

        try:
            # on having a cursor and connection set up
            cursor.execute(f"SELECT * FROM pay WHERE payID='{payID}'")
            record = cursor.fetchone()

            if record:
                # converts the record to a dictionary for easy access in the template, cool right
                record_dict = {
                    'payID': record.payID,
                    'paymentDate': record.paymentdate,
                    'userName': record.userName,
                    'paymentAmount': record.paymentAmount,
                    'paymentReason': record.paymentReason,
                }

                return render_template('payments/paymentsupdate.html', record=record_dict)
            
            else:
                flash(f'Payment with ID {payID} \nNot found!', 'danger')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('payments/paymentsupdate.html', record=None)

# coordinated route for updating records by ID
@payments_blueprint.route('/payments/update_record', methods=['POST'])
def update_record():
    if request.method == 'POST':
        payID = request.form['payID']
        paymentDate = request.form['paymentdate']
        userName = request.form['userName']
        paymentAmount = request.form['paymentAmount']
        paymentReason = request.form['paymentReason']
        
        # paymentdate, It works ::differs from db field title

        try:
            # updates the record in the database
            cursor.execute(f"UPDATE pay SET userName='{userName}',  paymentDate='{paymentDate}', "
                           f"paymentAmount='{paymentAmount}', paymentReason='{paymentReason}' WHERE payID='{payID}'")
            conn.commit()

            flash(f'Payment {payID} updated', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('payments.update'))

