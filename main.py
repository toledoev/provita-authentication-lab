import os
from datetime import date

from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect, secure_filename
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user

import databaseFunctions
from user import User

db_file = "mySQLite.db"
UPLOAD_FOLDER = 'static/images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ENV'] = "Development"
app.config['DEBUG'] = True

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'loginAction'


## Define an userloader function
@login_manager.user_loader
def load_user(username):
    return User(username)


## Set a secret key for the login session
app.secret_key = 'halapaoeed&**huahu2is'


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/signup')
def signup():
    if current_user.is_authenticated:
        flash("You are already logged in.", category='success')
        return redirect(url_for('profile'))
    return render_template("signup.html")


@app.route('/signupAction', methods=['POST'])
def signupAction():
    username = ""
    password = ""
    email = ""
    first_name = ""
    last_name = ""
    age = ""
    activity = ""

    if request.form.get("username"):
        username = request.form.get("username")
    if request.form.get("password"):
        password = request.form.get("password")

        ## This password is a normal string
        ## Therefore, we need to hash it before we put it in the database
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        print("True Password:", password, ", Hashed Password:", hashed_password)
        password = hashed_password

    if request.form.get("email"):
        email = request.form.get("email")
    if request.form.get("first_name"):
        first_name = request.form.get("first_name")
    if request.form.get("last_name"):
        last_name = request.form.get("last_name")
    if request.form.get("age"):
        age = request.form.get("age")
    if request.form.get("activity"):
        activity = request.form.get("activity")

    conn = sqlite3.connect(db_file)

    try:

        cursor = conn.cursor()
        sameUsernameCheck = "SELECT DISTINCT username FROM users WHERE username= ?"
        searchResult = cursor.execute(sameUsernameCheck, (username,))
        usernameInDb = None
        for row in searchResult:
            usernameInDb = row[0]
        if usernameInDb:
            flash('Username already exists.', category='error')
            return redirect(url_for('signup'))

        myquery = "INSERT INTO users (username, password, email, first_name, last_name, age, activity) VALUES (?,?,?,?,?,?,?)"
        print("My query is: ", myquery)
        cursor.execute(myquery, (username, password, email, first_name, last_name, age, activity))
        conn.commit()
        ## if this works, this means the user have been added successfully
        ## Therefore, we need to send them to the login page
    except Error as e:
        print(e)
        ## if the user is not added, we will get an exception which will be caught here
        ## So we need to say what to do if the user signup has failed and send them to the signup page again
        flash("Failed to signup. Try again!", category='error')
        return redirect(url_for('signup'))
    finally:
        if conn:
            conn.close()
    flash("Account created successfully!", category='success')
    return redirect(url_for('login'))


@app.route('/login')
def login():
    ## @TODO
    ## If user is already logged in we need to redirect them to their profile
    if current_user.is_authenticated:
        flash("You are already logged in.", category='success')
        return redirect(url_for('home'))
    return render_template("login.html")


@app.route('/loginAction', methods=['POST'])
def loginAction():
    username = ""
    password = ""
    if request.form.get("username"):
        username = request.form.get("username")
    if request.form.get("password"):
        password = request.form.get("password")

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        myquery = "SELECT password FROM users WHERE username= ?"
        data = cursor.execute(myquery, (username,))
        passwordInDB = None
        for row in data:
            passwordInDB = row[0]
        if passwordInDB:
            ## We have found a username matching the one provide for the login
            ## Now, we need to check that the password provide for the login is also correct
            validPassword = bcrypt.check_password_hash(passwordInDB, password)

            ## If the passwords match, we need to mark them as logged in and send them to their profile
            ## Else we need to send them to the login page again
            if validPassword:
                login_user(User(username))
                flash("You are now logged in.", category='success')
                return redirect(url_for('home'))
            else:
                ## The password does not match
                ## we need to send them to the login page again
                flash("Your username or password are incorrect! Try to login again.", category='error')
                return redirect(url_for('login'))
                pass
        else:
            ## The Username does not exist
            ## we need to send them to the login page again
            flash("Your username is incorrect! Try to login again.", category='error')
            return redirect(url_for('login'))
    except Error as e:
        print(e)
        ## if there was an error in the login, we will get an exception which will be caught here
        ## So we need to send the user to the login page again
        flash("Failled to login. Try again!", category='error')
        return redirect(url_for('login'))
    finally:
        if conn:
            conn.close()


@app.route('/profile', methods=['GET'])
def profile():
    ## If the user is not logged in, we need to redirect them to the login page
    if not current_user.is_authenticated:
        flash("You need to login to access the profile page.", category='error')
        return redirect(url_for('login'))

    ## If the user is logged in, we need to get their username
    myusername = current_user.username
    myemail = ""
    myfname = ""
    mylname = ""
    myage = ""
    myactivity = ""

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Get the personal data of the user
        myquery = "SELECT email, first_name, last_name, age, activity FROM users WHERE username=?"
        dataUser = cursor.execute(myquery, (myusername,))
        print("These are the details of the user: ")
        rows = []
        for row in dataUser:
            print(row)
            rows.append(row)
        if len(rows) == 1:
            myemail = rows[0][0]
            myfname = rows[0][1]
            mylname = rows[0][2]
            myage = rows[0][3]
            myactivity = rows[0][4]

        else:
            return "Error: the username does not exist"

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    # Render the user details
    return render_template("profile.html", username=myusername, email=myemail, first_name=myfname, last_name=mylname,
                           age=myage, activity=myactivity)


@app.route('/orders', methods=['GET'])
def orders():
    if not current_user.is_authenticated:
        flash("You need to login to access the orders page.", category='error')
        return redirect(url_for('login'))

    conn = None

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Get the orders of the User
        myquery = "SELECT order_date, orders.product_name, quantity, orders.image_path, price FROM orders join users on orders.username = users.username left join products on orders.product_name = products.product_name WHERE orders.username= ? ORDER BY order_date"
        cursor.execute(myquery, (current_user.username,))
        # print("These are the user's orders: ")
        rows = cursor.fetchall()

        # Render the orders details
        return render_template("orders.html", ordersData=rows)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


@app.route('/search')
def search():
    return render_template("search.html")


@app.route('/searchAction')
def searchAction():
    if not current_user.is_authenticated:
        flash("You need to login to access the profile page.", category='error')
        return redirect(url_for('login'))

    searchString = request.args.get("searchString")
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        likeString = f"%{searchString}%"
        cursor.execute("SELECT product_id, product_name, image_path, price FROM products WHERE product_name LIKE ?",
                       (likeString,))
        data = cursor.fetchall()
        print("These are the products found: ", data)

        return render_template('search.html', products=data)

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


@app.route('/addToCart', methods=['POST'])
def addToCart():
    product_name = request.form['product_name']
    image = request.form['image']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    return redirect(url_for('checkout.html', product_name=product_name, quantity=quantity, price=price, image=image))


@app.route('/checkout', methods=['GET'])
def checkout():
    product_name = request.args.get('product_name')
    image = request.args.get('image')
    quantity = request.args.get('quantity')
    price = request.args.get('price')
    return render_template('checkout.html', product_name=product_name, image=image, quantity=quantity, price=price)


@app.route('/completeOrder', methods=['POST'])
def completeOrder():
    # Insert the new order into the table 'orders' in the database
    order_id = ""
    product_name = ""
    image_path = ""
    quantity = ""
    order_date = date.today()
    username = current_user.username

    if request.args.get("product_name"):
        product_name = request.args.get("product_name")
    if request.args.get("image"):
        image_path = request.args.get("image")
    if request.args.get("quantity"):
        quantity = int(request.args.get("quantity"))

    conn = sqlite3.connect(db_file)

    try:
        cursor = conn.cursor()
        myquery = "INSERT INTO orders (order_id, product_name, image_path, quantity, order_date, username) VALUES (?,?,?,?,?,?)"
        print("My query is: ", myquery)
        cursor.execute(myquery, (order_id, product_name, image_path, quantity, order_date, username))
        conn.commit()
    except Error as e:
        print(e)
        flash("Error. Order failed. ", category='error')
    finally:
        if conn:
            conn.close()
    flash("Order placed successfully!", category='success')
    return redirect(url_for('checkout'))


@app.route('/admin')
def admin():
    if not current_user.is_authenticated:
        flash("You need to login to access the profile page.", category='error')
        return redirect(url_for('login'))
    if current_user.username == 'admin':
        return render_template("admin.html")
    else:
        return "Error: You cannot access this page"


@app.route('/addProduct', methods=['POST'])
def addProduct():
    # Only the below files types are accepted
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # Upload the image to the project folder
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            image_path = os.path.join(os.path.join(app.config['UPLOAD_FOLDER']), secure_filename(file.filename))
            file.save(image_path)
            print(image_path)
            flash("File uploaded successfully", category='success')

    # Insert the new product into the table products in the database
    product_id = ""
    product_name = ""
    image_path = image_path
    price = ""

    if request.form.get("product_id"):
        product_id = int(request.form.get("product_id"))
    if request.form.get("product_name"):
        product_name = request.form.get("product_name")
    if request.form.get("image"):
        image_path = image_path
    if request.form.get("price"):
        price = float(request.form.get("price"))

    conn = sqlite3.connect(db_file)

    try:
        cursor = conn.cursor()
        myquery = "INSERT INTO products (product_id, product_name, image_path, price) VALUES (?,?,?,?)"
        print("My query is: ", myquery)
        cursor.execute(myquery, (product_id, product_name, image_path, price))
        conn.commit()
    except Error as e:
        print(e)
        flash("Error. Product not added. ", category='error')
    finally:
        if conn:
            conn.close()
    flash("Product added successfully!", category='success')
    return redirect(url_for('admin'))


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return render_template("logout.html")


if __name__ == '__main__':
    # databaseFunctions.create_database()
    # databaseFunctions.insertData()
    # databaseFunctions.displayData()
    app.run(host='127.0.0.1', port=5000, debug=True)
