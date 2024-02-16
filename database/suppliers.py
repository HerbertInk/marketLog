from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
import pyodbc

# suppliers.py file handles interactions; add, retrieve and  update
# of the supplierinfo table in the MsAccess database
# it renders suppliersadd.html and suppliersupdate.html in templates/suppliers

# main.py coordination
suppliers_blueprint = Blueprint('suppliers', __name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'suppliers2024'

# db driver
DB_DRIVER = '{Microsoft Access Driver (*.mdb, *.accdb)}'

# database file path
DB_FILE = r'C:\Users\lenovo\Desktop\MarketJournal\marketLog\database\data\data.accdb'  

# establish a connection to the database
conn_str = f'DRIVER={DB_DRIVER};DBQ={DB_FILE}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# coordinated index route for suppliers
@suppliers_blueprint.route('/suppliers')
def index():
    # displays the list of records from the supplierinfo table
    cursor.execute('SELECT * FROM supplierinfo')
    records = cursor.fetchall()
    return render_template('suppliers/suppliersadd.html', records=records)

# coordinated route for adding records
@suppliers_blueprint.route('/suppliers/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        supplierID = request.form['supplierID']
        supplyDate = request.form['supplyDate']
        suppliedProduct = request.form['suppliedProduct']
        quantity = request.form['quantity']
        unitPrice = request.form['unitPrice']
        totalpurchasePrice = request.form['totalpurchasePrice']
        supplierNote = request.form['supplierNote']

        try:
            # check if supplierID already exists
            cursor.execute(f"SELECT * FROM supplierinfo WHERE supplierID='{supplierID}'")
            existing_record = cursor.fetchone()

            if existing_record:
                flash(f'Record with similar ID {supplierID} exists.\nChange the supplierID!', 'warning')
            else:
                # Insert the new record
                cursor.execute("INSERT INTO supplierinfo (supplierID, supplyDate, suppliedProduct, quantity, unitPrice, totalpurchasePrice, supplierNote) "
                               f"VALUES ('{supplierID}', '{supplyDate}', '{suppliedProduct}', '{quantity}', '{unitPrice}', '{totalpurchasePrice}', '{supplierNote}')")
                conn.commit()
                flash(f'Record {supplierID} added', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('suppliers.index'))

# coordinated route for retrieval of records by ID
@suppliers_blueprint.route('/suppliers/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        supplierID = request.form['supplierID']

        try:
            # on having a cursor and connection set up
            cursor.execute(f"SELECT * FROM supplierinfo WHERE supplierID='{supplierID}'")
            record = cursor.fetchone()

            if record:
                # converts the record to a dictionary for easy access in the template
                record_dict = {
                    'supplierID': record.supplierID,
                    'supplyDate': record.supplyDate,
                    'suppliedProduct': record.suppliedProduct,
                    'quantity': record.quantity,
                    'unitPrice': record.unitPrice,
                    'totalpurchasePrice': record.totalpurchasePrice,
                    'supplierNote': record.supplierNote,
                }

                return render_template('suppliers/suppliersupdate.html', record=record_dict)
            
            else:
                flash(f'Record with supplierID {supplierID} \nNot found', 'danger')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('suppliers/suppliersupdate.html', record=None)

# coordinated route for updating records by ID
@suppliers_blueprint.route('/suppliers/update_record', methods=['POST'])
def update_record():
    if request.method == 'POST':
        supplierID = request.form['supplierID']
        supplyDate = request.form['supplyDate']
        suppliedProduct = request.form['suppliedProduct']
        quantity = request.form['quantity']
        unitPrice = request.form['unitPrice']
        totalpurchasePrice = request.form['totalpurchasePrice']
        supplierNote = request.form['supplierNote']

        try:
            # updates the record in the database
            cursor.execute(f"UPDATE supplierinfo SET  supplyDate='{supplyDate}', suppliedProduct='{suppliedProduct}', quantity='{quantity}', "
                           f"unitPrice='{unitPrice}', totalpurchasePrice='{totalpurchasePrice}', supplierNote='{supplierNote}' WHERE supplierID='{supplierID}'")
            conn.commit()

            flash(f'Record {supplierID} updated', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('suppliers.update'))

