import os

def main():
    print('Welcome to the Scrape Worten Application.\nThis application has two halves:\
\n\tThe first one revolves around creating a catalog of products scraped through \
queries to worten.pt;\
\n\tThe second half revolves around creating a daily sales report with \
randomised data.')
    print('To use this interface, please follow the instructions on the screen, \
the rest will be handled for you.')
    print('These are the options available. To use one simply enter the number \
of the option:')
    run = True

    # Boolean values about whether or not options 1 and 4 have been used
    option1 = False
    option4 = False

    while run:
        print('''\t1- Create the Catalog .xml file;
    \t2- Create the Catalog web page (only available after using option 1);
    \t3- Create the Catalog .xml file and its web page;
    \t4- Create the Daily Sales .xml file;
    \t5- Create the Daily Sales web page (only available after using option 4);
    \t6- Create the Daily Sales .xml file and its web page;
    \t7- Create both .xml files and its web pages;
    \t8- Exit the progam;''')
        option = input('\n Enter the number of the option you wish to use: ')
        print()

        if option == '1':
            os.system('python catalog.py')
            print('Option 1 has finished running.\n')
            option1 = True

        elif option == '2':
            if option1:
                os.system('python gen_catalog_HTML_CSS.py')
                print('Option 2 has finished running.\n')
            else:
                print('You can only use option 2 after using option 1.\n')

        elif option == '3':
            os.system('python gen_catalog_XML_to_HTMLandCSS.py')
            print('Option 3 has finished running.\n')

        elif option == '4':
            os.system('python daily_sales.py')
            print('Option 4 has finished running.\n')
            option4 = True

        elif option == '5':
            if option4:
                os.system('python gen_sales_HTML_CSS.py')
                print('Option 5 has finished running.\n')
            else:
                print('You can only use option 5 after using option 4.\n')

        elif option == '6':
            os.system('python gen_sales_XML_to_HTMLandCSS.py')
            print('Option 6 has finished running.\n')

        elif option == '7':
            os.system('python gen_catalog_XML_to_HTMLandCSS.py')
            os.system('python gen_sales_XML_to_HTMLandCSS.py')                    
            print('Option 7 has finished running.\n')

        elif option == '8':
            print('The program has been terminated.')
            run = False
        
        else:
            print('Please choose a valid option.\n')


if __name__ == '__main__':
    main()