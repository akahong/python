#encoding:utf-8
import urllib
import urllib2
import ssl

url='https://mobile.jingwei.com/push/register'
ssl._create_default_https_context = ssl._create_unverified_context
reponse=urllib2.urlopen(url)
print '>>>>>>>>>header>>>>>'
print reponse.info()
print '>>>>>>getcode>>'
print reponse.getcode()
print '>>>>url>>>'
print reponse.geturl()
print '>>>>>>>>>>>>>'
for line in reponse:
      print line

