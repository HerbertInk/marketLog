from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
import pyodbc

# inventory.py file handles interactions; add, retrieve and  update
# of the inventoryOut table in the MsAccess database
# it renders inventoryadd.html and inventoryupdate.html in templates/inventory

# main.py coordination
inventory_blueprint = Blueprint('inventory', __name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'inventory2024'

# db driver
DB_DRIVER = '{Microsoft Access Driver (*.mdb, *.accdb)}'

# database file path
DB_FILE = r'C:\Users\lenovo\Desktop\MarketJournal\marketLog\database\data\data.accdb'  

# establish a connection to the database
conn_str = f'DRIVER={DB_DRIVER};DBQ={DB_FILE}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# coordinated index route for inventory
@inventory_blueprint.route('/inventory')
def index():
    # displays the list of records from the inventoryOut table
    cursor.execute('SELECT * FROM inventoryOut')
    records = cursor.fetchall()
    return render_template('inventory/inventoryadd.html', records=records)

# coordinated route for adding records
@inventory_blueprint.route('/inventory/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        invID = request.form['invID']
        invDate = request.form['invDate']
        productOut = request.form['productOut']
        quantityOut = request.form['quantityOut']

        try:
            # check if invID already exists
            cursor.execute(f"SELECT * FROM inventoryOut WHERE invID='{invID}'")
            existing_record = cursor.fetchone()

            if existing_record:
                flash(f'Inventory record with similar ID {invID} exists. \nChange Inventory ID!', 'warning')
            else:
                # Insert the new record
                cursor.execute("INSERT INTO inventoryOut (invID, invDate, productOut, quantityOut) "
                               f"VALUES ('{invID}', '{invDate}', '{productOut}', '{quantityOut}')")
                conn.commit()
                flash(f'inventory record {invID} added', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('inventory.index'))

# coordinated route for retrieval of records by ID
@inventory_blueprint.route('/inventory/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        invID = request.form['invID']

        try:
            # on having a cursor and connection set up
            cursor.execute(f"SELECT * FROM inventoryOut WHERE invID='{invID}'")
            record = cursor.fetchone()

            if record:
                # converts the record to a dictionary for easy access in the template
                record_dict = {
                    'invID': record.invID,
                    'invDate': record.invDate,
                    'productOut': record.productOut,
                    'quantityOut': record.quantityOut,
                    
                }

                return render_template('inventory/inventoryupdate.html', record=record_dict)
            
            else:
                flash(f'Inventory record {invID} \nNot found', 'danger')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('inventory/inventoryupdate.html', record=None)

# coordinated route for updating records by ID
@inventory_blueprint.route('/inventory/update_record', methods=['POST'])
def update_record():
    if request.method == 'POST':
        invID = request.form['invID']
        invDate = request.form['invDate']
        productOut = request.form['productOut']
        quantityOut = request.form['quantityOut']

        try:
            # updates the record in the database
            cursor.execute(f"UPDATE inventoryOut SET invDate='{invDate}', productOut='{productOut}', quantityOut='{quantityOut}' "
                           f" WHERE invID='{invID}'")
            conn.commit()

            flash(f'Inventory record {invID} updated ', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('inventory.update'))

