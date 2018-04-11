'''Make queries to worten.pt and scrape the first product result.
Scrape information about that product and its page, then save
the information to an .xml file.
The XML structure is written in english, but the scraped 
information itself is written in portuguese, since it is scraped 
from a portuguese website.'''

# http://docs.python-requests.org/en/master/
from requests import post, get
# https://beautiful-soup-4.readthedocs.io/en/latest/
from bs4 import BeautifulSoup
from time import time
from os import startfile
from random import randint

def scrape(args):

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
        # the Response object with latin 1
        soup = BeautifulSoup(query.content, 'lxml', from_encoding="latin 1")

        # Product page for the first result of the query
        prod_link = target + soup.find('div', class_='w-product__wrapper').a["href"]
        # Text version of the product's page source code
        product_page = get(prod_link)
        # Create a new BeautifulSoup object for the product's page, encoding the raw data from\
        # the Response object with latin 1
        soup = BeautifulSoup(product_page.content, 'lxml', from_encoding="latin 1")
    
    # If something does go wrong, the function ends here by returning None
    except:
        return None

    # Product detailed info (this section of the source code will be worked on ahead)
    more_info = soup.find('div', class_='w-product-details__wrapper').div

    # Product availability
    try:
        # This actually doesn't work for products not available, but at the time of writing I\
        # couldn't find products out of stock to look at its HTML (which I assume will be\
        # differente, hence they try/except clause)
        prod_avail = soup.find('button', class_='w-btn-store-locator__available').div.text.strip()
    except:
        prod_avail = 'Indisponível'
    
    # Product name
    prod_name = more_info.header.h2.find('span', class_='w-section__product').text.strip()

    # Product category (a single <ul> contains one or more <li> tags, each containing <a> tags\
    # that contain the text we want, the categories)
    prod_cat = soup.find('ul', class_='w-breadcrumbs breadcrumbs').find_all('li')[-1].a.text.strip()

    # Product current price (if it's on sale, scrapes the discounted price)
    prod_price = '€' + soup.find('span', class_='w-product__price__current')['content']

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
                prod_dimensions += li.find('span', class_='details-value').text.strip() + ' cm'

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
    prod_stock = 0 if prod_avail == 'Indisponível' else randint(1, 100)

    # print()
    # print('Title of the product found:', prod_name)
    # print('Link to the product\'s page:', prod_link)
    # print('Product category:', prod_cat)
    # print('Product price:', prod_price)
    # print('Product availability:', prod_avail)
    # print('Links for available pictures:', pictures)
    # print('Product internal reference number:', prod_ref)
    # print('Product description:', prod_desc)
    # print('Product brand:', prod_brand)
    # print('Product weight:', prod_weight)
    # print('Product dimensions:', prod_dimensions)
    # print('Product color:', prod_color)
    # print('Product stock:', prod_stock)

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

    # Return a list with 2 elements: the formatted text string\
    # that will be saved to the .txt file and the formatted
    # XML string that will be saved to the .xml file
    return [txt_text, xml_text]



# arg = 'nintendo switch'
arg = 'asus'
# scrape(arg)

# The beginning of the .xml, with the header, .dtd location and root element
xml_string = '''<?xml version="1.0" encoding="iso-8859-10" ?>
<!DOCTYPE catalog SYSTEM "catalog.dtd">
<catalog store="Worten">'''

# '''
if __name__ == "__main__":
    # Counter to keep track of how many times the main function\
    # returned prematurely
    error_count = 0
    with open('scraped_products.txt', 'w') as f:
        while arg:
            # Time how long it takes to run each iteration of the loop
            start = time()
            # Ask the user for the tags to be searched for
            arg = input('Enter tags for the query: ')
            # If the user entered a valid input (if not the\
            # loop will be terminated in the next iteration)
            if arg:
                scrape_results = scrape(arg)
                # If the function was executed without\
                # raising exceptions, then write the returned info\
                # to a .txt file and organize the XML-string to be\
                # written to an .xml file
                if scrape_results:
                    f.write(scrape_results[0])
                    xml_string += scrape_results[1]
                    print()
                    print('Elapsed time:', round(time()-start, 2), 'seconds.')
                # If it raised exceptions (specifically in the GET requests,\
                # move on to the next iteration of the loop a.k.a. ask for new\
                # input)
                else:
                    print('Oops, something went wrong. Please try again')
                    error_count += 1
                    # If the main function returned prematurely three times
                    if error_count == 3:
                        print('It\s the third time the script can\'t retrieve information properly.')
                        # Assign 'arg' to be an empty string so that the loop will terminate
                        arg = ''
        else:
            xml_string += '\n</catalog>'
            print('The script has finished.')

    # Write the formatted string with XML to the .xml file
    with open('catalog.xml', 'w') as f:
        f.write(xml_string)
    
    # Before terminating the file, open the .txt file that was written to
    startfile('scraped_products.txt')
# '''