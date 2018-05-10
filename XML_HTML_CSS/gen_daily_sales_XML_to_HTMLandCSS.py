import os, time, webbrowser

start = time.time()
os.system('python daily_sales.py')
print()
print()
os.system('python gen_sales_HTML_CSS.py')

print()
print('The created web page will be opened in your default browser.')
print('The script is now finished.')
print('Elapsed time:', round(time.time()-start, 2), 'seconds.')
webbrowser.open('daily_sales.html')