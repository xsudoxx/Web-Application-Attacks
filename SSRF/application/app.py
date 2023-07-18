import pdfkit
from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
import logging
import mysql.connector

# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = 'password-test'

# Home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get URL from form data
        url = request.form['url']
        
        # Insert URL into database
        db = mysql.connector.connect(
            host='db',
            user='myuser',
            password='mypassword',
            database='mydatabase'
        )
        cursor = db.cursor()
        sql = "INSERT INTO MyURLs (urls) VALUES (%s)"
        cursor.execute(sql, (url,))
        db.commit()
        
        # Generate PDF file from URL
        config = pdfkit.configuration(wkhtmltopdf='/usr/local/lib/python3.9/site-packages/wkhtmltopdf')
        pdf = pdfkit.from_url(url, False, configuration=config)
        
        # Send PDF file back to user
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=url.pdf'
        return response
    
    return render_template('home.html')
# Success page
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
