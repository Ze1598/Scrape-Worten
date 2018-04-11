# Scrape-Worten

A project that revolves around scraping information from worten.pt, saving it to an .xml file and then display that information using HTML and CSS.

The first half of the project consists in scraping the information about products that result from a query to worten.pt, then saving that information to an .xml file, which is validated by the corresponding .dtd file.

For the second half, I pretend to present the information in the .xml file graphically, using HTML and CSS.

So far, the repo contains a folder with the necessary Python, XML and DTD files for the first half of the project. Note the XML files are example files, though the DTD ones are final since all of the created XML files will have to be validated by the same DTD file.
The "XML_DTD/catalog" files are about the mini-catalog created with the scraped products' informations.
The "XML_DTD/daily_sales" are about the informations pertaining the daily sales of the online store. All the information on those files is randomly generated from sample_citizen_data.txt file and thus fake.

In the future, I'd like to create a Python package focused on the content of the first half, that is, a Python script to make queries to worten.pt and scrape information about the products. 
In a way, I'd like for it to be an rudimentary API of sorts to scrape information about products, based on user-queries. At the moment, I am planning to return that scraped information in JSON and XML, letting the user choose which format to be returned.

Update log:

-(apr. 11th 2018) Created the repository, with all the necessary files for the first half of the project a.k.a. the XML and DTD half.


External references:

-Target website: https://www.worten.pt/

-Beautiful Soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

-Requests: http://docs.python-requests.org/en/master/
