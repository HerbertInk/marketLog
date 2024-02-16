from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
import pyodbc

# marketsales.py file handles interactions; add, retrieve and  update
# of the marketeers table in the MsAccess database
# it renders marketsalesadd.html and marketsalesupdate.html in templates/marketsales

# main.py coordination
marketsales_blueprint = Blueprint('marketsales', __name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'marketsales2024'

# db driver
DB_DRIVER = '{Microsoft Access Driver (*.mdb, *.accdb)}'

# database file path
DB_FILE = r'C:\Users\lenovo\Desktop\MarketJournal\marketLog\database\data\data.accdb'  

# establish a connection to the database
conn_str = f'DRIVER={DB_DRIVER};DBQ={DB_FILE}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# coordinated index route for marketsales
@marketsales_blueprint.route('/marketsales')
def index():
    # displays the list of records from the marketeers table
    cursor.execute('SELECT * FROM marketeers')
    records = cursor.fetchall()
    return render_template('marketsales/marketsalesadd.html', records=records)

# coordinated route for adding records
@marketsales_blueprint.route('/marketsales/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        marketsaleID = request.form['marketsaleID']
        saleDate = request.form['saleDate']
        product = request.form['product']
        quantity = request.form['quantity']
        unitPrice = request.form['unitPrice']
        totalsalePrice = request.form['totalsalePrice']
        marketNote = request.form['marketNote']

        try:
            # check if marketsaleID already exists
            cursor.execute(f"SELECT * FROM marketeers WHERE marketsaleID='{marketsaleID}'")
            existing_record = cursor.fetchone()

            if existing_record:
                flash(f'Record with similar ID {marketsaleID} exists \nChange the Marketsale ID.', 'warning')
            else:
                # Insert the new record
                cursor.execute("INSERT INTO marketeers (marketsaleID, saleDate, product, quantity, unitPrice, totalsalePrice, marketNote) "
                            f"VALUES ('{marketsaleID}', '{saleDate}', '{product}', '{quantity}', '{unitPrice}', '{totalsalePrice}', '{marketNote}')")
                conn.commit()
                flash(f'Marketsale record {marketsaleID} added', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('marketsales.index'))

# coordinated route for retrieval of records by ID
@marketsales_blueprint.route('/marketsales/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        marketsaleID = request.form['marketsaleID']

        try:
            # on having a cursor and connection set up
            cursor.execute(f"SELECT * FROM marketeers WHERE marketsaleID='{marketsaleID}'")
            record = cursor.fetchone()

            if record:
                # converts the record to a dictionary for easy access in the template
                record_dict = {
                    'marketsaleID': record.marketsaleID,
                    'saleDate': record.saleDate,
                    'product': record.product,
                    'quantity': record.quantity,
                    'unitPrice': record.unitPrice,
                    'totalsalePrice': record.totalsalePrice,
                    'marketNote': record.marketNote,
                }

                return render_template('marketsales/marketsalesupdate.html', record=record_dict)
            
            else:
                flash(f'Marketsale record {marketsaleID} \nNot found', 'danger')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('marketsales/marketsalesupdate.html', record=None)

# coordinated route for updating records by ID
@marketsales_blueprint.route('/marketsales/update_record', methods=['POST'])
def update_record():
    if request.method == 'POST':
        marketsaleID = request.form['marketsaleID']
        saleDate = request.form['saleDate']
        product = request.form['product']
        quantity = request.form['quantity']
        unitPrice = request.form['unitPrice']
        totalsalePrice = request.form['totalsalePrice']
        marketNote = request.form['marketNote']

        try:
            # updates the record in the database
            cursor.execute(f"UPDATE marketeers SET product='{product}',  saleDate='{saleDate}', quantity='{quantity}', "
                           f"unitPrice='{unitPrice}', totalsalePrice='{totalsalePrice}', marketNote='{marketNote}' WHERE marketsaleID='{marketsaleID}'")
            conn.commit()

            flash(f'Marketsale record {marketsaleID} updated', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('marketsales.update'))

# ::task in queue -- the marketNote field; /MsAccess ... marked not required