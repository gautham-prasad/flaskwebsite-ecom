----------------------------------------------------------------------------------

APP URL: https://flaskwebsite-ecom.herokuapp.com/

----------------------------------------------------------------------------------

1. Register:

<<<<< Input >>>>>

Method: POST
URL: https://flaskwebsite-ecom.herokuapp.com/register
JSON: 
{
    "username":"<username>",
    "email":"<email_id>",
    "password":"<password>"
}

<<<<< Output >>>>>

Case-1: New account
Status code: default/code-to-be-updated
JSON:
{
    "email": "<email_id>",
    "msg": "Please verify email to complete registration",
    "password": "<encrypted_password>",
    "token": "<unique_id>",
    "username": "<username>"    
}

Case-2: Account exists for <email_id>
Status code: default/code-to-be-updated
JSON:
{
    "msg": "Account exist for <email_id"
}

Case-3: Username taken
Status code: default/code-to-be-updated
JSON:
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
Status code: 
JSON:
{
    "msg": "Congratulations, registration successful! Redirect to login page"
}

Case-2: Token expired
Status code: default/code-to-be-updated
JSON:
{
    "msg": "Token timed out!"
}

Case-3: Incorrect token
Status code: default/code-to-be-updated
JSON:
{
    "msg": "Token seems incorrect!"
}


----------------------------------------------------------------------------------
3. Login:

<<<<< Input >>>>>

Method: POST
URL: https://flaskwebsite-ecom.herokuapp.com/
JSON: 
{
    "username":"<username>",
    "password":"<password>"
}

<<<<< Output >>>>>

Case-1: Login success
Status code: default/code-to-be-updated
JSON:
{
   "msg":"Welcome back, <username>"   
}

Case-2: Incorrect username
Status code: default/code-to-be-updated
JSON:
{
    "msg": "Invalid username or password"
}

Case-3: Incorrect password
Status code: default/code-to-be-updated
JSON:
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
Status code: default/code-to-be-updated
JSON:
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
Status code: default/code-to-be-updated
JSON:
{
   "msg":"Welcome to dashboard"   
}

Case-2: Redirect to login page if user is not logged in
JSON:
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
Status code: default/code-to-be-updated
JSON:
{
   "msg":"Welcome to profile"   
}

Case-2: Redirect to login page if user is not logged in
Status code: default/code-to-be-updated
JSON:
{
  "msg":"redirect to login page"
}
