<h1>PROVITA</h1>

    1) Install the libraries from the file: requirements.txt
    2) Run the file main.py
    3) The landing page is the Provita Homepage
    4) Go to Signup page to create a new account or go to Login page to login with the test users below:
    
        a) Username: admin
        Password: password
        *** Has access to Admin page***
        
        b) Username: malika
        Password: password
    
<h2>SECURE WEB PROGRAMMING </h2>

    1) Authentication - To prevent passwords from being reused in case of a data breach, 
    the inputed password from the user is Hashed & Salted before been stored in the database.

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
    To prevent from SQL injection attacks, all queries to the database are done with prepared statements. 
    Therefore, incorrect parameters or arbitrary SQL code would not work to retrieve data from the database as the queries will return no results.
