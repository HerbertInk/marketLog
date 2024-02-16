from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
import pyodbc

# offshopsettlements.py file handles interactions; add, retrieve and  update
# of the offshop table in the MsAccess database
# it renders offshopsettlementsadd.html and offshopsettlementsupdate.html in templates/offshopsettlements

# main.py coordination
offshopsettlements_blueprint = Blueprint('offshopsettlements', __name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'offshopsettlements2024'

# db driver
DB_DRIVER = '{Microsoft Access Driver (*.mdb, *.accdb)}'

# database file path
DB_FILE = r'C:\Users\lenovo\Desktop\MarketJournal\marketLog\database\data\data.accdb'  

# establish a connection to the database
conn_str = f'DRIVER={DB_DRIVER};DBQ={DB_FILE}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# coordinated index route for offshopsettlements
@offshopsettlements_blueprint.route('/offshopsettlements')
def index():
    # displays the list of records from the offshop table
    cursor.execute('SELECT * FROM offshop')
    records = cursor.fetchall()
    return render_template('offshopsettlements/offshopsettlementsadd.html', records=records)

# coordinated route for adding records
@offshopsettlements_blueprint.route('/offshopsettlements/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        offshopID = request.form['offshopID']
        transactionDate = request.form['transactionDate'] 
        marketDebt = request.form['marketDebt']
        marketPayment = request.form['marketpayment'] 
        settlementAmount = request.form['settlementAmount']
        transactionPersona = request.form['transactionPersona']

        # 'transactiondate', It works ::differs from db field title
        # 'marketpayment', It works ::differs from db field title

        try:
            # check if offshopID already exists
            cursor.execute(f"SELECT * FROM offshop WHERE offshopID='{offshopID}'")
            existing_record = cursor.fetchone()

            if existing_record:
                flash(f'Record with similar ID {offshopID} exists. \nChange offshopID.', 'warning')
            else:
                # Insert the new record
                cursor.execute("INSERT INTO offshop (offshopID, transactionDate, marketDebt, marketPayment, settlementAmount, transactionPersona) "
                               f"VALUES ('{offshopID}', '{transactionDate}', '{marketDebt}', '{marketPayment}', '{settlementAmount}', '{transactionPersona}')")
                conn.commit()
                flash(f'Record {offshopID} added', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('offshopsettlements.index'))

# coordinated route for retrieval of records by ID
@offshopsettlements_blueprint.route('/offshopsettlements/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        offshopID = request.form['offshopID']

        try:
            # on having a cursor and connection set up
            cursor.execute(f"SELECT * FROM offshop WHERE offshopID='{offshopID}'")
            record = cursor.fetchone()

            if record:
                # converts the record to a dictionary for easy access in the template
                record_dict = {
                    'offshopID': record.offshopID,
                    'transactionDate': record.transactiondate, 
                    'marketDebt': record.marketdebt, 
                    'marketPayment': record.marketpayment,
                    'settlementAmount': record.settlementAmount,
                    'transactionPersona': record.transactionPersona,

                    # .transactiondate, It works ::differs from db field title
                    # .marketdebt, It works ::differs from db field title
                    # .marketpayment, It works ::differs from db field title
                }

                return render_template('offshopsettlements/offshopsettlementsupdate.html', record=record_dict)
            
            else:
                flash(f'Record {offshopID} \nNot found', 'danger')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('offshopsettlements/offshopsettlementsupdate.html', record=None)

# coordinated route for updating records by ID
@offshopsettlements_blueprint.route('/offshopsettlements/update_record', methods=['POST'])
def update_record():
    if request.method == 'POST':
        offshopID = request.form['offshopID']
        transactionDate = request.form['transactionDate']
        marketDebt = request.form['marketDebt']
        marketPayment = request.form['marketPayment']
        settlementAmount = request.form['settlementAmount']
        transactionPersona = request.form['transactionPersona']

        try:
            # updates the record in the database
            cursor.execute(f"UPDATE offshop SET marketDebt='{marketDebt}',  transactionDate='{transactionDate}', marketPayment='{marketPayment}', "
                           f"settlementAmount='{settlementAmount}', transactionPersona='{transactionPersona}' WHERE offshopID='{offshopID}'")
            conn.commit()

            flash(f'Record {offshopID} updated', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('offshopsettlements.update'))

