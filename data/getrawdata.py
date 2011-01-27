import urllib2

urlcount = 0
for line in open('service.urls'):
    if line[0] != '#':
        urlcount += 1
        doc = urllib2.urlopen(line).read()
        out = open('out%d.html' % (urlcount), 'w')
        out.write(doc)
        out.close()
