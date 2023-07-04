
from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
import logging
import mysql.connector

# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = 'password-test'

@app.route('/')
def home():
    return render_template('index.html')

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
            query = "SELECT * FROM users WHERE (email = %s OR username = %s) AND password = %s"
            values = (username_or_email, username_or_email, password)
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            # Connect to the database and check if the user is already registered
            db = mysql.connector.connect(
                host='db',
                user='myuser',
                password='mypassword',
                database='mydatabase'
            )
            cursor = db.cursor()
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if user:
                # User already exists, show flash message and redirect to login
                flash("User already registered. Please log in.")
                db.close()
                return redirect(url_for('login'))

            # Insert the user into the database with the 'user' role
            query = "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)"
            values = (username, email, password, 'user')
            cursor.execute(query, values)
            db.commit()
            db.close()

            logging.info("Registration successful")
            flash("Registration successful. Please log in.")
            return redirect(url_for('login'))

        except Exception as e:
            # Log the error
            logging.error(f"Error during registration: {str(e)}")
            return "An error occurred during registration. Please try again later."

    return render_template('register.html')



@app.route('/user/<int:user_id>')
def user_home(user_id):
    if 'user_id' in session:
        logged_in_user_id = session['user_id']
        if logged_in_user_id == user_id:
            # Retrieve user information from the database based on the user_id
            db = mysql.connector.connect(
                host='db',
                user='myuser',
                password='mypassword',
                database='mydatabase'
            )
            cursor = db.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE id = %s"
            values = (user_id,)
            cursor.execute(query, values)
            user = cursor.fetchone()
            db.close()

            if user:
                username = user['username']
                email = user['email']
                password = user['password']

                return render_template('home.html', username=username, email=email, user_id=user_id, password=password)
            else:
                flash("User not found.")
        else:
            flash("Unauthorized access.")
    else:
        flash("Please log in to access this page.")

    return redirect(url_for('login'))




@app.route('/admin')
def admin():
    # Check if the user is logged in as an admin
    if session.get('is_admin'):
        # Get the admin's email and name from the session or database
        email = session['email']  # Update this with the key used to store the email in the session
        username = session['username']  # Update this with the key used to store the name in the session

        # Render the admin.html template and pass the email and name as template variables
        return render_template('admin.html', email=email, username=username,is_admin=True)
    else:
        # Redirect non-admin users to a different page or display an error message
        return redirect(url_for('login'))



@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Store the contact form submission into the database

        # Connect to the database and check if the user is already registered
        db = mysql.connector.connect(
            host='db',
            user='myuser',
            password='mypassword',
            database='mydatabase'
        )
        cursor = db.cursor()
        query = "INSERT INTO submissions (name, email, message) VALUES (%s, %s, %s)"
        values = (name, email, message)
        cursor.execute(query, values)
        db.commit()

        return render_template('contact_success.html')
    return render_template('contact.html')


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get("query")

        # Perform the necessary database query and processing based on the search query
        # Perform a database query to retrieve search results
        db = mysql.connector.connect(
            host='db',
            user='myuser',
            password='mypassword',
            database='mydatabase'
        )
        cursor = db.cursor()
        sql = "SELECT * FROM submissions WHERE name LIKE %s"
        value = f"%{query}%"
        cursor.execute(sql, (value,))
        results = cursor.fetchall()
        cursor.close()

    # Format the results as a list of dictionaries
        result_list = []
        for result in results:
            result_dict = {
                "id": result[0],
                "name": result[1],
                "email": result[2],
                "message": result[3]
            }
            result_list.append(result_dict)

        return render_template("search.html", query=query, results=result_list)
    
    return render_template("search.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)