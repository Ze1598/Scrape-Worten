# Scrape-Worten

A project that revolves around scraping information from worten.pt, saving it to an .xml file and then create .html and .css files to display that information using HTML and CSS.

The first half of the project consists in scraping the information about products that result from a query to worten.pt, then saving that information to an .xml file, which is validated by the corresponding .dtd file.

For the second half, I present the information in the .xml file graphically, using HTML and CSS, for both the catalog and the daily sales.

The "XML_HTML_CSS/catalog" files are about the mini-catalog created with the scraped products' informations.
The "XML_HTML_CSS/daily_sales" files are about the informations pertaining the daily sales of the online store. All the information on those files is randomly generated from "sample_citizen_data.txt" file and thus fake.
The "XML_HTML_CSS/manual_" .html and .css files were the files I wrote manually at first to know what I wanted the end result to look like. From that point, I worked on automating the creation of those files, which resulted in the "XML_HTML_CSS/gen" python scripts.

TL;DR: to scrape the products you want and display its informations in a web browser, simply run "XML_HTML_CSS/app_interface.py" in the command line. Simply follow the instructions on the screen and the result will open automatically at the end.

Here's a sample of the end result for the Catalog (recorded with Gyazo GIF): https://gyazo.com/b50f6d8ab3b7982fd35d9cab9e41051a.
And here's a sample of the end result for the Daily Sales (recorded with Gyazo GiF): https://gyazo.com/1a144fb147c0899357f5ec1dc1b15603.

You can also use this application online in repl.it, albeit with some slight changes for it to work with the platform: https://repl.it/@ze1598/Scrape-Worten-Application. Please due note the .html, .css, .xml and .dtd files are only written to once the application terminates.


Update log:

-(apr. 11th 2018) Created the repository, with all the necessary files for the first half of the project a.k.a. the XML and DTD half.

-(may 5th 2018) Updated the repository, with the .html and .css files, along with a .python script to create those files from the generated .xml file; Also updated the structure of the repository (everything is in a single folder).

-(may 10th 2018) Updated the repository with the same content I added previously for the Catalog file, except this time the files are relative to the Daily Sales file.

-(may 12th 2018) Updated the files to have a more normalized in file naming but also in file structure. I have also added "XML_HTML_CSS/app_interface.py". You can use just the file because, has the name implies, it is an interface to use the application.


External references:

-Target website: https://www.worten.pt/

-Beautiful Soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

-Requests: http://docs.python-requests.org/en/master/

-Repl.it: https://repl.it/repls
