----------------------------------------------------------------------------------

APP URL: https://flaskwebsite-ecom.herokuapp.com/

----------------------------------------------------------------------------------

1. Register:

<<<<< Input >>>>>

Method: POST
URL: https://flaskwebsite-ecom.herokuapp.com/register

{
    "username":"<username>",
    "email":"<email_id>",
    "password":"<password>"
}

<<<<< Output >>>>>

Case-1: New account

{
    "email": "<email_id>",
    "msg": "Please verify email to complete registration",
    "password": "<encrypted_password>",
    "token": "<unique_id>",
    "username": "<username>"    
}

Case-2: Account exists for <email_id>

{
    "msg": "Account exist for <email_id"
}

Case-3: Username taken

{
    "msg": "username taken!"
}

----------------------------------------------------------------------------------

2. Verification:

<<<<< Input >>>>>

Method: GET
URL: https://flaskwebsite-ecom.herokuapp.com/verication/<token>

-> Replace <token> with <unique_id> generated from registration process.
                  OR
-> Click on the verification link sent to <email_id>.

<<<<< Output >>>>>

Case-1: Verification Successful

{
    "msg": "Congratulations, registration successful! Redirect to login page"
}

Case-2: Token expired

{
    "msg": "Token timed out!"
}

Case-3: Incorrect token

{
    "msg": "Token seems incorrect!"
}


----------------------------------------------------------------------------------
3. Login:

<<<<< Input >>>>>

Method: POST
URL: https://flaskwebsite-ecom.herokuapp.com/

{
    "username":"<username>",
    "password":"<password>"
}

<<<<< Output >>>>>

Case-1: Login success

{
   "msg":"Welcome back, <username>"   
}

Case-2: Incorrect username

{
    "msg": "Invalid username or password"
}

Case-3: Incorrect password

{
    "msg": "Invalid username or password"
}

----------------------------------------------------------------------------------
4. Logut:

<<<<< Input >>>>>

Method: GET
URL: https://flaskwebsite-ecom.herokuapp.com/logout

<<<<< Output >>>>>

Logout success

{
   "msg":"Logged out!"   
}


----------------------------------------------------------------------------------
5. Dashboard:

<<<<< Input >>>>>

Method: GET
URL: https://flaskwebsite-ecom.herokuapp.com/dashboard

<<<<< Output >>>>>

Case-1: Show dashboard if user is logged in

{
   "msg":"Welcome to dashboard"   
}

Case-2: Redirect to login page if user is not logged in

{
  "msg":"redirect to login page"
}


----------------------------------------------------------------------------------
6. Profile:

<<<<< Input >>>>>

Method: GET
URL: https://flaskwebsite-ecom.herokuapp.com/profile

<<<<< Output >>>>>

Case-1: Show profile if user is logged in

{
   "msg":"Welcome to profile"   
}

Case-2: Redirect to login page if user is not logged in

{
  "msg":"redirect to login page"
}
