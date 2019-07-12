from flask import Flask
from flaskext.mysql import MySQL

app= Flask(__name__)
app.secret_key="secret_key"


mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mynewpassword'
app.config['MYSQL_DATABASE_DB'] = 'register'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)