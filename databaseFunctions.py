import sqlite3
from sqlite3 import Error

from main import db_file


def create_database():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # cursor object
        cursor = conn.cursor()
        # Drop the USER table if already exists.
        cursor.execute("DROP TABLE IF EXISTS users")
        # Creating USER table
        table = """ CREATE TABLE users (
                            username VARCHAR(50) PRIMARY KEY,
                            password VARCHAR(50) NOT NULL,
                            email VARCHAR(50) NOT NULL,
                            first_name CHAR(50) default null,
                            last_name CHAR(50) default null,
                            age INTEGER default null,
                            activity VARCHAR(50) default null
                                ); """
        cursor.execute(table)

        # Create products table
        cursor.execute("DROP TABLE IF EXISTS products")
        table = """ CREATE TABLE products (
                        product_id INTEGER PRIMARY KEY ,
                        product_name VARCHAR(255) default null,
                        image_path VARCHAR(255) default null,
                        price FLOAT default null
                         ); """
        cursor.execute(table)

        # Create orders table
        cursor.execute("DROP TABLE IF EXISTS orders")
        table = """ CREATE TABLE orders (
                                order_id INTEGER PRIMARY KEY ,
                                product_name VARCHAR(255) default null,
                                image_path VARCHAR(255) default null,
                                quantity INTEGER,
                                order_date DATE default null,
                                username VARCHAR(50) not null,
                                FOREIGN KEY(username) REFERENCES users(username)
                                 ); """
        cursor.execute(table)

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def insertData():

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(""" INSERT INTO users (username, password, email, first_name, last_name, age, activity) VALUES
            ('admin', '$2b$12$OT9GEFU7ekEcJlFtzXaF9erl6VAweaLh9u8aroAMGO//cD05ZLqiG', 'admin@email.com', 'admin', 'admin', 0, '')
            ; """)

        cursor.execute(""" INSERT INTO products (product_id, product_name, image_path, price) VALUES
            (1, 'mineralwater-blueberry', 'static/images/mineralwater-blueberry.jpg', 2.90),
            (2, 'mineralwater-lemonlime', 'static/images/mineralwater-lemonlime.jpg', 2.90),
            (3, 'mineralwater-orange', 'static/images/mineralwater-orange.jpg', 2.90),
            (4, 'mineralwater-peach', 'static/images/mineralwater-peach.jpg', 2.90),
            (5, 'mineralwater-raspberry', 'static/images/mineralwater-raspberry.jpg', 2.90),
            (6, 'mineralwater-strawberry', 'static/images/mineralwater-strawberry.jpg', 2.90),
            (7, 'proteinbar-chocolate', 'static/images/proteinbar-chocolate.jpg', 1.99),
            (8, 'proteinbar-lemon', 'static/images/proteinbar-lemon.jpg', 1.99),
            (9, 'proteinbar-peanutbutter', 'static/images/proteinbar-peanutbutter.jpg', 1.99),
            (10, 'vitamin-a', 'static/images/vitamin-a.jpg', 14.99),
            (11, 'vitamin-bcomplex', 'static/images/vitamin-bcomplex.jpg', 14.99),
            (12, 'vitamin-calcium', 'static/images/vitamin-calcium.jpg', 19.99),
            (13, 'vitamin-c', 'static/images/vitamin-c.jpg', 14.99),
            (14, 'vitamin-d', 'static/images/vitamin-d.jpg', 14.99),
            (15, 'vitamin-flaxseed-oil', 'static/images/vitamin-flaxseed-oil.jpg', 19.99),
            (16, 'vitamin-iron', 'static/images/vitamin-iron.jpg', 19.99),
            (17, 'vitamin-magnesium', 'static/images/vitamin-magnesium.jpg', 19.99),
            (18, 'vitamin-multi', 'static/images/vitamin-multi.jpg', 19.99)
            ; """)

        cursor.execute(""" INSERT INTO orders (order_id, product_name, image_path, quantity, order_date, username) VALUES
            (1, 'mineralwater-blueberry', 'static/images/mineralwater-blueberry.jpg', 2, '2022-03-07', 'alex'),
            (2, 'mineralwater-lemonlime', 'static/images/mineralwater-lemonlime.jpg', 3,  '2022-06-01', 'alex'),
            (3, 'mineralwater-blueberry', 'static/images/mineralwater-blueberry.jpg', 2, '2022-10-23', 'alex'),
            (4, 'vitamin-bcomplex', 'static/images/vitamin-bcomplex.jpg', 1,  '2022-12-02', 'malika'),
            (5, 'proteinbar-peanutbutter', 'static/images/proteinbar-peanutbutter.jpg', 3,  '2022-07-15', 'charles'),
            (6, 'mineralwater-blueberry', 'static/images/mineralwater-blueberry.jpg', 2, '2022-03-07', 'malika'),
            (7, 'mineralwater-lemonlime', 'static/images/mineralwater-lemonlime.jpg', 4, '2022-06-01', 'charles'),
            (8, 'mineralwater-blueberry', 'static/images/mineralwater-blueberry.jpg', 2, '2022-10-23', 'malika'),
            (9, 'vitamin-a', 'static/images/vitamin-bcomplex.jpg', 1,  '2022-12-02', 'charles'),
            (10, 'proteinbar-lemon', 'static/images/proteinbar-lemon.jpg', 3,  '2022-07-15', 'charles')
            ; """)

        # persist the changes
        conn.commit()

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def displayData():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # cursor object
        cursor = conn.cursor()
        data = cursor.execute(""" SELECT * FROM users; """)
        # join orders on users.username=orders.username
        # join products on orders.product_name=products.product_name

        conn.commit()
        print("Query Result: ")
        for row in data:
            print(row)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
