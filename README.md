# PROVITA

This is an online shop website where users can create an account and buy a range of healthy products.

## Getting Started

1. Make sure to install all the required libraries from the file: `requirements.txt`
2. To reset the database: Go to the `main.py` file, un-comment the funtions `databaseFunctions.create_database()` & `databaseFunctions.insertData()` (Lines 450 & 451) & Run the file `main.py`
3. To run the app go to `main.py` file
4. The website landing page is the Provita Homepage
5. Go to `Signup` to create a new account then complete the Login. OR go to `Login` page to log in as the `admin` (Has access to the Admin page):

    - Username: `admin`
    - Password: `password`
   
6. Go to `My Profile` to display the current logged-in user's details
7. Go to `My Orders` to display the current logged-in user's orders (if any)
8. Go to `Shop` to search for products and add products to cart
9. If the user choses to add products to cart, the user will be redirected to the `Checkout` page to complete the order.
10. If the current logged-in user is the `admin`, go to `Admin` to add a new product to the database
    - Product Name: mineralwater-watermelon-raspberry
    - Upload an image: Chose the image `water-watermelon-raspberry` (make sure to save the image provided in your computer)
    - Set Price: 2.99
    - And click on Submit
    - Go to `Shop` and search for water to confirm the new product was added to the database
    
11. Go to `Logout` to log out from the website
12. Go to `LinkedIn` to be redirected to the Social Media page ( There is no ProVita profile)

## Secure Web Programming

1. Authentication - To prevent passwords from being reused in case of a data breach, the password is `Hashed` before been stored in the database.

2. Session Management - To prevent session cookies for being reused for session hijacking attacks, the library `session` adds the secret key to make the cookie stronger at the time of login. 
Another security measure, a logout option is provided to the user to terminate the session.

3. XSS - Scripts can be added by user input in the `Signup` page. 
To prevent XSS attacks to display malicious scripts in HTML pages that read data from the database, the `Profile` HTML code is `encoded` which transforms JavasScript code into text, so the script code won't run.<br>

    **To test for XSS attack:**
    
   1. Go to `Signup`, create a new account using the below code & then login:<br>
          - Username: `<script>alert(‘XSS’)</script>`<br>
          - Password: `<script>alert(‘XSS’)</script>` <br>
   2. Go to `My Profile` page >> View Source Page >> Confirm the script is handled as string. 

4. SQL Injection - SQL injections can be added by user input in the `Login` and `Shop` pages (and by the admin input in the `Admin` page). 
To prevent from SQL injection attacks, all queries to the database are `parameterized` and done with prepared statements. 
Therefore, incorrect parameters or arbitrary SQL code would not work to retrieve data from the database as the queries will return no results.

    ** To test for SQL Injection:**
    1. Go to `Shop` and search for the following string: "water";DROP TABLE orders;
    2. Logout and then go to `Login` and use the following string as username and passworkd: " or ""="
