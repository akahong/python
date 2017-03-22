# python的httplib、urllib和urllib2的区别及用

## urllib和urllib2

urllib 和urllib2都是接受URL请求的相关模块，但是urllib2可以接受一个Request类的实例来设置URL请求的headers，urllib仅可以接受URL。

这意味着，你不可以伪装你的User Agent字符串等。

urllib提供urlencode方法用来GET查询字符串的产生，而urllib2没有。这是为何urllib常和urllib2一起使用的原因。

目前的大部分http请求都是通过urllib2来访问的

## httplib

httplib实现了HTTP和HTTPS的客户端协议，一般不直接使用，在python更高层的封装模块中（urllib,urllib2）使用了它的http实现。


## urllib简单用法

#encoding:utf-8
import urllib

url='http://mobile.jingwei.com/push/register'
reponse=urllib.urlopen(url)
print '>>>>>>>>>header>>>>>'
print reponse.info()
print '>>>>>>getcode>>'
print reponse.getcode()
print '>>>>url>>>'
print reponse.geturl()
print '>>>>>>>>>>>>>'
for line in reponse:
      print line
reponse.close() 

urllib.urlopen(url[, data[, proxies]]) :

创建一个表示远程url的类文件对象，然后像本地文件一样操作这个类文件对象来获取远程数据。参数url表示远程数据的路径，一般是网址；
参数data表示以post方式提交到url的数据；
参数proxies用于设置代理。urlopen返回一个类文件对象，他提供了如下方法：

read(),readline(),readlines(), fileno(), close()：这些方法的使用方式与文件对象完全一样;
info()：返回一个httplib.HTTPMessage对象，表示远程服务器返回的头信息；
getcode()：返回Http状态码。如果是http请求，200表示请求成功完成;404表示网址未找到；
geturl()：返回请求的url；


urllib.urlretrieve(url[, filename[, reporthook[, data]]])：

urlretrieve方法直接将远程数据下载到本地。参数filename指定了保存到本地的路径（如果未指定该参数，urllib会生成一个临时文件来保存数据）；
参数reporthook是一个回调函数，当连接上服务器、以及相应的数据块传输完毕的时候会触发该回调。
我们可以利用这个回调函 数来显示当前的下载进度。参数data指post到服务器的数据。
该方法返回一个包含两个元素的元组(filename, headers)，filename表示保存到本地的路径，header表示服务器的响应头。

def cbk(a, b, c):    
    '''''''回调函数  
    @a: 已经下载的数据块  
    @b: 数据块的大小  
    @c: 远程文件的大小  
    '''    
    per = 100.0 * a * b / c    
    if per > 100:    
        per = 100    
    print '%.2f%%' % per    
    
url = 'http://www.sina.com.cn'    
local = 'd://sina.html'    
urllib.urlretrieve(url, local, cbk)    


urllib中还提供了一些辅助方法，用于对url进行编码、解码。url中是不能出现一些特殊的符号的，有些符号有特殊的用途。
我们知道以get方式提交数据的时候，会在url中添加key=value这样的字符串，所以在value中是不允许有'='，因此要对其进行编码；
与此同时服务器接收到这些参数的时候，要进行解码，还原成原始的数据。这个时候，这些辅助方法会很有用：

urllib.quote(string[, safe])：对字符串进行编码。参数safe指定了不需要编码的字符;
urllib.unquote(string) ：对字符串进行解码；
urllib.quote_plus(string[,safe]) ：与urllib.quote类似，但这个方法用'+'来替换' '，而quote用'%20'来代替' '
urllib.unquote_plus(string) ：对字符串进行解码；
urllib.urlencode(query[, doseq])：将dict或者包含两个元素的元组列表转换成url参数。例如 字典{'name': 'dark-bull', 'age': 200}将被转换为"name=dark-bull&age=200"
urllib.pathname2url(path)：将本地路径转换成url路径；
urllib.url2pathname(path)：将url路径转换成本地路径；

例：
data = 'name = ~a+3'    
    
data1 = urllib.quote(data)    
print data1 # result: name%20%3D%20%7Ea%2B3    
print urllib.unquote(data1) # result: name = ~a+3    
    
data2 = urllib.quote_plus(data)    
print data2 # result: name+%3D+%7Ea%2B3    
print urllib.unquote_plus(data2)    # result: name = ~a+3    
    
data3 = urllib.urlencode({ 'name': 'dark-bull', 'age': 200 })    
print data3 # result: age=200&name=dark-bull    
    
data4 = urllib.pathname2url(r'd:/a/b/c/23.php')    
print data4 # result: ///D|/a/b/c/23.php    
print urllib.url2pathname(data4)    # result: D:/a/b/c/23.php  


##urllib2简单用法

import urllib2  
response=urllib2.urlopen('http://www.douban.com')  
html=response.read()   

实际步骤：
1、urllib2.Request()的功能是构造一个请求信息，返回的req就是一个构造好的请求

2、urllib2.urlopen()的功能是发送刚刚构造好的请求req，并返回一个文件类的对象response，包括了所有的返回信息。

3、通过response.read()可以读取到response里面的html，通过response.info()可以读到一些额外的信息。

如：
#!/usr/bin/env python  
    import urllib2  
    req = urllib2.Request("http://www.douban.com")  
    response = urllib2.urlopen(req)  
    html = response.read()  
    print html  

有时你会碰到，程序也对，但是服务器拒绝你的访问。这是为什么呢?问题出在请求中的头信息(header)。 有的服务端有洁癖，不喜欢程序来触摸它。
这个时候你需要将你的程序伪装成浏览器来发出请求。请求的方式就包含在header中。
常见的情形：

import urllib  
import urllib2  
url = 'http://www.someserver.com/cgi-bin/register.cgi'  
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'# 将user_agent写入头信息  
values = {'name' : 'who','password':'123456'}  
headers = { 'User-Agent' : user_agent }  
data = urllib.urlencode(values)  
req = urllib2.Request(url, data, headers)  
response = urllib2.urlopen(req)  
the_page = response.read()  


GET方法

#coding:utf-8  
import urllib   
import urllib2    
url = 'http://www.baidu.com/s'   
values = {'wd':'D_in'}     
data = urllib.urlencode(values)  
print data   
url2 = url+'?'+data  
response = urllib2.urlopen(url2)    
the_page = response.read()   
print the_page 

POST方法

import urllib  
import urllib2  
url = 'http://www.someserver.com/cgi-bin/register.cgi'  
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' //将user_agent写入头信息  
values = {'name' : 'who','password':'123456'}      //post数据  
headers = { 'User-Agent' : user_agent }  
data = urllib.urlencode(values)                   //对post数据进行url编码  
req = urllib2.Request(url, data, headers)  
response = urllib2.urlopen(req)  
the_page = response.read()  


urllib2带cookie的使用

#coding:utf-8  
import urllib2,urllib  
import cookielib  
   
url = r'http://www.renren.com/ajaxLogin'  
   
#创建一个cj的cookie的容器  
cj = cookielib.CookieJar()  
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))  
#将要POST出去的数据进行编码  
data = urllib.urlencode({"email":email,"password":pass})  
r = opener.open(url,data)  
print cj  

httplib简单用法

#!/usr/bin/env python      
# -*- coding: utf-8 -*-      
import httplib    
import urllib    
    
def sendhttp():    
    data = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})       
    headers = {"Content-type": "application/x-www-form-urlencoded",    
               "Accept": "text/plain"}    
    conn = httplib.HTTPConnection('bugs.python.org')    
    conn.request('POST', '/', data, headers)    
    httpres = conn.getresponse()    
    print httpres.status    
    print httpres.reason    
    print httpres.read()               
                  
if __name__ == '__main__':      
    sendhttp()  
    
＃ 访问https：
urllib来说有两种方式，一种是urllib.urlopen()有一个参数context,把他设成ssl._create_unverified_context
或者修改现在的全局默认值
_create_unverified_https_context
或
ssl._create_default_https_context
为
ssl._create_unverified_context

那么requests呢，难道必须设置全局变量吗。
request的post和get都有一个叫verify的参数，把他设成False就可以了。
