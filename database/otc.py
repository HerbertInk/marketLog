from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
import pyodbc

# otc.py file handles interactions; add, retrieve and  update
# of the marketLog table in the MsAccess database
# it renders add.html and update.html in templates/otc

# main.py coordination
otc_blueprint = Blueprint('otc', __name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'otc2024'

# db driver
DB_DRIVER = '{Microsoft Access Driver (*.mdb, *.accdb)}'

# database file path
DB_FILE = r'C:\Users\lenovo\Desktop\MarketJournal\marketLog\database\data\data.accdb'  

# establish a connection to the database
conn_str = f'DRIVER={DB_DRIVER};DBQ={DB_FILE}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# coordinated index route for otc
@otc_blueprint.route('/otc')
def index():
    # displays the list of records from the marketLog table
    cursor.execute('SELECT * FROM marketLog')
    records = cursor.fetchall()
    return render_template('otc/add.html', records=records)

# coordinated route for adding records
@otc_blueprint.route('/otc/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        salesID = request.form['salesID']
        saleDate = request.form['saleDate']
        product = request.form['product']
        quantity = request.form['quantity']
        unitPrice = request.form['unitPrice']
        productSale = request.form['productSale']

        try:
            # check if salesID already exists
            cursor.execute(f"SELECT * FROM marketLog WHERE salesID='{salesID}'")
            existing_record = cursor.fetchone()

            if existing_record:
                flash(f'Sale with similar ID {salesID} exists. \nChange Sales ID!', 'warning')
            else:
                # Insert the new record
                cursor.execute("INSERT INTO marketLog (salesID,  saleDate, product, quantity, unitPrice, productSale) "
                               f"VALUES ('{salesID}', '{saleDate}', '{product}', '{quantity}', '{unitPrice}', '{productSale}')")
                conn.commit()
                flash(f'Sale {salesID} added', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('otc.index'))

# coordinated route for retrieval of records by ID
@otc_blueprint.route('/otc/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        salesID = request.form['salesID']

        try:
            # on having a cursor and connection set up
            cursor.execute(f"SELECT * FROM marketLog WHERE salesID='{salesID}'")
            record = cursor.fetchone()

            if record:
                # converts the record to a dictionary for easy access in the template
                record_dict = {
                    'salesID': record.salesID,
                    'saleDate': record.saleDate,
                    'product': record.product,
                    'quantity': record.quantity,
                    'unitPrice': record.unitprice,
                    'productSale': record.productsale,
                }

                return render_template('otc/update.html', record=record_dict)
            
            else:
                flash(f'Sale record  {salesID} \nNot found', 'danger')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('otc/update.html', record=None)

# coordinated route for updating records by ID
@otc_blueprint.route('/otc/update_record', methods=['POST'])
def update_record():
    if request.method == 'POST':
        salesID = request.form['salesID']
        saleDate = request.form['saleDate']
        product = request.form['product']
        quantity = request.form['quantity']
        unitPrice = request.form['unitPrice'] # unitPrice, It works ::differs from db field title
        productSale = request.form['productSale'] # productSale, It works ::differs from db field title

        try:
            # updates the record in the database
            cursor.execute(f"UPDATE marketLog SET saleDate='{saleDate}', product='{product}', quantity='{quantity}', "
                           f" unitPrice='{unitPrice}', productSale='{productSale}' WHERE salesID='{salesID}'")
            conn.commit()

            flash(f'Sales record {salesID} updated', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('otc.update'))

