from random import choice, randint
# from time import time
from datetime import datetime

def create_sales():
    '''
    Create an XML file that represents data about
    the daily sales of an online store (Worten in this
    case). While the represented data is supposedly 
    about Worten, every aspect of the data is 
    randomly generated.
    
    Args:
        None

    Returns:
        xml_string (str): The string with XML.

    '''
    # The start time of the script (to be used for timing\
    # how long it takes to run)
    # start = time()

    # Datasets to generate data from
    names = ['Dave Martin', 'Charles Harris', 'Eric Williams', 'Corey Jefferson', 'Jennifer Martin', 'Erick Davis', 'Neil Patterson', 'Laura Jefferson', 'Maria Johnson', 'Michael Arnold', 'Michael Smith', 'Erik Stuart', 'Laura Martin', 'Patricia Thomas', 'Jennifer Davis', 'Patricia Brown', 'Barbara Williams', 'James Taylor', 'Eric Harris', 'Travis Anderson']
    phones = ['615-555-7164', '800-555-5669', '560-555-5153', '900-555-9340', '714-555-7405', '800-555-6771', '783-555-4799', '516-555-4615', '127-555-1867', '608-555-4938', '568-555-6051', '292-555-1875', '900-555-3205', '614-555-1166', '530-555-2676', '470-555-2750', '800-555-6089', '880-555-8319', '777-555-8378', '998-555-7385']
    addresses = ['173 Main St., Springfield RI 55924', '969 High St., Atlantis VA 34075', '806 1st St., Faketown AK 86847', '826 Elm St., Epicburg NE 10671', '212 Cedar St., Sunnydale CT 74983', '519 Washington St., Olympus TN 32425', '625 Oak St., Dawnstar IL 61914', '890 Main St., Pythonville LA 29947', '884 High St., Braavos ME 43597', '249 Elm St., Quahog OR 90938', '619 Park St., Winterfell VA 99000', '220 Cedar St., Lakeview NY 87282', '391 High St., Smalltown WY 28362', '121 Hill St., Braavos UT 92474', '433 Elm St., Westworld TX 61967', '838 Main St., Balmora MT 56526', '732 High St., Valyria KY 97152', '217 High St., Old-town IA 82767', '191 Main St., Mordor IL 72160', '607 Washington St., Blackwater NH 97183']
    # emails = [''.join(name.split()).lower()+'@email.com' for name in names]

    alphabet= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Variable to hold the internal ID of each client. 
    # The first client will have ID 1,the second 2,\
    # the third 3 and so on
    id_c = 1
    # The same applies to the sales IDs
    id_s = 1
    # List to hold the clients' IDs
    clients = []

    # Start the string that will contain all the XML to be written to the .xml\
    # file (includes the XML header, a reference to an external .dtd file,\
    # the root element and also opens the "macro" <clients> element).
    # Note: tin stands for Taxpayer Identification Number (NIF in Portugal)
    xml_string = '<?xml version="1.0" encoding="UTF-8" ?>' +\
    '\n<!DOCTYPE daily_sales SYSTEM "daily_sales.dtd">' +\
    f'\n<daily_sales day="{datetime.now().day}" month="{datetime.now().month}" year="{datetime.now().year}" store="WORTEN" local="STA. CATARINA" tin="503630330">' +\
    '\n\n\t<clients>\n'

    # Create 5 clients for the XML document
    for i in range(5):
        name = choice(names)
        phone = choice(phones)
        address = choice(addresses)
        # first_name_last_name@email.com
        email = '_'.join(name.split()).lower()+'@email.com'
        # Remove the used data from the datasets to prevent duplicates
        names.remove(name)
        phones.remove(phone)
        addresses.remove(address)
        # Client ID (alphanumeric string)
        client_id = 'C' + str(id_c)
        # Append the client ID to the list of client ids
        clients.append(client_id)
        # Generate a Taxpayer Identification Number (TIN) for the client
        tin_c = str(randint(111111111,999999999))
        # Increment the counter for the next client
        id_c += 1
        # Create the elements (with its respective attributes) to be\
        # written to the .xml file using the generated information
        xml_string += f'\n\t\t<client id_c="{client_id}" tin_c="{tin_c}">' +\
        f'\n\t\t\t<name>{name}</name>' +\
        f'\n\t\t\t<address locality="{choice(alphabet)}">{address}</address>' +\
        f'\n\t\t\t<contacts>' +\
        f'\n\t\t\t\t<contact type="PHONE NUMBER">{phone}</contact>' +\
        f'\n\t\t\t\t<contact type="EMAIL">{email}</contact>' +\
        f'\n\t\t\t</contacts>' +\
        f'\n\t\t</client>' +\
        f'\n'

    # After creating the XML for the 5 clients, close the "macro" <clients>
    # element
    xml_string += '\n\t</clients>\n'

    # Open a second "macro" element, this time for <sales>
    xml_string += '\n\t<sales>\n'

    # Create 5 different sales
    for i in range(5):
        # Create the ID for the sale
        sale_id = 'S' + str(id_s)
        # Increment the counter for the next sale's ID
        id_s += 1
        # Number of items in the sale
        total_quant = 0
        # List of IDs of products bought in this sale
        products = []
        # List of how many of each product were bought for this sale
        quants = []
        # Each sale will include between 1 to 3 different items
        for i in range(randint(1,3)):
            # Generate a random product ID (alphanumeric string)
            product_id = 'P' + str(randint(1000000, 9999999))
            products.append(product_id)
            # Each product can be bought in quantities between 1 and 10
            quantity = randint(1, 10)
            quants.append(quantity)
            total_quant += quantity
        # Randomize the price of the product, per unit
        price = randint(5, 1500)
        # Generate the shipping price, based on the quantity bought
        shipping = 2.5 * total_quant
        # Calculate the final price of the sale
        final_price = (price*quantity) + shipping
        # Choose to change the delivery and invoice addresses or not
        change_address1 = choice(('Y', 'N'))
        change_address2 = choice(('Y', 'N'))
        # If it chose to change the address, pick another address from the dataset
        # If it chose "no" ('N'), then this will be an empty element in the XML, to denote\
        # the delivery address for the sale is the same as the one registered in the client\
        # information
        if change_address1 == 'Y':
            delivery_address = choice(addresses)
            addresses.remove(delivery_address)
            del_locality = choice(alphabet)
        else:
            delivery_address = ''

        if change_address2 == 'Y':
            invoice_address = choice(addresses)
            addresses.remove(invoice_address)
            del_locality = choice(alphabet)
        else:
            invoice_address = ''
        
        xml_string += f'\n\t\t<sale id_s="{sale_id}" client="{choice(clients)}" unit="EURO">' +\
        '\n\t\t\t<products>'
        for i in range(len(products)):
            xml_string += f'\n\t\t\t\t<product quantity="{quants[i]}">{products[i]}</product>'
        xml_string += f'\n\t\t\t</products>' +\
        f'\n\t\t\t<order_price>{final_price-shipping}</order_price>' +\
        f'\n\t\t\t<shipping>{shipping}</shipping>' +\
        f'\n\t\t\t<final_price>{final_price}</final_price>'
        if change_address1 == 'Y':
            xml_string += f'\n\t\t\t<delivery_address locality="{del_locality}">{delivery_address}</delivery_address>'
        else:
            xml_string += f'\n\t\t\t<delivery_address></delivery_address>'
        if change_address2 == 'Y':
            xml_string += f'\n\t\t\t<invoice_address locality="{del_locality}">{invoice_address}</invoice_address>'
        else:
            xml_string += f'\n\t\t\t<invoice_address></invoice_address>'
        xml_string += f'\n\t\t</sale>\n'
        
    # Finally finish formatting the string that contains the XML to\
    # be written to the file
    xml_string += '\n\t</sales>\n' +\
    '\n</daily_sales>'
    
    # print('Elapsed time:', round(time() - start, 6), 'seconds.')

    return xml_string


if __name__ == '__main__':
    # Call the function to generate the XML
    xml_string = create_sales()

    # Create an .xml file and write the string with XML to it
    with open('daily_sales.xml' , 'w') as f:
        f.write(xml_string)

    # String with the data to be written to the .dtd file
    dtd_string = '''<!ELEMENT daily_sales (clients, sales)>
<!ELEMENT clients (client+)>
<!ELEMENT client (name, address, contacts)>
<!ELEMENT name (#PCDATA)>
<!ELEMENT address (#PCDATA)>
<!ELEMENT contacts (contact+)>
<!ELEMENT contact (#PCDATA)>
<!ELEMENT sales (sale+)>
<!ELEMENT sale (products, order_price, shipping, final_price, delivery_address, invoice_address)>
<!ELEMENT products (product+)>
<!ELEMENT product (#PCDATA)>
<!ELEMENT product_id (#PCDATA)>
<!ELEMENT quantity (#PCDATA)>
<!ELEMENT order_price (#PCDATA)>
<!ELEMENT shipping (#PCDATA)>
<!ELEMENT final_price (#PCDATA)>
<!ELEMENT delivery_address (#PCDATA)>
<!ELEMENT invoice_address (#PCDATA)>

<!ATTLIST daily_sales day CDATA #REQUIRED
					month CDATA #REQUIRED
					year CDATA #REQUIRED
					store CDATA #REQUIRED
					local CDATA #REQUIRED
					tin CDATA #REQUIRED>
<!ATTLIST client id_c ID #REQUIRED
					tin_c CDATA #REQUIRED>
<!ATTLIST address locality CDATA #REQUIRED>
<!ATTLIST contact type CDATA #REQUIRED>
<!ATTLIST sale id_s CDATA #REQUIRED
					client IDREF #REQUIRED
					unit CDATA #REQUIRED>
<!ATTLIST product quantity CDATA #REQUIRED>
<!ATTLIST delivery_address locality CDATA #IMPLIED>
<!ATTLIST invoice_address locality CDATA #IMPLIED>'''

    with open('daily_sales.dtd', 'w') as f:
        f.write(dtd_string)
    
    print('The daily sales report has been created.\n')