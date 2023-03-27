PROVITA-AUTHENTICATION

1) Install the libraries from the file: requirements.txt
2) Run the file main.py
3) The landing page is the Provita Homepage
4) Go to Signup page to create a new account or go to Login page to login with the test users below:
    
    a) Username: admin
    Password: password
    *** Has access to Admin page***
    
    b) Username: malika
    Password: password
    
SECURE WEB PROGRAMMING

1) XSS - Scripts can be added by user input in the 'Signup' page. 
To prevent from XSS atacks, the profile page HTML code is sanetized with regular expression
that transforms javascript code into string so the script code won't run.
    
    To test for XSS attack:
    
    a) Use the below credentials to login:
    Username: <script>alert(‘XSS’)</script>
    Password: <script>alert(‘XSS’)</script>
    b) Go to the Profile page >> View Source Page >> Confirm the script is handled as string. The angle brackets are 

2) SQL Injection - SQL injections can be added by user input in the 'Login' and 'Buy' pages. 
To prevent from SQL injection attacks, all queries to the database are done with prepared statements. 
Therefore, incorrect parameters or arbitrary SQL code would not work to retrieve data from the database as the queries will return no results.