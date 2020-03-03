import sys
import fileinput
import os
import io

file = (os.getenv('APP_INDEX_HTML_TEMPLATE_DIRECTORY') or  'templates/index.html')

filedata = None
with io.open(file, mode="r", encoding="utf-8") as f:
	filedata = f.read()

filedata = "{% load static %}\n" + filedata
filedata = filedata.replace('content=' + (os.getenv('DJANGO_STATIC_URL') or  '/static-vuedj/'), "content=\"{% static '")
filedata = filedata.replace('href=' + (os.getenv('DJANGO_STATIC_URL') or  '/static-vuedj/'), "href=\"{% static '")
filedata = filedata.replace('href=\"' + (os.getenv('DJANGO_STATIC_URL') or  '/static-vuedj/'), "href=\"{% static '")
filedata = filedata.replace('href=/static/', "href=\"{% static '")
filedata = filedata.replace('.css ', ".css' %}\"")
filedata = filedata.replace('.css>', ".css' %}\">")
filedata = filedata.replace('.css\"', ".css' %}\"")
filedata = filedata.replace('src=' + (os.getenv('DJANGO_STATIC_URL') or  '/static-vuedj/'), "src=\"{% static '")
filedata = filedata.replace('src=\"' + (os.getenv('DJANGO_STATIC_URL') or  '/static-vuedj/'), "src=\"{% static '")
filedata = filedata.replace('src=/static/', "src=\"{% static '")
filedata = filedata.replace('.js ', ".js' %}\"")
filedata = filedata.replace('.js>', ".js' %}\">")
filedata = filedata.replace('.js\"', ".js' %}\"")
filedata = filedata.replace('.png>', ".png' %}\">")
filedata = filedata.replace('.ico>', ".ico' %}\">")
filedata = filedata.replace('.json>', ".json' %}\">")
filedata = filedata.replace('.xml>', ".xml' %}\">")


with io.open(file, mode="w", encoding="utf-8") as f:
	f.write(filedata)
