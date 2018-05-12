# http://docs.python-requests.org/en/master/
from requests import post, get
# https://beautiful-soup-4.readthedocs.io/en/latest/
from bs4 import BeautifulSoup
from time import time
from random import randint

def scrape(args):
    '''
    Make a query to worten.pt. Then open the page of the
    result and scrape information about it. The function will
    return a string with xml about that page (product).

    Args:
        args (str): the query parameters.
    
    Returns:
        xml_text (str): a string with XML about the scraped product page.
    '''

    # Use a try/except clause in case something goes wrong with\
    # the GET requests or the creation of the BeautifulSoup\
    # objects
    try:
        # Target website
        target = 'https://www.worten.pt'
        # String formatting to accomodate query with multiple words
        args = args.replace(' ', '+')
        # Make a get request to get a text version of the query results
        query = get('https://www.worten.pt/search?sortBy=relevance&hitsPerPage=24&page=1&query='+args)
        # Create a BeautifulSoup object to hold the scraped html, encoding the raw data from\
        # the Response object with iso-8859-15
        soup = BeautifulSoup(query.content, 'lxml', from_encoding="iso-8859-15")

        # Product page for the first result of the query
        prod_link = target + soup.find('div', class_='w-product__wrapper').a["href"]
        # Text version of the product's page source code
        product_page = get(prod_link)
        # Create a new BeautifulSoup object for the product's page, encoding the raw data from\
        # the Response object with iso-8859-15
        soup = BeautifulSoup(product_page.content, 'lxml', from_encoding="iso-8859-15")
    
    # If something does go wrong, the function ends here by returning None
    except:
        return None

    # Product detailed info (this section of the source code will be worked on ahead)
    more_info = soup.find('div', class_='w-product-details__wrapper').div

    # Product availability
    try:
        # This actually doesn't work for products not available, but at the time of writing I\
        # couldn't find products out of stock to look at its HTML (which I assume will be\
        # different, hence the try/except clause)
        prod_avail = soup.find('button', class_='w-btn-store-locator__available').div.text.strip()
        prod_avail = 'In stock'
    except:
        prod_avail = 'Out of stock'
    
    # Product name
    prod_name = more_info.header.h2.find('span', class_='w-section__product').text.strip()

    # Product category (a single <ul> contains one or more <li> tags, each containing <a> tags\
    # that contain the text we want, the categories)
    prod_cat = soup.find('ul', class_='w-breadcrumbs breadcrumbs').find_all('li')[-1].a.text.strip()

    # Product current price (if it's on sale, scrapes the discounted price)
    prod_price = soup.find('span', class_='w-product__price__current')['content']

    # Product pictures' links
    # The try clause is for cases where the product has 5 pictures or less
    try:
        pics = soup.find('div', class_='swiper-container w-product-gallery__thumbnails swiper__off').find_all('div', class_='swiper-slide')
        pictures = [target+pic.a.img["src"] for pic in pics]
    # The except clause is run when a product has 6 or more pictures
    # We need to use a different line of code for products with more\
    # than 5 pictures because the source HTML is different for these cases
    except:
        pics = soup.find('div', class_='swiper-wrapper').find_all('div')
        pictures = [target+pic.a.img["src"] for pic in pics]

    # Product description
    try:
        prod_desc = soup.find('div', class_='w-section__wrapper__content').find_all('p')[1].text.strip()
    # If there's a problem scraping the product's description (such as it being nonexistent), just\
    # create a string telling the information is not available
    except:
        prod_desc = 'Product description not available'

    # Left column info (Usually "Referências", "Características Físicas" and "Mais Informações")
    left_col = more_info.find('div', class_='w-product-details__column w-product-details__moreinfo show-for-medium')
    # Scrapes the titles of each list of aspects in the left column
    l_col_titles = [col.text.strip() for col in left_col.find_all('p')]
    # Scrapes the <ul> tags from the previous section, that is, just the lines\
    # of the list without the title
    l_info_ULs = [col for col in left_col.find_all('ul')]
    # Scrapes <li> tags nested in the previous <ul> tags, that is, each <li>\
    # corresponds to a line of the list of information
    l_info_LIs = [col.find_all('li') for col in l_info_ULs]

    # Product internal reference
    # We scrape this one "directly" because it is always the first value of\
    # the first list in the left column
    prod_ref = l_info_ULs[0].li.find('span', class_='details-value').text.strip()
    
    # Initialize strings to hold information about these aspects of the product
    # They begin as empty strings, so that if they are still empty after trying\
    # to scrape that information, it is assumed the information is not available
    prod_brand = ''
    prod_weight = ''
    prod_dimensions = ''
    prod_color = ''
    # Loop through the <li> elements of the left column, looking for the desired\
    # aspects
    # Note we need a nested for loop, since in the outer loop we loop through the\
    # an iterable of <li> tags stored in the 'l_info_LIs' list, that is,\
    # we are simply looping through that list in the outer loop. In the nested\
    # loop, we loop through each <li> of each of those iterables (which are\
    # the lists of information from the left column of the product specifications)
    for lst in l_info_LIs:
        for li in lst:
            if 'Referência Worten' in li.find('span', class_='details-label').text:
                prod_ref = li.find('span', class_='details-value').text.strip()

            if 'Marca' in li.find('span', class_='details-label').text:
                prod_brand = li.find('span', class_='details-value').text.strip()
            
            if 'Peso' in li.find('span', class_='details-label').text:
                prod_weight = li.find('span', class_='details-value').text.strip()

            # Even though 'Altura', 'Largura' and 'Profundidade' (Height, Width, Depth) will\
            # all make a up a single Dimensions values, they need to be scraped separately
            if 'Altura' in li.find('span', class_='details-label').text:
                prod_dimensions += li.find('span', class_='details-value').text.strip() + '*'

            if 'Largura' in li.find('span', class_='details-label').text:
                prod_dimensions += li.find('span', class_='details-value').text.strip() + '*'

            if 'Profundidade' in li.find('span', class_='details-label').text:
                prod_dimensions += li.find('span', class_='details-value').text.strip()

            if 'Cor' in li.find('span', class_='details-label').text:
                prod_color = li.find('span', class_='details-value').text.strip()

    # After trying to scrape information about these aspects, if the strings are\
    # still empty then just assume the information about said aspects is not\
    # available
    else:
        if not prod_brand:
            prod_brand = 'Information not available'
        if not prod_weight:
            prod_weight = 'Information not available'
        if not prod_dimensions:
            prod_dimensions = 'Information not available'
        if not prod_color:
            prod_color = 'Information not available'

    # Add a letter to the beginning of the product reference, so it is\
    # an alphanumeric string (this way it is an ID in XML)
    prod_ref = 'P' + prod_ref    

    # Create a random stock for the product, taking into acount its\
    # availability
    prod_stock = 0 if prod_avail == 'Out of stock' else randint(1, 100)

    '''
    # Create a single string to contain all the scraped info, to be saved in a .txt file
    txt_text = f'Title of the product found: {prod_name}\n' +\
    f'Link to the product\'s page: {prod_link}\n' +\
    f'Product category: {prod_cat}\n' +\
    f'Product price: {prod_price}\n' +\
    f'Product availability: {prod_avail}\n' +\
    f'Links for available pictures: {pictures}\n' +\
    f'Product internal reference number: {prod_ref}\n' +\
    f'Product description: {prod_desc}\n' +\
    f'Product brand: {prod_brand}\n' +\
    f'Product weight: {prod_weight}\n' +\
    f'Product dimensions: {prod_dimensions}\n' +\
    f'Product color: {prod_color}\n' +\
    f'Product stock: {prod_stock}' + '\n\n\n'
    '''

    # Create a single string to contain all the scraped info, to be save in a .xml file
    xml_text = f'\n\n\t<product id="{prod_ref}" avail="{prod_avail}" link="{prod_link}">'+\
    f'\n\t\t<name>{prod_name}</name>' +\
    f'\n\t\t<pu>{prod_price}</pu>'+\
    f'\n\t\t<images>'
    for image in pictures:
        xml_text += f'\n\t\t\t<image ref="{image}"/>'
    xml_text += f'\n\t\t</images>' +\
    f'\n\t\t<description>{prod_desc}</description>'+\
    f'\n\t\t<extra_info>' +\
    f'\n\t\t\t<info type="Category">{prod_cat}</info>'+\
    f'\n\t\t\t<info type="Brand">{prod_brand}</info>'+\
    f'\n\t\t\t<info type="Weight">{prod_weight}</info>'+\
    f'\n\t\t\t<info type="Dimensions">{prod_dimensions}</info>'+\
    f'\n\t\t\t<info type="Color">{prod_color}</info>'+\
    f'\n\t\t\t<info type="Stock">{prod_stock}</info>'
    xml_text += f'\n\t\t</extra_info>' +\
    f'\n\t</product>\n'

    return xml_text



def write_xml():
    '''
    Call the scrape function to scrape product pages on worten.pt. This
    function is responsible for receiving input from the user about what
    queries to make, along with organizing the XML strings.

    Args:
        None
    
    Returns:
        scraped (str): a string with XML.
    '''

    # Will hold XML for the scraped products
    scraped = ''''''
    # Initialize as True to run the loop, but it will be a string when used
    arg = True

    # Counter to keep track of how many times the main function\
    # returned prematurely
    error_count = 0
    while arg:
        # Time how long it takes to run each iteration of the loop
        start = time()
        # Ask the user for the tags to be searched for
        arg = input('Enter tags for the query (enter nothing to finish scraping products): ')
        # If the user entered a valid input (if not the\
        # loop will be terminated in the next iteration)
        if arg:
            # If the function was executed without\
            # raising exceptions, then write the returned info\
            # to a .txt file and organize the XML-string to be\
            # written to an .xml file
            scrape_results = scrape(arg)
            if scrape_results:
                scraped += scrape_results
                print('The product has been scraped.')
                # print('Elapsed time:', round(time()-start, 2), 'seconds.')
                print()
            # If it raised exceptions (specifically in the GET requests,\
            # move on to the next iteration of the loop a.k.a. ask for new\
            # input)
            else:
                print('Oops, something went wrong. Please try again.')
                error_count += 1
                # If the main function returned prematurely three times
                if error_count == 3:
                    print('It\'s the third time the script can\'t retrieve information properly.')
                    # Assign 'arg' to be an empty string so that the loop will terminate
                    arg = ''
    else:
        scraped += '\n</catalog>'
        print()
    return scraped



if __name__ == '__main__':
    # The beginning of the .xml, with the header, .dtd location and root element
    xml_string = f'''<?xml version="1.0" encoding="iso-8859-15" ?>
<!DOCTYPE catalog SYSTEM "catalog.dtd">
<catalog day="{randint(1,31)}" month="{randint(1,12)}" year="2018" store="Worten">'''

    # This will prompt the user for tags for the queries, scrape the information\
    # and return it as XML in a string
    xml_string += write_xml()

    # Write the formatted string with XML to the .xml file
    with open('catalog.xml', 'w', encoding="iso-8859-15") as f:
        f.write(xml_string)

    # The data to be written to the .dtd file that will validate the .xml
    dtd_string = '''<!ELEMENT catalog (product+)>
<!ELEMENT product (name, pu, images, description, extra_info)>
<!ELEMENT name (#PCDATA)>
<!ELEMENT pu (#PCDATA)>
<!ELEMENT images (image+)>
<!ELEMENT image EMPTY>
<!ELEMENT description (#PCDATA)>
<!ELEMENT extra_info (info+)>
<!ELEMENT info (#PCDATA)>

<!ATTLIST catalog day CDATA #REQUIRED
				month CDATA #REQUIRED
				year CDATA #REQUIRED
				store CDATA #REQUIRED>
<!ATTLIST product id ID #REQUIRED
				avail CDATA #REQUIRED
				link CDATA #REQUIRED>
<!ATTLIST link ref CDATA #REQUIRED>
<!ATTLIST image ref CDATA #REQUIRED>
<!ATTLIST info type CDATA #REQUIRED>'''

    # Create and write to the .dtd
    with open('catalog.dtd', 'w') as f:
        f.write(dtd_string)
    
    print('The catalog has been created.\n')