# -*- coding: iso-8859-15 -*-

from bs4 import BeautifulSoup
import time

def gen_html_css(xml_file):
    '''
    Take an .xml file, scrape information from it and
    generate an .html and .css files to represent that
    information. 
    Note this script is supposed to be run after
    'catalog.py'.
    
    Args:
        xml_file (str): The name of the .xml file (in the
    context of the application it'll be "catalog.xml").

    Returns:
        None
    '''
    # Open the target .xml file
    with open(xml_file, 'r', encoding="iso-8859-15") as f:
        # Read all the content from the file at once
        string = f.read()

    # Extract information from the .xml

    # Convert the read content to bytes, encoded using 'iso-8859-15'
    string = string.encode('iso-8859-15')
    # Create a BeautifulSoup object from the bytes
    xml_soup = BeautifulSoup(string, 'xml', from_encoding='iso-8859-15')
    # A list of all the products in the .xml
    prods = xml_soup.find_all('product')
    # Now extract the actual information from the XML we got from the file
    # Scrape the date and title of the file (these will be the headers\
    # for the web page)
    file_title = 'Worten online store\'s catalog'
    day, month, year = xml_soup.find('catalog')['day'], xml_soup.find('catalog')['month'], xml_soup.find('catalog')['year']
    file_date = "/".join((day, month, year))

    # We are using lists to store the various informations so that we can\
    # cross a single product's data given the index of an item in a list
    # Product IDs
    prod_ids = [prod['id'] for prod in prods]
    # Product availability
    prod_avail = [prod['avail'] for prod in prods]
    # Product page
    prod_pages = [prod['link'] for prod in prods]
    # Product names
    prod_names = [prod.find('name').text for prod in prods]
    # Product prices
    prod_prices = [prod.find('pu').text for prod in prods]
    # Product images
    # Element that contains the images
    prod_images_ = [prod.find_all('image') for prod in prods]
    prod_images = []
    # Extract the image URLs from each element
    for images in prod_images_:
        temp = []
        for img in images:
            temp.append(img['ref'])
        prod_images.append(temp)
    # Product descriptions
    prod_descs = [prod.find('description').text for prod in prods]
    # Product extra informations
    # Elements that contain the various extra informations
    prod_extra_info = [prod.find_all('info') for prod in prods]
    prod_infos = []
    # Extra the extra informations for each product
    for product in prod_extra_info:
        temp = {}
        for info in product:
            temp[info['type']] = info.text
        prod_infos.append(temp)
    num_prods = len(prod_names)


    # Create the .html

    # Create the HTML that will be written to an .html file at the end
    html_string = f'''<!DOCTYPE html>
<html>
<head>
	<title>Worten Daily Catalog</title>
	<link href="catalog.css" type="text/css" rel="stylesheet" />
</head>

<body>
	<h1 id="top">Worten online store's catalog</h1>
	<h2 id="date">Date: 15/12/2018</h2>
	<p class="file-ref"><a href="daily_sales.html">Open Daily Sales Report</a></p>
	<p><a href="auth.html" id="log-out">Log Out</a></p>
	<div class="prod-ref" id="database">
		<table class="database">
			<tr>
				<th>Product Name</th>
				<th>Product Internal ID</th>
				<th>Product Information</th>
				<th>Product Page</th>
			</tr>'''

    # The table rows for the table at the top of the page
    prod_counter = 1
    for i in range(num_prods):
        temp_string = f'\n\t\t\t<tr>' +\
        f'\n\t\t\t\t<td>{prod_names[i]}</td>' +\
        f'\n\t\t\t\t<td>{prod_ids[i]}</td>' +\
        f'\n\t\t\t\t<td><a href="#prod{prod_counter}">Go to product information</a></td>' +\
        f'\n\t\t\t\t<td><a href="{prod_pages[i]}" target="_blank">Product page</a></td>' +\
        f'\n\t\t\t</tr>'
        prod_counter += 1
        html_string += temp_string
    html_string += '\n\t\t</table>\n\t</div>\n'

    # Create the content for each product
    prod_counter = 1
    for i in range(num_prods):
        temp_string = f'\n\t<div class="prod" id="prod{prod_counter}">' +\
        f'\n\t\t<div class="prod-info">' +\
        f'\n\t\t\t<h1 class="prod-name">{prod_names[i]}</h1>'
        if prod_avail[i] == 'In stock':
            temp_string += f'\n\t\t\t<h3 style="background-color: #01a701" class="avail">Availability: {prod_avail[i]}</h3>'
        else:
            temp_string += f'\n\t\t\t<h3 style="background-color: #a70101" class="not-avail">Availability: {prod_avail[i]}</h3>'
        temp_string += f'\n\t\t\t<p class="prod-id">{prod_ids[i]}<p>' +\
        f'\n\t\t\t<img src="{prod_images[i][0]}" alt="Product Picture"/>' +\
        f'\n\t\t\t<p class="prod-desc">{prod_descs[i]}</p>' +\
        f'\n\t\t</div>' +\
        f'\n\t\t<div class="extra-info">' +\
        f'\n\t\t\t<table class="extra">' +\
        f'\n\t\t\t\t<tr>\n\t\t\t\t\t<td>Price</td>\n\t\t\t\t\t<td>€{prod_prices[i]}</td>\n\t\t\t\t</tr>' +\
        f'\n\t\t\t\t<tr>\n\t\t\t\t\t<td>Category</td>\n\t\t\t\t\t<td>{prod_infos[i]["Category"]}</td>\n\t\t\t\t</tr>' +\
        f'\n\t\t\t\t<tr>\n\t\t\t\t\t<td>Brand</td>\n\t\t\t\t\t<td>{prod_infos[i]["Brand"]}</td>\n\t\t\t\t</tr>' +\
        f'\n\t\t\t\t<tr>\n\t\t\t\t\t<td>Weight</td>\n\t\t\t\t\t<td>{prod_infos[i]["Weight"]}</td>\n\t\t\t\t</tr>' +\
        f'\n\t\t\t\t<tr>\n\t\t\t\t\t<td>Dimensions</td>\n\t\t\t\t\t<td>{prod_infos[i]["Dimensions"]}</td>\n\t\t\t\t</tr>' +\
        f'\n\t\t\t\t<tr>\n\t\t\t\t\t<td>Color</td>\n\t\t\t\t\t<td>{prod_infos[i]["Color"]}</td>\n\t\t\t\t</tr>' +\
        f'\n\t\t\t\t<tr>\n\t\t\t\t\t<td>Stock</td>\n\t\t\t\t\t<td>{prod_infos[i]["Stock"]}</td>\n\t\t\t\t</tr>' +\
        f'\n\t\t\t\t</table>\n\t\t\t</div>\n\t\t<p class="top"><a href="#database">Page Top</a></p>\n\t</div>'
        prod_counter += 1
        html_string += temp_string
    html_string += f'\n</body>\n\n</html>'

    with open('catalog.html', 'w', encoding='iso-8859-15') as f:
        f.write(html_string)


    # Create the .css
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
    padding-left: 17px;
}


/* Style the paragraph with an anchor to the Catalog page */
.file-ref {
    border: 1px solid black;
    text-align: center;
    background-color: yellow;
    font-size: 105%;
    width: 15%;
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

/* Top table */

/* Move the product reference table a bit to the left */
.prod-ref {
	padding-left: 15px;
}

/* Format the table at the top of the page with a border. Collapse
the borders so that there's no space in-between cells*/
.database {
	text-align: center;
	border: 2px solid black;
	border-collapse: collapse;
}

/* Text to appear before the table */
.prod-ref:before {
	content: "List of catalog products";
	display: block;
	font-size: 200%;
	margin-bottom: 10px;
}

/* Format the table headers and cells to have a border */
.database th, .database td {
	border: 1px solid black;
}
/* Table rows have white background */
tr {
	background-color: white;
}
/* When hovering over a row, that row's border becomes thicker */
tr:hover {
	border: 2px solid black;
}
/* Table even table rows have grey background */
tr:nth-child(2n+2) {
	background-color: #c5c5c5;
}
/* Table cells have 5px of padding in all directions */
th, td {
	padding: 5px;
}



/* Individual products */

/* Change the background and border for each product */
.prod {
	background: linear-gradient(135deg, #46a3f0, #2036fc);
	padding: 5px 5px 10px 10px;
	margin: 15px;
	border: 2px solid black;
	width: 70%;
}

/* When hovering over a product, change its background and border */
.prod:hover {
	border: 5px solid black;
	background: linear-gradient(135deg, #46f0b7, #007552);
}

/* Make it so that the product's name is not as bold as the HTML makes it */
.prod-name {
	font-weight: lighter;
}

/* Format the availability part */
.avail {
	width: 20%;
	padding: 3px;
	border: 1px dotted #015a01;
}
.not-avail {
	width: 25%;
	padding: 3px;
	border: 1px dotted grey;
}

/* Add text before the product id */
.prod-id:before {
	content: "Product ID: ";
	font-size: 105%;
	font-weight: bold;
}

/* Add information before the product description */
.prod-desc:before {
	content: "Product description: ";
	display: block;
	padding-bottom: 10px;
	font-size: 110%;
	font-weight: bold;
}

/* Add information before the product's extra information */
.extra-info:before {
	content: "More information: ";
	display: block;
	font-size: 110%;
	font-weight: bold;
	margin-bottom: 10px;
}

/* Make the extra information text size bigger */
.extra-info {
	font-size: 105%;
}

/* Adjust the padding for the various elements inside each product */
.prod-info {
	padding: 10px;
}
.prod-id {
	font-size: 120%;
}
div img {
	border: 3px solid grey;
}
.prod-desc {
	padding: 10px;
	text-align:justify;
	width: 70%;
}
.extra-info {
	border-collapse: collapse;
	padding: 10px 10px 3px 10px;
}


/* Product tables */

/* Format the table about a product's extra information */
.extra {
	border-collapse: collapse;
	border: 2px solid grey;
	margin-bottom: 10px;
}
.extra tr {
	border-bottom: 1px solid grey;
	padding: 5px 5px 5px 10px;
}
.extra tr:hover {
	border: 2px solid black;
	padding: 5px;
}

/* Format the Page Top anchor */
.top {
	width: 8%;
	border: 1px solid #a1a14d;
	background: yellow;
	text-decoration: none;
	text-align: center;
	position: relative;
	left: 850px;
}

/* When hovering over the Page Top anchor, make its border thicker */
.top:hover {
	border: 2px solid #a1a14d;
}'''

    with open('catalog.css', 'w') as f:
            f.write(css_string)
    
    return None

if __name__ == '__main__':
    # start = time.time()
    gen_html_css('catalog.xml')
    print('Your Catalog HTML and CSS have been generated.')
    # print('Elapsed time:', round(time.time()-start, 2), 'seconds.')