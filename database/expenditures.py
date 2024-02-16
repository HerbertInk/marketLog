from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
import pyodbc

# expenditures.py file handles interactions; add, retrieve and  update
# of the expenses table in the MsAccess database
# it renders expendituresadd.html and expendituresupdate.html in templates/expenditures

# main.py coordination
expenditures_blueprint = Blueprint('expenditures', __name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'expenditures2024'

# db driver
DB_DRIVER = '{Microsoft Access Driver (*.mdb, *.accdb)}'

# database file path
DB_FILE = r'C:\Users\lenovo\Desktop\MarketJournal\marketLog\database\data\data.accdb'  

# establish a connection to the database
conn_str = f'DRIVER={DB_DRIVER};DBQ={DB_FILE}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# coordinated index route for expenditures
@expenditures_blueprint.route('/expenditures')
def index():
    # displays the list of records from the expenses table
    cursor.execute('SELECT * FROM expenses')
    records = cursor.fetchall()
    return render_template('expenditures/expendituresadd.html', records=records)

# coordinated route for adding records
@expenditures_blueprint.route('/expenditures/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        expID = request.form['expID']
        incurredDate = request.form['incurredDate']
        userItem = request.form['userItem']
        quantity = request.form['quantity']
        unitPrice = request.form['unitPrice']
        totalExpenditure = request.form['totalExpenditure']

        try:
            # check if expID already exists
            cursor.execute(f"SELECT * FROM expenses WHERE expID='{expID}'")
            existing_record = cursor.fetchone()

            if existing_record:
                flash(f'Expenditure record with similar Expenditure ID{expID}exists. \nChange Expenditure ID.', 'warning')
            else:
                # Insert the new record
                cursor.execute("INSERT INTO expenses (expID, incurredDate, userItem, quantity, unitPrice, totalExpenditure) "
                               f"VALUES ('{expID}', '{incurredDate}', '{userItem}', '{quantity}', '{unitPrice}', '{totalExpenditure}')")
                conn.commit()
                flash(f'Expenditure {expID} added', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('expenditures.index'))

# coordinated route for retrieval of records by ID
@expenditures_blueprint.route('/expenditures/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        expID = request.form['expID']

        try:
            # on having a cursor and connection set up
            cursor.execute(f"SELECT * FROM expenses WHERE expID='{expID}'")
            record = cursor.fetchone()

            if record:
                # converts the record to a dictionary for easy access in the template
                record_dict = {
                    'expID': record.expID,
                    'incurredDate': record.incurreddate,
                    'userItem': record.userItem,
                    'quantity': record.quantity,
                    'unitPrice': record.unitPrice,
                    'totalExpenditure': record.totalExpenditure,
                    
                    # .record.incurreddate, It works ::differs from db field title
                }

                return render_template('expenditures/expendituresupdate.html', record=record_dict)
            
            else:
                flash(f'Expenditure record {expID} not found', 'danger')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('expenditures/expendituresupdate.html', record=None)

# coordinated route for updating records by ID
@expenditures_blueprint.route('/expenditures/update_record', methods=['POST'])
def update_record():
    if request.method == 'POST':
        expID = request.form['expID']
        incurredDate = request.form['incurredDate']
        userItem = request.form['userItem']
        quantity = request.form['quantity']
        unitPrice = request.form['unitPrice']
        totalExpenditure = request.form['totalExpenditure']

        try:
            # updates the record in the database
            cursor.execute(f"UPDATE expenses SET userItem='{userItem}',  incurredDate='{incurredDate}', quantity='{quantity}', "
                           f"unitPrice='{unitPrice}', totalExpenditure='{totalExpenditure}' WHERE expID='{expID}'")
            conn.commit()

            flash(f'Expenditure record {expID} updated', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('expenditures.update'))

