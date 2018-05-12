# Scrape-Worten

A project that revolves around scraping information from worten.pt, saving it to an .xml file and then create .html and .css files to display that information using HTML and CSS.

The first half of the project consists in scraping the information about products that result from a query to worten.pt, then saving that information to an .xml file, which is validated by the corresponding .dtd file.

For the second half, I present the information in the .xml file graphically, using HTML and CSS.

The "XML_HTML_CSS/catalog" files are about the mini-catalog created with the scraped products' informations.
The "XML_HTML_CSS/daily_sales" files are about the informations pertaining the daily sales of the online store. All the information on those files is randomly generated from "sample_citizen_data.txt" file and thus fake.
The "XML_HTML_CSS/manual_" .html and .css files were the files I wrote manually at first to know what I wanted the end result to look like. From that point, I worked on automating the creation of those files, which resulted in "XML_HTML_CSS/generate_HTML_CSS.py". This file reads the contents of "catalog.xml" and generates an .html and a .css file to display its contents in a web browser.
"XML_HTML_CSS/gen_XML_to_HTMLandCSS.py" is a file intended (like the other Python files) to be ran in the command line. Running this script simply runs the other two Python scripts, "XML_HTML_CSS/catalog.py" to scrape products from worten.pt and "XML_HTML_CSS/generate_HTML_CSS.py" to generate the HTML and CSS.

TL;DR: to scrape the products you want and display its informations in a web browser, simply run "XML_HTML_CSS/gen_XML_to_HTMLandCSS.py" in the command line. Simply follow the instructions on the screen and the result will open automatically at the end.

Here's a sample of the end result for the Catalog (recorded with Gyazo GIF): https://i.gyazo.com/0249feacda2da2c481f3cbdb7c97d81f.mp4 .
And here's a sample of the end result for the Daily Sales (recorded with Gyazo GiF): https://i.gyazo.com/fbda911e1e6a45a30f84b4530643b0cd.mp4 .

Update log:

-(apr. 11th 2018) Created the repository, with all the necessary files for the first half of the project a.k.a. the XML and DTD half.

-(may 5th 2018) Updated the repository, with the .html and .css files, along with a .python script to create those files from the generated .xml file; Also updated the structure of the repository (everything is in a single folder).

-(may 10th 2018) Updated the repository with the same content I added previously for the Catalog file, except this time the files are relative to the Daily Sales file.


External references:

-Target website: https://www.worten.pt/

-Beautiful Soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

-Requests: http://docs.python-requests.org/en/master/
