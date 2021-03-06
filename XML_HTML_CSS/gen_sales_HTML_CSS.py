# -*- coding: iso-8859-15 -*-

'''
Take an .xml file, scrape information from it and
generate an .html and .css files to represent that
information. 
Note this script is supposed to be run after
'daily_sales.py'.
'''

from bs4 import BeautifulSoup
# import time
from datetime import datetime

def gen_html_css(xml_file):
    # Open the target .xml file
    with open(xml_file, 'r', encoding="iso-8859-15") as f:
        # Read all the content from the file at once
        string = f.read()

    # Extract information from the .xml

    # Convert the read content to bytes, encoded using 'iso-8859-15'
    string = string.encode('iso-8859-15')
    # Create a BeautifulSoup object from the bytes
    xml_soup = BeautifulSoup(string, 'xml', from_encoding='iso-8859-15')

    # Now scrape information
    # Scrape the date and title of the file (these will be the headers\
    # for the web page)
    file_title = 'Worten online store\'s daily sales report'
    day, month, year = xml_soup.find('daily_sales')['day'], xml_soup.find('daily_sales')['month'], xml_soup.find('daily_sales')['year']
    file_date = "/".join((day, month, year))

    # Scrape the client "profiles"
    clients = xml_soup.find_all('client')
    # A dictionary where the key-values are\
    # client_id--client_info, given that\
    # client_info is a dictionary itself with the\
    # various elements of a client profile
    clients_info = {}
    for client in clients:
        temp = {}
        temp['id'] = client['id_c']
        temp['tin'] = client['tin_c']
        temp['name'] = client.find('name').text
        temp['locality'] = client.find('address')['locality']
        temp['address'] = client.find('address').text
        contacts = client.find('contacts').find_all('contact')
        temp['phone'] = contacts[0].text
        temp['email'] = contacts[1].text
        clients_info[temp['id']] = temp


    # Scrape the sales' info
    sales = xml_soup.find_all('sale')
    sales_info = {}
    for sale in sales:
        temp = {}
        temp['id'] = sale['id_s']
        temp['client'] = sale['client']
        temp['products'] = sale.find('products')
        temp['subtotal'] = sale.find('order_price').text
        temp['shipping'] = sale.find('shipping').text
        temp['final_price'] = sale.find('final_price').text
        temp['delivery_address'] = sale.find('delivery_address').text
        temp['invoice_address'] = sale.find('invoice_address').text
        sales_info[temp['id']] = temp
    # Set of client ids that placed orders today
    clients_active = {sales_info[sale]['client'] for sale in sales_info}

    # A dictionary to hold the products sold in each sale: each sale\
    # is mapped to a dictionary that contains a mapping of products ids\
    # and the quantity sold that product
    products_sold = {}
    for sale in sales_info:
        temp = {}
        for product in sales_info[sale]['products'].find_all('product'):
            temp[product.text] = product['quantity']
        products_sold[sale] = temp
                    


    # Create the HTML
    # The document headers and the head element is always the same
    html_string = f'''<!DOCTYPE html>
<html>
<head>
    <title>Worten Daily Sales</title>
    <link href="daily_sales.css" type="text/css" rel="stylesheet" />
</head>

<body>
    <h1 id="top">Worten online store's daily sales report</h1>
    <h2 id="date">Date: {datetime.now().day}/{datetime.now().month}/{datetime.now().year}</h2>
    <p class="file-ref"><a href="catalog.html">Open Catatalog</a></p>
    <p><a href="auth.html" id="log-out">Log Out</a></p>

    <section class="first-table">
        <h2>Tables' Summary</h2>
        <table class="table-summary">
            <tr>
                <th><a href="#clients-sales">Clients/Sales</a></th>
                <th><a href="#clients">Clients</a></th>
                <th><a href="#sales">Sales</a></th>
                <th><a href="#products">Products</a></th>
            </tr>
        </table>
        <p class="top"><a href="#top">Page Top</a></p>
    </section>

    <section class="second-table">
        <h2>Clients/Sales' Table</h2>
        <table id="clients-sales">
            <tr>
                <th>Client ID</th>
                <th>Sale ID</th>
                <th>Subtotal</th>
                <th>Shipping</th>
                <th>Final Price</th>
            </tr>
'''
    # Create the Client/Sales table. For this we need to use\
    # the data scraped to the 'sales_info' dictionary
    for sale in sales_info:
        temp = f'''\n\t\t\t<tr>
                <td><a href="#{sales_info[sale]['client']}">{sales_info[sale]['client']}</a></td>
                <td><a href="#{sales_info[sale]['id']}">{sales_info[sale]['id']}</a></td>
                <td>€{sales_info[sale]['subtotal']}</td>
                <td>€{sales_info[sale]['shipping']}</td>
                <td>€{sales_info[sale]['final_price']}</td>
            </tr>'''
        html_string += temp
    # Close elements involved with the Client/Sales table
    html_string += '''\n\t\t</table>
        <p class="top"><a href="#top">Page Top</a></p>
    </section>'''
    # Create the Client's table
    html_string += '''\n\n\t<section class="third-table">
        <h2>Client's Table</h2>
        <table id="clients">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>TIN</th>
                <th>Locality</th>
                <th>Address</th>
                <th>Phone Number</th>
                <th>E-mail</th>
            </tr>'''
    # Fill the Client's table with data. For this we need\
    # to use the data scraped to the 'clients_info' dictionary
    for client in clients_info:
        if client in clients_active:
            temp = f'''\n\t\t\t<tr>
                <td id="{client}">{client}</td>
                <td>{clients_info[client]['name']}</td>
                <td>{clients_info[client]['tin']}</td>
                <td>{clients_info[client]['locality']}</td>
                <td>{clients_info[client]['address']}</td>
                <td>{clients_info[client]['phone']}</td>
                <td>{clients_info[client]['email']}</td>
            </tr>'''
            html_string += temp
    # Close elements involved with the Clients' table
    html_string += '''\n\t\t</table>
        <p class="top"><a href="#top">Page Top</a></p>
    </section>'''
    # Create the Sales' table
    html_string += '''\n\n\t<section class="fourth-table">
        <h2>Sales' Table</h2>
        <table id="sales">
            <tr>
                <th>Sale ID</th>
                <th>Client ID</th>
                <th>Product IDs/<br>Quantities</th>
                <th>Subtotal</th>
                <th>Shipping</th>
                <th>Final Price</th>
                <th>Delivery Address</th>
                <th>Invoice Address</th>
            </tr>'''
    # Fill the Sales' table with data
    for sale in sales_info:
        temp = f'''\n\t\t\t<tr>
                <td id="{sale}">{sale}</td>
                <td><a href="#{sales_info[sale]['client']}">{sales_info[sale]['client']}</a></td>
                <td>
                    <ul>'''
        for product in products_sold[sale]:
            temp += f'\n\t\t\t\t\t\t<li>{product} / {products_sold[sale][product]}</li>'
        temp += f'''\n\t\t\t\t\t</ul>
                </td>
                <td>€{sales_info[sale]['subtotal']}</td>
                <td>€{sales_info[sale]['shipping']}</td>
                <td>€{sales_info[sale]['final_price']}</td>
                <td>{sales_info[sale]['delivery_address']}</td>
                <td>{sales_info[sale]['invoice_address']}</td>
            </tr>'''
        html_string += temp
    # Close the elements related to the Sales' table
    html_string += '''\n\t\t</table>
        <p class="top"><a href="#top">Page Top</a></p>
    </section>'''
    # Create the Products' table
    html_string += '''\n\n\t<section class="fifth-table">
        <h2>Product's Table</h2>
        <table id="products">
            <tr>
                <th>Product ID</th>
                <th>Quantity Sold</th>
            </tr>'''
    # Fill the Products' table with data
    for sale in products_sold:
        for product in products_sold[sale]:
            temp = f'''\n\t\t\t<tr>
                <td>{product}</td>
                <td>{products_sold[sale][product]}</td>
            </tr>'''
            html_string += temp
    # Close the elements involved with the Products' table
    html_string += '''\n\t\t</table>
        <p class="top"><a href="#top">Page Top</a></p>
    </section>'''
    # Close the body and end the HTML document
    html_string += '\n\n</body>\n\n</html>'

    # Now write the HTML to an .html file
    with open('daily_sales.html', 'w', encoding='iso-8859-15') as f:
        f.write(html_string)



    # Create the CSS
    css_string = '''/* Use a gradient as the background for the whole page */
body {
    background: linear-gradient(135deg, #c7503b,#a80404);
    font-family: Lato,sans-serif;
}

/* Add the worten logo a the top of the page */
/* https://stackoverflow.com/questions/12082948/resize-the-content-propertys-image */
#top:before {
	/* Display the logo in is own line */
	display: block;
	/* Define the width and height for the image to occupy */
    width: 250px;
	height: 80px;
	/* Needed to make the image appear */
	content: "";
	background: url("https://logosinside.com/uploads/posts/2016-09/medium/worten-logo.png") no-repeat;	
	/* Make it so the image rendering origin position is the top left of its box */
	background-origin: 0;
	/* Make it so x% of the image is resized to the size of the box */
	background-size: 100%;
	background-color: white;
	border: 2px solid black;
	margin-bottom: 30px;
}


/* Adjust the padding for the headers  */
#top, #date {
    margin-top: 17px;
    padding-left: 17px;
}


/* Style the paragraph with an anchor to the Catalog page */
.file-ref {
    border: 1px solid black;
    text-align: center;
    background-color: yellow;
    font-size: 105%;
    width: 10%;
    padding: 5px;
	font-weight: bold;
	margin-left: 17px;
}

/* Style the Log Out button */
#log-out {
    border: 1px solid black;
    text-align: center;
    background-color: yellow;
    font-size: 105%;
    width: 15%;
    padding: 5px;
	font-weight: bold;
	margin-left: 17px;
}


/* Make the a row thicker when hovering over it. This applies
    to any table */
tr:hover {
    border: 2px solid black;
}


/* The type of bullet used for list items is 'none'. Also add
    an extra 25px of padding to their right side */
li {
    padding-right: 25px;
    list-style-type: none;
}


/* Format each <section>, knowing that each <section> contains one table and a
    "Page Top" anchor */
section {
    background: linear-gradient(135deg, #46a3f0, #2036fc);
    padding: 5px 5px 10px 10px;
    margin: 15px;
    border: 2px solid black;
}
/* When hovering over a section, change its background and border */
section:hover {
    border: 3px solid black;
    background: linear-gradient(135deg, #46f0b7, #007552);
}


/* Format the first table's borders */
.table-summary {
    border-collapse: collapse;
    text-align: center;
    border: 2px solid black;
    background-color: white;
    color: black;
}
.table-summary th {
    border: 1px solid black;
}


/* Format the Clients/Sales table */
#clients-sales {
    border-collapse: collapse;
    text-align: center;
    border: 2px solid black;
    background-color: white;
    color: black;
}
#clients-sales th, #clients-sales td {
    border: 1px solid black;
    padding: 5px;
}
/* The even rows will have a different background
    color */
#clients-sales tr:nth-child(2n+2) {
    background-color: #c5c5c5;
}


/* Format the Clients table */
#clients {
    border-collapse: collapse;
    text-align: center;
    border: 2px solid black;
    background-color: white;
    color: black;
}
#clients th, #clients td {
    border: 1px solid black;
    padding: 5px;
}
/* The even rows will have a different background
    color */
#clients tr:nth-child(2n+2) {
    background-color: #c5c5c5;
}


/* Format the Sales table */
#sales {
    border-collapse: collapse;
    text-align: center;
    border: 2px solid black;
    background-color: white;
    color: black;
}
#sales th, #sales td {
    border: 1px solid black;
    padding: 5px;
}
/* The even rows will have a different background
    color */
#sales tr:nth-child(2n+2) {
    background-color: #c5c5c5;
}


/* Format the Products table */
#products {
    border-collapse: collapse;
    text-align: center;
    border: 2px solid black;
    background-color: white;
    color: black;
}
#products th, #products td {
    border: 1px solid black;
    padding: 5px;
}
/* The even rows will have a different background
    color */
#products tr:nth-child(2n+2) {
    background-color: #c5c5c5;
}


/* Format the Page Top anchor */
.top {
    width: 8%;
    border: 1px solid #a1a14d;
    background: yellow;
    text-decoration: none;
    text-align: center;
    position: relative;
    left: 1150px;
}
/* When hovering over the "Page Top" anchor, make its border thicker */
.top:hover {
    border: 2px solid #a1a14d;
}'''

    # Write the CSS to a .css file
    with open('daily_sales.css', 'w') as f:
        f.write(css_string)

if __name__ == '__main__':
    # start = time.time()
    gen_html_css('daily_sales.xml')
    print('Your Daily Sales HTML and CSS have been generated.')
    # print('Elapsed time:', round(time.time()-start, 2), 'seconds.')