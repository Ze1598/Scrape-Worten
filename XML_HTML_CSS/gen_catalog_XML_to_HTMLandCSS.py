import os, time, webbrowser

if __name__ == '__main__':
    # start = time.time()
    os.system('python catalog.py')
    os.system('python gen_catalog_HTML_CSS.py')

    print()
    # print('Elapsed time:', round(time.time()-start, 2), 'seconds.')
    print('Both the Catalog and its web page have been created.')
    # print('The created web page will be opened in your default browser.\n')
    # webbrowser.open('catalog.html')