from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
import pymysql
from db_config import mysql,app

from passlib.hash import sha256_crypt
engine = create_engine("mysql+pymysql://root:mynewpassword@localhost/register")

db=scoped_session(sessionmaker(bind=engine))

@app.route('/add', methods=['POST'])
def add_user():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()	
		_name = request.form['Name']
		_price = request.form['Price']
		_desc = request.form['Description']
		_avail = request.form['Available']
		_cat = request.form['Category']
		_pic = request.form['Picture']
		# validate the received values
		if _name and _price and _desc and _avail and _cat and _pic and request.method == 'POST':
		# save edits
			sql = "INSERT INTO products(Name, Price,Description, Available,Category,Picture) VALUES(%s, %s, %s,%s,%s,%s)"
			data = (_name,_price, _desc, _avail,_cat,_pic)
			cursor.execute(sql, data)
			conn.commit()

			return redirect('/admin')
		else:
			return 'Error while adding user'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/admin')
def admin():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products")
		row = cursor.fetchall()

		return render_template('product.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/loggedin/<int:id>')
def loggedin(id):
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM users WHERE id=%s",(id,) )
		user=cursor.fetchall()
		return render_template("loggedin.html",user=user)
	except:
		return("errorrrr")
	finally:
		cursor.close()
		conn.close()

@app.route('/adminhome')
def adminhome():
	return render_template("admin.html")

@app.route('/cart/<int:product_id>/<int:user_id>')

def cart(product_id,user_id):
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		sql = "INSERT INTO cart(id,product_id) VALUES(%s,%s)"
		data = (user_id,product_id)
		cursor.execute(sql, data)
		conn.commit()
		cursor.execute("SELECT count(product_id) FROM cart WHERE id =%s and product_id=%s",(user_id,product_id,))
		count=cursor.fetchone()
		return ("success")
	except:
		print("errorrrr")
	finally:
		cursor.close()
		conn.close()
@app.route('/cartshow/<int:user_id>')
def cartshow(user_id):
	cart1=db.execute("SELECT * FROM products,cart WHERE products.user_id = cart.product_id and cart.id =:user_id",{"user_id":user_id}).fetchall()
	return render_template('cart.html',cart=cart1)

@app.route('/single/<int:id>')
def single(id):
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE user_id=%s",(id,) )
		row=cursor.fetchall()
		return render_template("single.html",row=row)
	except:
		print("errorrrr")
	finally:
		cursor.close()
		conn.close()
@app.route('/lsingle/<int:id>/<int:id2>')
def lsingle(id,id2):
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE user_id=%s",(id,) )
		user=db.execute("SELECT * FROM users WHERE id=:id2",{"id2":id2}).fetchall()
		row=cursor.fetchall()
		return render_template("lsingle.html",row=row,user=user)
	except:
		print("errorrrr")
	finally:
		cursor.close()
		conn.close()
@app.route('/asingle/<int:id>')
def asingle(id):
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE user_id=%s",(id,) )
		row=cursor.fetchall()
		return render_template("asingle.html",row=row)
	except:
		print("errorrrr")
	finally:
		cursor.close()
		conn.close()
@app.route('/update', methods=['POST'])
def update_user():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		_name = request.form['Name']
		_price = request.form['Price']
		_desc = request.form['Description']
		_avail = request.form['Available']
		_cat = request.form['Category']
		_pic = request.form['Picture']
		_id = request.form['id']
# validate the received values
		if _name and _price and _desc and _avail and _cat and _pic and _id and request.method == 'POST':
# save edits
			sql = "UPDATE products SET Name=%s,Price=%s, Description=%s, Available=%s, Category=%s, Picture=%s WHERE user_id=%s"
			data = (_name,_price, _desc, _avail,_cat,_pic,_id)
			cursor.execute(sql, data)
			conn.commit()
			flash('User updated successfully!')
			return redirect('/admin')
		else:
			return 'Error while updating user'
	except:
		return "Error updating."
	finally:
		cursor.close() 
		conn.close()

@app.route('/delete/<int:id>')
def delete_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM products WHERE user_id=%s", (id,))
		conn.commit()
		return redirect('/admin')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/')
def index():
	return render_template("homepage.html")

@app.route("/register",methods=["GET","POST"])
def register():
	if request.method=="POST":
		name=request.form.get("name")
		username=request.form.get("username")
		password=request.form.get("password")
		confirm=request.form.get("confirm")
		secure_password=sha256_crypt.encrypt(str(password))

	if password == confirm:
		db.execute("INSERT INTO users(name,username,password) VALUES(:name,:username,:password) ", {"name":name,"username":username,"password":secure_password})
		db.commit()
		return render_template('login.html')
	else:
		flash("Password does not match","danger")
		return render_template('homepage.html')
		return render_template('homepage.html')

@app.route("/signup",methods=["GET","POST"])
def signup():
	return render_template('register.html')



@app.route("/login_post",methods=["GET","POST"])
def login_post():
	if request.method == "POST":
		username=request.form.get("name")
		password=request.form.get("password")
		user=db.execute("SELECT * FROM users WHERE username=:username",{"username":username}).fetchall()
		usernamedata = db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
		passwordata = db.execute("SELECT password FROM users WHERE username=:username",{"username":username}).fetchone()
		if usernamedata is None:
			flash("No username","danger")
			return render_template("login.html")
		elif usernamedata==("admin@gmail.com",):
			for passwor_data in passwordata:
				if sha256_crypt.verify(password,passwor_data):
					session["log"]=True
					flash("You are now logged in","success")
					return render_template("admin.html")
				else:
					return render_template("login.html")
		else:
			for passwor_data in passwordata:
				if sha256_crypt.verify(password,passwor_data):
					session["log"]=True
					flash("You are now logged in","success")
					return render_template("loggedin.html",user=user)
				else:
					flash("Try again")
					return render_template('login.html')
@app.route("/logout",methods=["GET","POST"])
def logout():
	session.clear()
	flash("You are now logged out","success")
	return render_template("homepage.html")
@app.route('/back')
def back():
	return render_template("admin.html")
@app.route('/shirts')
def shirts():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='shirts'")
		row = cursor.fetchall()

		return render_template('show.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/lshirts/<int:id>')
def lshirts(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='shirts'")
		row = cursor.fetchall()
		user=db.execute("SELECT * FROM users WHERE id=:id",{"id":id}).fetchall()
		print(user,row)
		return render_template('lshow.html', row=row,user=user)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/ashirts')
def ashirts():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='shirts'")
		row = cursor.fetchall()

		return render_template('ashow.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/tshirts')
def tshirts():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='t-shirts'")
		row = cursor.fetchall()

		return render_template('show.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/ltshirts/<int:id>')
def ltshirts(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='t-shirts'")
		row = cursor.fetchall()
		user=db.execute("SELECT * FROM users WHERE id=:id",{"id":id}).fetchall()
		print(user,row)
		return render_template('lshow.html', row=row,user=user)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
@app.route('/atshirts')
def atshirts():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='t-shirts'")
		row = cursor.fetchall()

		return render_template('ashow.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/trousers')
def trousers():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='trousers'")
		row = cursor.fetchall()

		return render_template('show.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/ltrousers/<int:id>')
def ltrousers(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='trousers'")
		row = cursor.fetchall()
		user=db.execute("SELECT * FROM users WHERE id=:id",{"id":id}).fetchall()
		print(user,row)
		return render_template('lshow.html', row=row,user=user)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
@app.route('/atrousers')
def atrousers():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='trousers'")
		row = cursor.fetchall()

		return render_template('ashow.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/hijabs')
def hijabs():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='hijabs'")
		row = cursor.fetchall()

		return render_template('show.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/lhijabs/<int:id>')
def lhijabs(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='hijabs'")
		row = cursor.fetchall()
		user=db.execute("SELECT * FROM users WHERE id=:id",{"id":id}).fetchall()
		print(user,row)
		return render_template('lshow.html', row=row,user=user)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
@app.route('/ahijabs')
def ahijabs():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='hijabs'")
		row = cursor.fetchall()

		return render_template('ashow.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/sarees')
def sarees():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='sarees'")
		row = cursor.fetchall()

		return render_template('show.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/lsarees/<int:id>')
def lsarees(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='sarees'")
		row = cursor.fetchall()
		user=db.execute("SELECT * FROM users WHERE id=:id",{"id":id}).fetchall()
		print(user,row)
		return render_template('lshow.html', row=row,user=user)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
@app.route('/asarees')
def asarees():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='sarees'")
		row = cursor.fetchall()

		return render_template('ashow.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/belts')
def belts():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='belts'")
		row = cursor.fetchall()

		return render_template('show.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/lbelts/<int:id>')
def lbelts(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='belts'")
		row = cursor.fetchall()
		user=db.execute("SELECT * FROM users WHERE id=:id",{"id":id}).fetchall()
		print(user,row)
		return render_template('lshow.html', row=row,user=user)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
@app.route('/abelts')
def abelts():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='belts'")
		row = cursor.fetchall()

		return render_template('ashow.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/purse')
def purse():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='purse'")
		row = cursor.fetchall()

		return render_template('show.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/lpurse/<int:id>')
def lpurse(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='purse'")
		row = cursor.fetchall()
		user=db.execute("SELECT * FROM users WHERE id=:id",{"id":id}).fetchall()
		print(user,row)
		return render_template('lshow.html', row=row,user=user)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
@app.route('/apurse')
def apurse():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='purse'")
		row = cursor.fetchall()

		return render_template('ashow.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/watches')
def watches():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='watches'")
		row = cursor.fetchall()

		return render_template('show.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/lwatches/<int:id>')
def lwatches(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='watches'")
		row = cursor.fetchall()
		user=db.execute("SELECT * FROM users WHERE id=:id",{"id":id}).fetchall()
		print(user,row)
		return render_template('lshow.html', row=row,user=user)
	except Exception as e:
		print(e)
	finally:
		cursor.close()

@app.route('/awatches')
def awatches():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='watches'")
		row = cursor.fetchall()

		return render_template('ashow.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


if __name__ == '__main__':
	app.secret_key="secret_key"
	app.run(debug=True)