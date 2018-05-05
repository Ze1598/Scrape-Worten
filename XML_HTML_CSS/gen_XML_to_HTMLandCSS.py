import os, time, webbrowser

start = time.time()
os.system('python catalog.py')
print()
print()
os.system('python generate_HTML_CSS.py')

print()
print('The created web page will be opened in your default browser.')
print('The script is now finished.')
print('Elapsed time:', round(time.time()-start, 2))
webbrowser.open('catalog.html')