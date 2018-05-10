# -*- coding: iso-8859-15 -*-

'''
Take an .xml file, scrape information from it and
generate an .html and .css files to represent that
information. 
Note this script is supposed to be run after
'catalog.py'.
'''

from bs4 import BeautifulSoup
import time

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
    # A list of all the products in the .xml
    prods = xml_soup.find_all('product')
    # Now extract the actual information from the XML we got from the file
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
    html_string = '''<!DOCTYPE html>
        <html>
            <head>
                <title>Worten Daily Catalog</title>
                <link href="catalog.css" type="text/css" rel="stylesheet" />
            </head>

            <body>
                <div class="prod-ref" id="database">
                    <table class="database">
                        <tr>
                            <th>Product Name</th>
                            <th>Product Internal ID</th>
                            <th>Product Information</th>
                            <th>Product Page</th>
                        </tr>
    '''

    # The table rows for the table at the top of the page
    prod_counter = 1
    for i in range(num_prods):
        temp_string = f'\n\t\t\t\t\t<tr>' +\
        f'\n\t\t\t\t\t\t<td>{prod_names[i]}</td>' +\
        f'\n\t\t\t\t\t\t<td>{prod_ids[i]}</td>' +\
        f'\n\t\t\t\t\t\t<td><a href="#prod{prod_counter}">Go to product information</a></td>' +\
        f'\n\t\t\t\t\t\t<td><a href="{prod_pages[i]}" target="_blank">Product page</a></td>' +\
        f'\n\t\t\t\t\t</tr>'
        prod_counter += 1
        html_string += temp_string
    html_string += '\n\t\t\t\t</table>\n\t\t\t</div>\n'

    # Create the content for each product
    prod_counter = 1
    for i in range(num_prods):
        temp_string = f'\n\t\t<div class="prod" id="prod{prod_counter}">' +\
        f'\n\t\t\t<div class="prod-info">' +\
        f'\n\t\t\t\t<h1 class="prod-name">{prod_names[i]}</h1>'
        if prod_avail[i] == 'In stock':
            temp_string += f'\n\t\t\t\t<h3 style="background-color: #01a701" class="avail">Availability: {prod_avail[i]}</h3>'
        else:
            temp_string += f'\n\t\t\t\t<h3 style="background-color: #a70101" class="not-avail">Availability: {prod_avail[i]}</h3>'
        temp_string += f'\n\t\t\t\t<p class="prod-id">{prod_ids[i]}<p>' +\
        f'\n\t\t\t\t<img src="{prod_images[i][0]}" alt="Product Picture"/>' +\
        f'\n\t\t\t\t<p class="prod-desc">{prod_descs[i]}</p>' +\
        f'\n\t\t\t</div>' +\
        f'\n\t\t\t<div class="extra-info">' +\
        f'\n\t\t\t\t<table class="extra">' +\
        f'\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<td>Price</td>\n\t\t\t\t\t\t<td>€{prod_prices[i]}</td>\n\t\t\t\t\t</tr>' +\
        f'\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<td>Category</td>\n\t\t\t\t\t\t<td>{prod_infos[i]["Category"]}</td>\n\t\t\t\t\t</tr>' +\
        f'\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<td>Brand</td>\n\t\t\t\t\t\t<td>{prod_infos[i]["Brand"]}</td>\n\t\t\t\t\t</tr>' +\
        f'\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<td>Weight</td>\n\t\t\t\t\t\t<td>{prod_infos[i]["Weight"]}</td>\n\t\t\t\t\t</tr>' +\
        f'\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<td>Dimensions</td>\n\t\t\t\t\t\t<td>{prod_infos[i]["Dimensions"]}</td>\n\t\t\t\t\t</tr>' +\
        f'\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<td>Color</td>\n\t\t\t\t\t\t<td>{prod_infos[i]["Color"]}</td>\n\t\t\t\t\t</tr>' +\
        f'\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<td>Stock</td>\n\t\t\t\t\t\t<td>{prod_infos[i]["Stock"]}</td>\n\t\t\t\t\t</tr>' +\
        f'\n\t\t\t\t\t</table>\n\t\t\t\t</div>\n\t\t<p class="top"><a href="#database">Page Top</a></p>\n\t\t</div>'
        prod_counter += 1
        html_string += temp_string
    html_string += f'\n\t</body>\n\n</html>'

    with open('catalog.html', 'w', encoding='iso-8859-15') as f:
        f.write(html_string)


    # Create the .css
    css_string = '''body {
        background: linear-gradient(135deg, #c7503b,#a80404);
        font-family: Lato,sans-serif;
    }




    .prod-ref {
        padding-left: 15px;
    }

    .database {
        text-align: center;
        border: 2px solid black;
        border-collapse: collapse;
    }

    .prod-ref:before {
        content: "List of catalog products";
        display: block;
        font-size: 200%;
    }

    .database th, .database td {
        border: 1px solid black;
    }
    tr {
        background-color: white;
    }
    tr:hover {
        border: 2px solid black;
    }
    tr:nth-child(2n+2) {
        background-color: #c5c5c5;
    }
    th, td {
        padding: 5px;
    }




    .prod {
        background: linear-gradient(135deg, #46a3f0, #2036fc);
        padding: 5px 5px 10px 10px;
        margin: 15px;
        border: 2px solid black;
        width: 70%;
    }

    .prod:hover {
        border: 5px solid black;
        background: linear-gradient(135deg, #46f0b7, #007552);
    }

    .prod-name {
        font-weight: lighter;
    }

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

    .prod-id:before {
        content: "Product ID: ";
        font-size: 105%;
        font-weight: bold;
    }

    .prod-desc:before {
        content: "Product description: ";
        display: block;
        padding-bottom: 10px;
        font-size: 110%;
        font-weight: bold;
    }

    .extra-info:before {
        content: "More information: ";
        display: block;
        font-size: 110%;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .extra-info {
        font-size: 105%;
    }

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

    .top {
        width: 8%;
        border: 1px solid #a1a14d;
        background: yellow;
        text-decoration: none;
        text-align: center;
        position: relative;
        left: 850px;
    }

    .top:hover {
        border: 2px solid #a1a14d;
    }'''

    with open('catalog.css', 'w') as f:
            f.write(css_string)

if __name__ == '__main__':
    start = time.time()
    gen_html_css('catalog.xml')
    print('Your HTML and CSS have been generated.')
    print('Elapsed time:', round(time.time()-start, 2), 'seconds.')