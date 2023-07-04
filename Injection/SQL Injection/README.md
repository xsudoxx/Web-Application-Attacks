
# Structured Query Language Injection
## Summary
````
[https://portswigger.net/web-security/access-control/idor](https://portswigger.net/web-security/sql-injection#:~:text=SQL%20injection%20%28SQLi%29%20is%20a%20web%20security%20vulnerability,that%20they%20are%20not%20normally%20able%20to%20retrieve.)
````
````
SQL injection (SQLi) is a web security vulnerability that allows an attacker to interfere with the queries that an application makes to its database. It generally allows an attacker to view data that they are not normally able to retrieve. This might include data belonging to other users, or any other data that the application itself is able to access. In many cases, an attacker can modify or delete this data, causing persistent changes to the application's content or behavior.
````

## chatgpt summary
````
Structured Query Language (SQL) injection is a type of web application security vulnerability that allows an attacker to inject malicious SQL code into a web application's input fields, which can then be executed by the backend database. This can enable the attacker to access, modify, or delete data in the database, or to perform other malicious actions such as bypassing authentication or escalating privileges.

SQL injection attacks typically occur when web applications use user input to construct SQL queries without proper validation or sanitization. An attacker can exploit this vulnerability by submitting input values that contain SQL code, such as ' OR 1=1 --, which can modify the SQL query and cause unexpected behavior.
````
## Explaining this to a 5th grader
````
Imagine you have a toy box with different toys inside it. You can only play with one toy at a time, so you have to ask your mom or dad to get the toy you want out of the box for you.

Now, imagine you have a friend who is really sneaky and always wants to play with all of your toys, not just one. One day, your friend figures out that they can trick your mom or dad into giving them all of the toys by asking for a toy in a certain way.

That's kind of like what SQL injection is. When you use a website, sometimes you have to tell the website what you want to see or do by typing something into a box (like a username or a search term). Just like how you ask your mom or dad for a toy, the website uses a special language called SQL to ask a database for the information you want.

But if the website isn't careful, a sneaky person can trick the website into asking the database for more information than they're supposed to get. They can do this by typing in something tricky, like a secret code, that makes the website ask the database for all the information instead of just the information they're supposed to see.

When this happens, the sneaky person can see or do things they're not supposed to, just like how your friend can play with all of your toys instead of just one. This is bad because it can let the sneaky person steal information or cause problems on the website.

To prevent this from happening, website developers have to be very careful about how they ask the database for information. They have to make sure they're only asking for the information they're supposed to get, and not letting sneaky people trick them into asking for more.
````
## Setup
### Option #1
````
Open Docker and have it running
````

![image](https://github.com/xsudoxx/Web-Application-Attacks/assets/127046919/16a6145f-5cce-4c70-be86-34b0e24e03ee)

````
Go into [VSCode]
Open up [Terminal]
git clone https://github.com/xsudoxx/Web-Application-Attacks.git
cd Web-Application-Attacks
cd Injection
cd '.\SQL Injection\'
````

### Clear the DB
````
docker volume rm sqlinjection_db-data
````
### Running the vulnerable application
````
docker-compose up
````
### Shutting down the vulnerable application
````
docker-compose down
````
### Option #2
````
Open [Docker Desktop]
Open [VSCODE]
(If you already have Docker Extension added please continue, if not please install it)
Find [docker-compose.yml] & [right-click on the file] & [click][Compose Up]
Hit [Enter]
ctrl + c
docker-compose down
docker-compose up
````

# Code Review
````
The vulnerable part of this code is where the SQL query is constructed using string concatenation instead of using parameterized queries. Specifically, these two lines of code:


query = "SELECT * FROM users WHERE email = '" + username_or_email + "' AND password = '" + password + "'"

query = "SELECT * FROM users WHERE username = '" + username_or_email + "' AND password = '" + password + "'"
These lines of code concatenate the user input values username_or_email and password directly into the SQL query string using string interpolation. This makes the code vulnerable to SQL injection attacks, where an attacker could submit a specially crafted input value that modifies the SQL query in unexpected ways.

To prevent SQL injection attacks, the code should use parameterized queries, which ensures that the user input is always treated as data, rather than as part of the SQL query. Parameterized queries use placeholders in the SQL query and pass the values separately, which helps prevent unexpected behavior and improves the security of the application.
````
## Updated code
````
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username_or_email = request.form['username_or_email']
            password = request.form['password']

            # Connect to the database and retrieve the user
            db = mysql.connector.connect(
                host='db',
                user='myuser',
                password='mypassword',
                database='mydatabase'
            )
            cursor = db.cursor()

            if '@' in username_or_email:
                # Look up user by email
                query = "SELECT * FROM users WHERE email = %s AND password = %s"
                values = (username_or_email, password)
            else:
                # Look up user by username
                query = "SELECT * FROM users WHERE username = %s AND password = %s"
                values = (username_or_email, password)

            cursor.execute(query, values)
            user = cursor.fetchone()

            # Close the connection
            db.close()

            if user:
                # Store the user's information in the session
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['email'] = user[2]
                session['password'] = user[3]

                if user[4] == 'admin':
                    # Store the admin status in the session
                    session['is_admin'] = True

                    # Redirect the admin user to the admin.html page
                    return redirect(url_for('admin'))

                # Redirect to the user's home page
                return redirect(url_for('user_home', user_id=user[0]))

            else:
                flash("Invalid username or password. Please try again.")
                return redirect(url_for('login'))

        except Exception as e:
            # Log the error
            logging.error(f"Error during login: {str(e)}")
            flash("An error occurred during login. Please try again later.")

    return render_template('login.html')
````
````
In this modified version of the code, we use parameterized queries instead of string concatenation to construct the SQL query. Parameterized queries use placeholders in the SQL query and pass the values separately, which ensures that user input is always treated as data, rather than as part of the SQL query. This helps prevent SQL injection attacks.

The code uses %s as placeholders in the SQL query, and passes the actual values as a tuple to the execute() method of the cursor object. This ensures that the values are properly escaped and sanitized, which helps to prevent SQL injection attacks.

By using parameterized queries, the code is much safer from SQL injection attacks, as the input values are always treated as data, rather than as part of the SQL query.
````

# Cyber Security Skills Learned
## Authentication
````
Authentication is the process of verifying the identity of a user or entity to ensure that they are who they claim to be. In the context of computer systems and online services, authentication is crucial for controlling access to resources and protecting sensitive information.
````
### Example 
````
User provides credentials: The user submits their identification information, such as a username or email, and a secret password.
````
