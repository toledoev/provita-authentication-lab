<h1>PROVITA</h1>

This is an online shop website where users can create an account and buy a range of healthy products.

    1) Install the libraries from the file: requirements.txt
    2) In main.py, un-comment the funtions databaseFunctions.create_database() & databaseFunctions.insertData()
    to create the database and tables (Lines 409 & 410) 
    3) Re-comment the same lines again (Lines 409 & 410) 
    4) Run the file main.py
    5) The landing page is the Provita Homepage
    6) Go to Signup page to create a new account OR go to Login page to login with the test user below:
    
        a) Username: admin
        Password: password
        *** Has access to Admin page***
       
    
<h2>SECURE WEB PROGRAMMING </h2>

    1) Authentication - To prevent passwords from being reused in case of a data breach, 
    the inputed password from the user is Hashed before been stored in the database.

    2) Session Management - To prevent session cookies for being reused for session hajacking attacks,
    the library session adds the secret key to make the cookie stronger at the time of login.
    Another security measure, a logout option is provided to the user to terminate the session.

    3) XSS - Scripts can be added by user input in the 'Signup' page. 
    To prevent from XSS atacks, the 'Profile' HTML code is sanetized with regular expression
    that transforms javascript code into string so the script code won't run.
    
        To test for XSS attack:
        
        a) Use the below credentials to login:
        Username: <script>alert(‘XSS’)</script>
        Password: <script>alert(‘XSS’)</script>
        b) Go to the Profile page >> View Source Page >> Confirm the script is handled as string. 

    4) SQL Injection - SQL injections can be added by user input in the 'Login' and 'Buy' pages. 
    To prevent from SQL injection attacks, all queries to the database are parameterized and done with prepared statements. 
    Therefore, incorrect parameters or arbitrary SQL code would not work to retrieve data from the database as the queries will return no results.
