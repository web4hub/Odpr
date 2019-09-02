import sys
import fileinput
import os

file = (os.getenv('APP_INDEX_HTML_TEMPLATE_DIRECTORY') or  'templates/index.html')

# with open(file, "r+") as f:
#     s = f.read()
#     f.seek(0)
#     f.write("{% load staticfiles %}\n" + s)
#
# for i, line in enumerate(fileinput.input(file, inplace=1)):
#     sys.stdout.write(line.replace('/static-vuedj/', "{% static '"))
# for i, line in enumerate(fileinput.input(file, inplace=1)):
#     sys.stdout.write(line.replace('.css', ".css' %}"))
# for i, line in enumerate(fileinput.input(file, inplace=1)):
#     sys.stdout.write(line.replace('.js', ".js' %}"))

with open(file, "r+") as f:
	s = f.read()
	f.seek(0)
	f.write("{% load static %}\n" + s)

for i, line in enumerate(fileinput.input(file, inplace=1)):
	sys.stdout.write(line.replace('href=' + (os.getenv('DJANGO_STATIC_URL') or  '/static-vuedj/'), "href=\"{% static '"))
for i, line in enumerate(fileinput.input(file, inplace=1)):
	sys.stdout.write(line.replace('href=\"' + (os.getenv('DJANGO_STATIC_URL') or  '/static-vuedj/'), "href=\"{% static '"))
for i, line in enumerate(fileinput.input(file, inplace=1)):
	sys.stdout.write(line.replace('href=/static/', "href=\"{% static '"))
for i, line in enumerate(fileinput.input(file, inplace=1)):
	sys.stdout.write(line.replace('.css ', ".css' %}\""))
for i, line in enumerate(fileinput.input(file, inplace=1)):
	sys.stdout.write(line.replace('.css>', ".css' %}\">"))
for i, line in enumerate(fileinput.input(file, inplace=1)):
	sys.stdout.write(line.replace('.css\"', ".css' %}\""))
for i, line in enumerate(fileinput.input(file, inplace=1)):
	sys.stdout.write(line.replace('src=' + (os.getenv('DJANGO_STATIC_URL') or  '/static-vuedj/'), "src=\"{% static '"))
for i, line in enumerate(fileinput.input(file, inplace=1)):
	sys.stdout.write(line.replace('src=\"' + (os.getenv('DJANGO_STATIC_URL') or  '/static-vuedj/'), "src=\"{% static '"))
for i, line in enumerate(fileinput.input(file, inplace=1)):
	sys.stdout.write(line.replace('src=/static/', "src=\"{% static '"))
for i, line in enumerate(fileinput.input(file, inplace=1)):
	sys.stdout.write(line.replace('.js ', ".js' %}\""))
for i, line in enumerate(fileinput.input(file, inplace=1)):
	sys.stdout.write(line.replace('.js>', ".js' %}\">"))
for i, line in enumerate(fileinput.input(file, inplace=1)):
	sys.stdout.write(line.replace('.js\"', ".js' %}\""))
