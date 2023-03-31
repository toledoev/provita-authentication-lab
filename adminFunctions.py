import os
import sqlite3
from sqlite3 import Error

from flask import request, flash, redirect, url_for, app
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(image_path)
            flash("File uploaded successfully", category='success')


def insertProduct():
    # Create a new product and insert into the table products in the database
    # Upload the image file
    product_id = ""
    product_name = ""
    image_path = ""
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
        ## if this works, this means the user have been added successfully
        ## Therefore, we need to send them to the login page
    except Error as e:
        print(e)
        ## if the user is not added, we will get an exception which will be caught here
        ## So we need to say what to do if the user signup has failed and send them to the signup page again
        flash("Error. Product not added. ", category='error')
        return redirect(url_for('admin'))
    finally:
        if conn:
            conn.close()
    flash("Product added successfully!", category='success')
    return redirect(url_for('home'))
