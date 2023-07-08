from flask import Flask, render_template, request
import mysql.connector
import xml.etree.ElementTree as ET
import traceback
from lxml import etree

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
            # Vulnerable code: XML data is parsed without disabling external entities
            parser = ET.XMLParser()
            root = ET.fromstring(xml_data, parser=parser)
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
    
@app.route('/xml', methods=['POST', 'GET'])
def xml():
    parsed_xml = None  # Variable to store parsed XML
    errormsg = ''  # Variable to store error message if any
    
    html = """
    <html>
      <body>
    """
    
    if request.method == 'POST':
        xml = request.form['xml']  # Get the XML data from the form submission
        parser = etree.XMLParser(no_network=False)  # Enable network entity resolution
        try:
            doc = etree.fromstring(str(xml), parser)  # Parse the XML using the specified parser
            parsed_xml = etree.tostring(doc)  # Convert the parsed XML back to string
            print(repr(parsed_xml))  # Print the parsed XML (for debugging purposes)
        except Exception as e:
            print("Cannot parse the XML")
            html += "Error:\n<br>\n" + traceback.format_exc()  # Display the error message if parsing fails
            
    if parsed_xml:
        html += "Result:\n<br>\n" + parsed_xml.decode()  # Display the parsed XML if available
    else:
        html += """
          <form action="/xml" method="POST">
            <p><h3>Enter XML to parse</h3></p>
            <textarea class="input" name="xml" cols="40" rows="5"></textarea>
            <p><input type="submit" value="Parse"/></p>
          </form>
        """
    
    html += """
      </body>
    </html>
    """
    
    return html
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)