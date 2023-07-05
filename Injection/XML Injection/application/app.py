from flask import Flask, render_template
import mysql.connector
import xml.etree.ElementTree as ET
import xml.dom.minidom

app = Flask(__name__)
app.secret_key = 'password-test'

@app.route('/')
def index():
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host='db',
        user='myuser',
        password='mypassword',
        database='mydatabase'
    )
    cursor = db.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM employees")
    results = cursor.fetchall()

    # Create the root element
    root = ET.Element("employees")

    # Iterate over the results and create XML elements
    for row in results:
        employee = ET.SubElement(root, "employee")
        id = ET.SubElement(employee, "id")
        id.text = str(row[0])
        name = ET.SubElement(employee, "name")
        name.text = row[1]
        email = ET.SubElement(employee, "email")
        email.text = row[2]
        password = ET.SubElement(employee, "password")
        password.text = row[3]
        phone_number = ET.SubElement(employee, "phone_number")
        phone_number.text = row[4]

    # Generate XML string from the root element
    xml_str = ET.tostring(root).decode()

    # Prettify the XML string
    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml_str = dom.toprettyxml()

    # Close the database connection
    cursor.close()
    db.close()

    # Render the XML template
    return render_template("index.html", xml_data=pretty_xml_str)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)