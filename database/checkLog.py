from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
import pyodbc

# checkLog.py file handles interactions; add, retrieve and  update
# of the checkLog table in the MsAccess database
# it renders checkadd.html and checkupdate.html in /templates folder

# main.py coordination
check_log_blueprint = Blueprint('check_log', __name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'checkLog'

# db driver
DB_DRIVER = '{Microsoft Access Driver (*.mdb, *.accdb)}'

# database file path
DB_FILE = r'C:\Users\lenovo\Desktop\MarketJournal\marketLog\database\data\data.accdb'

# establish a connection to the database
conn_str = f'DRIVER={DB_DRIVER};DBQ={DB_FILE}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# coordinated index route for checkLOg
@check_log_blueprint.route('/dnd')
def indexthat():
    # displays the list of records from checkLog table
    cursor.execute('SELECT * FROM checkLog')
    records = cursor.fetchall()
    return render_template('checkadd.html', records=records)

# coordinated route for adding records
@check_log_blueprint.route('/addthat', methods=['GET', 'POST'])
def addthat():
    if request.method == 'POST':
        checkID = request.form['checkID']
        userName = request.form['userName']
        userAge = request.form['userAge']
        Birthday = request.form['birthDay'] # 'birthDay', It works ::differs from db field title

        try:
            # check if salesID already exists
            cursor.execute(f"SELECT * FROM checkLog WHERE checkID='{checkID}'")
            existing_record = cursor.fetchone()

            if existing_record:
                flash(f'User {checkID} already exists. \nTry Again.', 'warning')
            else:
                # Insert the new record
                cursor.execute("INSERT INTO checkLog (checkID, userName, userAge, Birthday) "
                            f"VALUES ('{checkID}', '{userName}', '{userAge}', '{Birthday}')")
                conn.commit()

                flash(f'User {checkID} added', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('check_log.indexthat'))

# coordinated route for retrieval of records by ID
@check_log_blueprint.route('/updatethat', methods=['POST', 'GET'])
def updatethat():
    if request.method == 'POST':
        checkID = request.form['checkID']

        try:
            # on having a cursor and connection set up
            cursor.execute(f"SELECT * FROM checkLog WHERE checkID='{checkID}'")
            record = cursor.fetchone()

            if record:
                # converts the record to a dictionary for easy access in the template
                record_dict = {
                    'checkID': record.checkID,
                    'userName': record.userName,
                    'userAge': record.userAge,
                    'Birthday': record.Birthday,
                }

                return render_template('checkupdate.html', record=record_dict)
            
            else:
                flash(f'User {checkID} not found', 'danger')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('checkupdate.html', record=None)

# coordinated route for updating records by ID
@check_log_blueprint.route('/update_recordthat', methods=['POST'])
def update_recordthat():
    if request.method == 'POST':
        checkID = request.form['checkID']
        userName = request.form['userName']
        userAge = request.form['userAge']
        Birthday = request.form['Birthday']

        try:
            # updates the record in the database
            cursor.execute(f"UPDATE checkLog SET userName='{userName}', userAge='{userAge}', "
                        f"Birthday='{Birthday}' WHERE checkID='{checkID}'")
            conn.commit()

            flash('User profile updated', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('check_log.updatethat'))

