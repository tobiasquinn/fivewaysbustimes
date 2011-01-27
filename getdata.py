#!/usr/bin/python

# Screen scrape from buses.citytransport.org.uk to get bus times from
# Fiveways in the Brighton  Centre direction

# (c) Tobias Quinn, 2011 <tobias@tobiasquinn.com>, GPLv3
# LiCENSE: GPLv3 - http://www.gnu.org/licenses/gpl.html

import urllib2
from datetime import timedelta, datetime
from BeautifulSoup import BeautifulSoup

class BusData:
    def __init__(self, URLFILE=None):
        # read data file urls
        # Read live data
        if URLFILE != None:
            self._urls = []
            for line in open(URLFILE).readlines():
                if line[0] != '#':
                    self._urls.append(line.strip())
        else:
        # Test data
            self._urls = [
                    'file:data/set1/out1.html',
                    'file:data/set1/out2.html',
                    'file:data/set1/out3.html',
                    'file:data/set1/out4.html',
                    'file:data/set1/out5.html',
                    ]

    def getData(self):
        # get and scrape all the data into a list
        times = []
        for url in self._urls[:]:
            doc = urllib2.urlopen(url).read()
            soup = BeautifulSoup(doc, convertEntities=BeautifulSoup.HTML_ENTITIES)
            dtimes = (soup.findAll('span', attrs = 'dfifahrten'))
            # we want to iterate over the returned data 3 at a time
            # as it is supplied in the for busnum, destination, time
            for i in range(0, len(dtimes), 3):
                busnum = dtimes[i].string
                destination = dtimes[i+1].string
                arrive = dtimes[i+2].string
                if arrive == None:
                    continue
                # the time can have various formats
                # - calculated minutes to arrival
                # - calculated time of arrival
                # - timetabled time of arrival
                # For now, lets convert the time to an absolute time
                # the times decrease to zero then disappear
                if arrive.find(':') == -1:
                    timenow = datetime.now()
                    # cut out anything pass the first space (encoded in html)
                    td = timedelta(minutes = int(arrive[:2]))
                    arrive = (timenow + td)
                else:
                    # strip any following * which means calculated time when non offset
                    arrive = arrive.replace('*', '')
                    arrive = datetime.strptime(arrive, "%H:%M")
                times.append((busnum, destination, arrive))
                print "%s,%s,%s" % (busnum, destination, arrive)
        # sort the list by times
        data = sorted(times, key=lambda arrive: arrive[2])
        print data
        return data

if __name__ == '__main__':
    bd = BusData('service.urls')
    bd._getdata()
