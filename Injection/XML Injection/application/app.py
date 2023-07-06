from flask import Flask, render_template, request
import mysql.connector
import xml.etree.ElementTree as ET
import xml.dom.minidom

app = Flask(__name__)
app.secret_key = 'password-test'

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        # Render the upload form template
        return render_template('upload.html')
    elif request.method == 'POST':
        # Check if an XML file was provided
        if 'file' not in request.files:
            return 'No file selected'

        xml_file = request.files['file']
        xml_data = xml_file.read()

        # Parse the XML data
        try:
            root = ET.fromstring(xml_data)
        except ET.ParseError as e:
            return f'Error parsing XML: {str(e)}'

        # Connect to the MySQL database
        db = mysql.connector.connect(
            host='db',
            user='myuser',
            password='mypassword',
            database='mydatabase'
        )
        cursor = db.cursor()

        # Extract data from XML and insert into the employees table
        for employee in root.findall('employee'):
            name = employee.find('name').text
            email = employee.find('email').text
            password = employee.find('password').text
            phone_number = employee.find('phone_number').text

            # Insert data into the employees table
            query = "INSERT INTO employees (name, email, password, phone_number) VALUES (%s, %s, %s, %s)"
            values = (name, email, password, phone_number)
            cursor.execute(query, values)
            db.commit()

        # Close the database connection
        cursor.close()
        db.close()

        return 'XML data uploaded successfully'


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        # Render the search form template
        return render_template('search.html')
    elif request.method == 'POST':
        # Retrieve the keyword from the form submission
        keyword = request.form.get('keyword')

        # Connect to the MySQL database and perform the search
        db = mysql.connector.connect(
            host='db',
            user='myuser',
            password='mypassword',
            database='mydatabase'
        )
        cursor = db.cursor()

        # Execute the search query
        query = "SELECT * FROM employees WHERE email LIKE %s"
        values = (f'%{keyword}%',)
        cursor.execute(query, values)
        results = cursor.fetchall()

        # Close the database connection
        cursor.close()
        db.close()

        # Render the search results template with the results and keyword
        return render_template('search.html', results=results, keyword=keyword)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)