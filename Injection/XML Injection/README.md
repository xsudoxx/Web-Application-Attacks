# XML Injection
## Summary
````
https://portswigger.net/web-security/xxe
````
````
XML external entity injection (also known as XXE) is a web security vulnerability that allows an attacker to interfere with an application's processing of XML data. It often allows an attacker to view files on the application server filesystem, and to interact with any back-end or external systems that the application itself can access.

In some situations, an attacker can escalate an XXE attack to compromise the underlying server or other back-end infrastructure, by leveraging the XXE vulnerability to perform server-side request forgery (SSRF) attacks
````
## PayloadAllThings
````
https://github.com/payloadbox/xxe-injection-payload-list
````
## chatgpt summary
````
XXE stands for XML External Entity. It is a vulnerability that occurs when an application parses XML input from untrusted sources without proper validation and protection. The vulnerability arises due to the ability of XML parsers to process external entities, which are references to external resources such as files or URLs.

When an application is vulnerable to XXE, an attacker can exploit it by injecting specially crafted XML input containing external entity references. This can lead to various security risks, including:

Disclosure of sensitive information: An attacker can use XXE to read arbitrary files on the server, including configuration files, credentials, or other sensitive data. By leveraging entity expansion, the attacker can view the contents of these files within the XML response.

Server-side request forgery (SSRF): XXE can be used to initiate requests to internal or external network resources by leveraging entity expansion to include URLs. This can result in SSRF attacks, where an attacker can make requests to arbitrary URLs on behalf of the vulnerable server.

Denial of Service (DoS): By exploiting recursive entity expansion, an attacker can cause resource exhaustion and potentially crash the server by creating excessively large XML payloads or by including a large number of nested entities.

To mitigate XXE vulnerabilities, it is important to apply the following security practices:

Disable external entity resolution: Configure the XML parser to disable the resolution of external entities or restrict it to trusted sources only.

Use a secure XML parser: Ensure that you are using a secure XML parsing library that has built-in protections against XXE vulnerabilities.

Validate and sanitize input: Implement strict input validation and sanitization techniques to prevent malicious XML input from being processed.

Implement least privilege: Restrict the access and permissions of the XML processing components to minimize the potential impact of an XXE attack.

By following these best practices, you can protect your application from XXE vulnerabilities and ensure the secure processing of XML input.
````
## Explaining this to a 5th grader
````
Certainly! Imagine you have a secret codebook with instructions written in a special language called XML. This codebook helps your computer understand and process information in a structured way. XML is like a set of rules for organizing data.

Now, XML allows us to use special codes called entities to refer to other pieces of information. It's like using shortcuts or placeholders. For example, instead of writing a long name every time, we can use a short name that represents the same thing.

However, sometimes, bad people can take advantage of these shortcuts. They can trick the computer into looking for information in the wrong place or even read secret information that they shouldn't have access to. It's like someone sneaking into your secret hiding spot and reading your personal diary.

This is what we call an XML External Entity (XXE) attack. The bad people try to manipulate the computer by using these shortcuts in the XML code. They can make the computer do things it's not supposed to do or reveal information that should be kept secret.

To protect against XXE attacks, we need to be careful with how we handle XML data. We need to make sure that the computer only reads the information it's supposed to and doesn't get tricked by these shortcuts used by the bad people.

Just like you wouldn't want someone snooping around in your private things, we need to protect our computer systems from these sneaky attacks to keep our information safe.
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
cd '.\XML Injection\'
````

### Clear the DB
````
docker volume rm xmlinjection-db-1
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
The XXE vulnerability in the provided code is due to the use of the etree.fromstring() method to parse the XML data without disabling external entity resolution. This vulnerability arises because the XML parser is configured to allow the processing of external entities.

The line parser = etree.XMLParser(no_network=False) enables network entity resolution, meaning the XML parser can resolve and process external entities referenced in the XML. This includes accessing files or resources on the network.

In an XXE attack, an attacker can craft a malicious XML payload and submit it to the /xml endpoint. If the application does not properly validate or sanitize the XML data and allows external entity resolution, the attacker can leverage the vulnerability to read sensitive files, perform SSRF attacks, or exploit other security weaknesses.
````

````
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
````
## Updated code
````
@app.route('/xml', methods=['POST', 'GET'])
def xml():
    parsed_xml = None
    errormsg = ''
    
    html = """
    <html>
      <body>
    """
    
    if request.method == 'POST':
        xml = request.form['xml']
        parser = etree.XMLParser(no_network=True)  # Disable network entity resolution
        try:
            doc = etree.fromstring(str(xml), parser)
            parsed_xml = etree.tostring(doc)
            print(repr(parsed_xml))
        except Exception as e:
            print("Cannot parse the XML")
            html += "Error:\n<br>\n" + traceback.format_exc()
            
    if parsed_xml:
        html += "Result:\n<br>\n" + parsed_xml.decode()
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
````
````
In this updated code, the XML parser is configured with parser = etree.XMLParser(no_network=True), which disables the network entity resolution. This ensures that the XML parser will not process any external entities, mitigating the XXE vulnerability.

By making this change, the code becomes more secure as it prevents potential exploitation through external entity references in the XML data.
````

# Cyber Security Skills Learned
## XXE
````
XXE stands for XML External Entity. It is a vulnerability that occurs when an XML parser insecurely processes external entities defined in the XML input. External entities are references to external resources such as files, URLs, or even system commands.
````
### Example 
````
Here are a few examples of different XXE (XML External Entity) attacks:

File Inclusion: An attacker can include local or remote files by defining an external entity pointing to the file location. For example:
<!DOCTYPE test [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
Server Side Request Forgery (SSRF): An attacker can make the vulnerable server perform requests to other internal or external systems by defining an external entity with a URL. For example:

<!DOCTYPE test [<!ENTITY xxe SYSTEM "http://internal-server/secret">]>
Denial of Service (DoS): An attacker can cause a DoS condition by defining an external entity that repeatedly fetches a large file from the server or a remote system. For example:

<!DOCTYPE test [
  <!ENTITY xxe SYSTEM "http://attacker-server/large-file">
  <!ENTITY xxe1 "&xxe;&xxe;&xxe;&xxe;&xxe;&xxe;&xxe;&xxe;&xxe;&xxe;">
]>
Blind XXE: In this type of attack, an attacker doesn't receive the response directly, but can still extract information indirectly by leveraging the out-of-band (OOB) techniques. For example, an attacker can include an external entity that triggers a DNS lookup or sends an HTTP request to their controlled server.
````
## XML
````
XML stands for eXtensible Markup Language. It is a markup language that is designed to store and transport data. XML uses tags to define elements and their hierarchical structure, allowing for the representation of structured data.

XML is often used as a format for data interchange between different systems and platforms, as it provides a standardized way to structure and organize data. It is widely used in web services, configuration files, data storage, and many other applications.

XML documents consist of a prologue, which includes the XML declaration, and a root element that encloses all other elements. Elements can have attributes, which provide additional information about the element. The content of elements can be text, other elements, or a combination of both.
````
### Example
````
<?xml version="1.0" encoding="UTF-8"?>
<bookstore>
  <book category="fiction">
    <title>Harry Potter and the Sorcerer's Stone</title>
    <author>J.K. Rowling</author>
    <year>1997</year>
  </book>
  <book category="non-fiction">
    <title>The Lean Startup</title>
    <author>Eric Ries</author>
    <year>2011</year>
  </book>
</bookstore>

In this example, the XML document represents a collection of books in a bookstore. Each book is enclosed within the <book> element, and it has attributes such as category. The book's title, author, and year are represented by the <title>, <author>, and <year> elements, respectively.

XML provides a flexible and self-describing structure for representing data, making it easy to exchange information between different systems and platforms.
````
## prevent XXE (XML External Entity) vulnerabilities
````
To prevent XXE (XML External Entity) vulnerabilities, you can apply the following preventive measures in different programming languages and libraries:
````
### Example
````
Use a Secure XML Parser: Ensure that you use a secure XML parser that is not vulnerable to XXE attacks. Many programming languages provide secure XML parsing libraries that disable external entity resolution by default. For example:

Java: Use SAXParserFactory with setFeature("http://javax.xml.XMLConstants/feature/secure-processing", true).
.NET: Use XmlReaderSettings with DtdProcessing set to DtdProcessing.Prohibit.
Python: Use defusedxml library or set the "resolve_entities" option to False in the XML parser.
Disable External Entity Resolution: In XML parsing configurations, disable external entity resolution explicitly. This prevents the parser from resolving external entities, which is the primary cause of XXE vulnerabilities. For example:

Java: Set the feature "http://apache.org/xml/features/disallow-doctype-decl" to true.
.NET: Set the DtdProcessing property of XmlReaderSettings to DtdProcessing.Prohibit.
PHP: Use libxml_disable_entity_loader(true).
Python: Use ET.parse(source, forbid_dtd=True) or set the "resolve_entities" option to False.
Input Validation and Filtering: Validate and filter user input that is used in XML processing. Ensure that user-supplied data is not treated as part of the XML structure, especially when constructing XML dynamically.

Use Whitelisting: Define a whitelist of allowed XML elements, attributes, and entities. Reject any input that contains unknown or unexpected elements, attributes, or entities.

Avoid Dynamic XPath and XSLT: Avoid constructing XPath queries or XSLT templates dynamically using user input. This can prevent injection attacks that could lead to XXE vulnerabilities.

Proper Error Handling: Implement proper error handling and error messages to prevent leakage of sensitive information. Avoid displaying detailed error messages to users, as they might provide attackers with valuable information.

Regularly Update Libraries: Keep XML parsing libraries and frameworks up to date with the latest security patches and updates. This ensures that any known vulnerabilities are addressed.
````
