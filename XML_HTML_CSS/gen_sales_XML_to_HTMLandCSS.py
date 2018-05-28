import os, time, webbrowser

if __name__ == '__main__':
    # start = time.time()
    os.system('python daily_sales.py')
    os.system('python gen_sales_HTML_CSS.py')

    print()
    # print('Elapsed time:', round(time.time()-start, 2), 'seconds.')
    print('Both the Daily Sales and its web page have been created.')
    # print('The created web page will be opened in your default browser.\n')
    # webbrowser.open('daily_sales.html')