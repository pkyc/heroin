
import urllib2
import re
import string
from bs4 import BeautifulSoup

link = 'http://www.hkjc.com/english/racing/selecthorsebychar.asp?ordertype=A'
#atoz = list(string.uppercase)
atoz = ['A']
allhor = ([])


def hor(all):
    for a in all:
        link = 'http://www.hkjc.com/english/racing/' + a[0].encode("utf-8")
        name = a[1].encode("utf-8")
        print(link,name)
    return


for a in atoz:
    link = 'http://www.hkjc.com/english/racing/selecthorsebychar.asp?ordertype='+a
    htmlfile = urllib2.urlopen(link)
    htmltext = htmlfile.read()
    soup = BeautifulSoup(htmltext,'html.parser')
    for each in  soup.find_all(href=re.compile("^horse.asp")):
        allhor.append([each.get('href'),each.contents[0]])

hor(allhor)

