# main.py file :: for table file connections using blueprint
from flask import Flask, render_template, redirect, url_for
from config import configure_app

from otc import otc_blueprint
from checkLog import check_log_blueprint
from marketsales import marketsales_blueprint
from suppliers import suppliers_blueprint
from payments import payments_blueprint
from offshopsettlements import offshopsettlements_blueprint
from expenditures import expenditures_blueprint
from inventory import inventory_blueprint


app = Flask(__name__)
app.config['SECRET_KEY'] = '125-695-083'

configure_app(app)

# register blueprints
app.register_blueprint(otc_blueprint)
app.register_blueprint(check_log_blueprint)
app.register_blueprint(marketsales_blueprint)
app.register_blueprint(suppliers_blueprint)
app.register_blueprint(payments_blueprint)
app.register_blueprint(offshopsettlements_blueprint)
app.register_blueprint(expenditures_blueprint)
app.register_blueprint(inventory_blueprint)

# marketLog webapp route
@app.route('/')
def index():
    # route can customized with respect to ones requirements
    return render_template('otc/add.html')

# debug=True/False debug mode on/off
# T continuous logs on changes, immediate reflection ::F minimal logs and reflection of changes on re-run
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
