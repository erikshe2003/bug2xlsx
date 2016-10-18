# -*- coding: utf-8 -*-
__author__ = 'wufeng_wb'

from urllib import request
from urllib import parse
from http import cookiejar
from packages.myParsers import bugIdParser, bugListParser, bugCreateTimeParser, bugResolvedTimeParser, bugIdParser_requirement, bugListParser_requirement, bugReopenANDPendingParser_requirement, bugHistoryParser_requirement
import re, os, images


class bug2xlsx_request():
    def __init__(self):
        # 新增cookie对象，这个对象可以存储与使用cookie。该对象一般作为HTTPCookieProcessor对象的参数
        self.cookies = cookiejar.CookieJar()
        # 创建对象cookie对象的处理器
        self.cookie_processor = request.HTTPCookieProcessor(self.cookies)
        self.bugHistoryDict = {}

    def login_getLogCookie(self):
        # 准备请求中的headers，以下内容非必需
        headers = [
            ('Content-Type', 'application/x-www-form-urlencoded'),
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.47 Safari/537.36'),
            ('Accept-Encoding', 'gzip, deflate'),
            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
            ('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')]
        url = "http://bugzilla.qiyi.domain/index.cgi"
        # 新增cookie对象，这个对象可以存储与使用cookie。该对象一般作为HTTPCookieProcessor对象的参数
        cookies = cookiejar.CookieJar()
        # 创建对象cookie对象的处理器
        cookie_processor = request.HTTPCookieProcessor(cookies)
        # 由于基本的urlopen()函数不支持验证、cookie或其他HTTP高级功能，所以要支持这些功能，必须使用build_opener()函数来创建自己的自定义Opener对象
        # build_opener自定义opener（即request请求）,在opener中绑定CookieJar对象的处理器，从而生成一个新的opener，这个opener包含了一个cookie处理器，随时记录cookie
        getLogCookie = request.build_opener(cookie_processor)
        # 往opener中添加headers
        getLogCookie.addheaders = headers
        getLogCookie.open(url)
        for i in cookies:
            self.Bugzilla_login_request_cookie = i.value
            # print(self.Bugzilla_login_request_cookie)

    def login_getCookie(self):
        # self.login_getLogCookie()
        username = ''
        passwd = ''
        config = open('config.txt', mode='r', encoding='utf-8')
        for i in config.readlines():
            if i[0] == '#':
                pass
            else:
                if i.startswith('username=') == True:
                    try:
                        username = re.match('username=(.+)', i).group(1)
                    except Exception as e:
                        pass
                if i.startswith('passwd=') == True:
                    try:
                        passwd = re.match('passwd=(.+)', i).group(1)
                    except Exception as e:
                        pass
        config.close()
        if username == '' or passwd == '':
            return 2
        else:
            headers = [
                ('Referer', 'http://bugzilla.qiyi.domain/index.cgi?logout=1')]
            post_data = parse.urlencode({"Bugzilla_login": username,
                                         "Bugzilla_password": passwd,
                                         "Bugzilla_login_token": "",
                                         "GoAheadAndLogIn": "Log in"}).encode("UTF-8")
            url = "http://bugzilla.qiyi.domain/index.cgi"
            getCookie = request.build_opener(self.cookie_processor)
            getCookie.addheaders = headers
            getCookie.open(url, post_data)
            # print(self.cookies._cookies.values()[0]['/'].has_key('Bugzilla_logincookie'))
            for i in self.cookies._cookies.values():
                if 'Bugzilla_logincookie' in i['/']:
                    return 0
                else:
                    return 1

    def return_idList(self, id):
        # 准备请求中的headers，以下内容非必需
        headers = [
            ('Content-Type', 'application/x-www-form-urlencoded'),
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.47 Safari/537.36'),
            ('Accept-Encoding', 'gzip, deflate'),
            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
            ('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')]
        idReq = request.build_opener(self.cookie_processor)
        idReq.addheaders = headers
        # build_opener对象具有open方法，基本等同于urlopen
        # read方法读取open后返回的内容
        url = "http://bugzilla.qiyi.domain/show_bug.cgi?id=" + id
        try:
            idRes = idReq.open(url)
        except Exception as e:
            return 1
        idListParser = bugIdParser()
        idListParser.feed(idRes.read().decode("UTF-8"))
        idListStr = idListParser.show()
        idListStrReplace = idListStr.replace(', ', '')
        singleId = ''
        idList = []
        n = 1
        for i in idListStrReplace:
            singleId = singleId + i
            n = n + 1
            if n == 7:
                idList.append(singleId)
                n = 1
                singleId = ''
        return idList
        # for i in idListParser.show():

    def getBugList(self, cidList):
        buglist = '%2C'.join(cidList)
        headers = [
            ('Origin', 'http://bugzilla.qiyi.domain'),
            ('Connection', 'keep-alive'),
            ('Upgrade-Insecure-Requests', '1'),
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.47 Safari/537.36'),
            ('Accept-Encoding', 'gzip, deflate'),
            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
            ('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')]
        bugListReq = request.build_opener(self.cookie_processor)
        bugListReq.addheaders = headers
        url = "http://bugzilla.qiyi.domain/buglist.cgi?bug_id=" + buglist + '&columnlist=bug_id%2Cshort_desc%2Cassigned_to%2Cpriority%2Cbug_status&list_id=988553&query_format=advanced'
        try:
            bugListRes = bugListReq.open(url)
        except Exception as e:
            return 1
        bugData = bugListParser()
        bugData.feed(bugListRes.read().decode("utf-8"))
        bugDataDict = bugData.show()
        return bugDataDict
        # print(bugDataStr)

    def getBugHistory(self, cid):
        headers = [
            ('Content-Type', 'application/x-www-form-urlencoded'),
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.47 Safari/537.36'),
            ('Accept-Encoding', 'gzip, deflate'),
            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
            ('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')]
        bugHistoryReq = request.build_opener(self.cookie_processor)
        bugHistoryReq.addheaders = headers
        # build_opener对象具有open方法，基本等同于urlopen
        # read方法读取open后返回的内容
        bugHtmlUrl = "http://bugzilla.qiyi.domain/show_bug.cgi?id=" + str(cid)
        bugHistoryHtmlUrl = "http://bugzilla.qiyi.domain/show_activity.cgi?id=" + str(cid)
        try:
            bugHtml = bugHistoryReq.open(bugHtmlUrl)
        except Exception as e:
            return 1
        getBugCreateTime = bugCreateTimeParser()
        getBugCreateTime.feed(bugHtml.read().decode("utf-8"))
        bugCreateTime = getBugCreateTime.show()
        try:
            bugHistoryHtml = bugHistoryReq.open(bugHistoryHtmlUrl)
        except Exception as e:
            return 1
        getBugResolvedTime = bugResolvedTimeParser()
        getBugResolvedTime.feed(bugHistoryHtml.read().decode("utf-8"))
        bugResolvedTime = getBugResolvedTime.show()
        bugCreateTime.update(bugResolvedTime)
        # try:
        #     bugHistoryHtml = bugHistoryReq.open(bugHistoryUrl)
        # except Exception as e:
        #     return 1
        # bugHistory =
        self.bugHistoryDict[str(cid)] = bugCreateTime

    def return_bugHistoryDictLens(self):
        return len(self.bugHistoryDict)

    def return_bugHistoryDict(self):
        return self.bugHistoryDict

class bug2xlsx_request_ChanDao():
    def __init__(self):
        # 新增cookie对象，这个对象可以存储与使用cookie。该对象一般作为HTTPCookieProcessor对象的参数
        self.cookies = cookiejar.CookieJar()
        # 创建对象cookie对象的处理器
        self.cookie_processor = request.HTTPCookieProcessor(self.cookies)
        self.bugHistoryDict = {}
        self.sid = ""

    def getSid(self):
        # 准备请求中的headers，以下内容非必需
        url = "http://pm.game.qiyi.domain/index.php"
        # 新增cookie对象，这个对象可以存储与使用cookie。该对象一般作为HTTPCookieProcessor对象的参数
        cookies = cookiejar.CookieJar()
        # 创建对象cookie对象的处理器
        cookie_processor = request.HTTPCookieProcessor(cookies)
        # 由于基本的urlopen()函数不支持验证、cookie或其他HTTP高级功能，所以要支持这些功能，必须使用build_opener()函数来创建自己的自定义Opener对象
        # build_opener自定义opener（即request请求）,在opener中绑定CookieJar对象的处理器，从而生成一个新的opener，这个opener包含了一个cookie处理器，随时记录cookie
        getSidReq = request.build_opener(cookie_processor)
        # 往opener中添加headers
        try:
            getSidReq.open(url)
        except Exception as e:
            return 1
        for i in cookies:
            if i.name == "sid":
                return i.value

    def setAuthentication(self):
        self.sid = self.getSid()
        if self.sid == 1 or self.sid == None:
            return 1
        else:
            cusername = ''
            cpasswd = ''
            config = open('config.txt', mode='r', encoding='utf-8')
            for i in config.readlines():
                if i[0] == '#':
                    pass
                else:
                    if i.startswith('cusername=') == True:
                        try:
                            cusername = re.match('cusername=(.+)', i).group(1)
                        except Exception as e:
                            pass
                    if i.startswith('cpasswd=') == True:
                        try:
                            cpasswd = re.match('cpasswd=(.+)', i).group(1)
                        except Exception as e:
                            pass
            config.close()
            if cusername == '' or cpasswd == '':
                return 2
            else:
                headers = [
                    ('Content-Type', 'application/x-www-form-urlencoded'),
                    ('Cookie', 'sid=' + self.sid),
                ]
                post_data = parse.urlencode({"account": cusername,
                                             "password": cpasswd,
                                             "referer": "/index.php"}).encode("UTF-8")
                url = "http://pm.game.qiyi.domain/index.php?m=user&f=login"
                setAuthenticationReq = request.build_opener()
                setAuthenticationReq.addheaders = headers
                try:
                    setAuthenticationReq.open(url, post_data)
                except Exception as e:
                    return 1
                # print(setAuthenticationRes.read().decode("utf-8"))

    def getQueryId(self, id, keyword, productID):
        # 准备请求中的headers，以下内容非必需
        headers = [
            ('Content-Type', 'application/x-www-form-urlencoded'),
            ('Cookie', 'sid=' + self.sid),
        ]
        post_data = parse.urlencode({"andOr1": "AND", "field1": str(keyword), "operator1": "=", "value1": id,
                                     "andOr2": "and", "field2": "story", "operator2": "=", "value2": "",
                                     "andOr3": "and", "field3": "title", "operator3": "include", "value3": "",
                                     "groupAndOr": "and",
                                     "andOr4": "AND", "field4": "id", "operator4": "=", "value4": "",
                                     "andOr5": "and", "field5": "keywords", "operator5": "include", "value5": "",
                                     "andOr6": "and", "field6": "steps", "operator6": "include", "value6": "",
                                     "module": "bug",
                                     "actionURL": "/index.php?m=bug&f=browse&productID=" + str(productID) + "&browseType=bySearch|1&queryID=myQueryID",
                                     "groupItems": "3",
                                     "queryID": "",
                                     "formType": "lite",
                                     }).encode("UTF-8")
        getQueryIdReq = request.build_opener()
        getQueryIdReq.addheaders = headers
        # build_opener对象具有open方法，基本等同于urlopen
        # read方法读取open后返回的内容
        url = "http://pm.game.qiyi.domain/index.php?m=search&f=buildQuery"
        try:
            getQueryIdReq.open(url, post_data)
        except Exception as e:
            return 1

    def return_idList(self, id, keyword, productID):
        getSuccess = self.getQueryId(id=id, keyword=keyword, productID=productID)
        if getSuccess == 1:
            return 1
        else:
            headers = [
                ('Content-Type', 'application/x-www-form-urlencoded'),
                ('Cookie', 'sid=' + self.sid + ';windowWidth=1423;windowHeight=777')
            ]
            idListReq = request.build_opener()
            idListReq.addheaders = headers
            url = "http://pm.game.qiyi.domain/index.php?m=bug&f=browse&t=html&productID=" + str(productID) + "&browseType=bySearch|2&param=myQueryID&orderBy=&recTotal=&recPerPage=1000&pageID=1"
            try:
                idListRes = idListReq.open(url)
            except Exception as e:
                return 1
            # print(bugListRes.read().decode("utf-8"))
            idListData = bugIdParser_requirement()
            idListData.feed(idListRes.read().decode("utf-8"))
            idList = idListData.show()
            return idList

    def return_bugList(self, id, keyword, productID):
        getSuccess = self.getQueryId(id=id, keyword=keyword, productID=productID)
        if getSuccess == 1:
            return 1
        else:
            headers = [
                ('Content-Type', 'application/x-www-form-urlencoded'),
                ('Cookie', 'sid=' + self.sid + ';windowWidth=1423;windowHeight=777')
            ]
            bugListReq = request.build_opener()
            bugListReq.addheaders = headers
            url = "http://pm.game.qiyi.domain/index.php?m=bug&f=browse&t=html&productID=" + str(productID) +"&browseType=bySearch|2&param=myQueryID&orderBy=&recTotal=&recPerPage=1000&pageID=1"
            try:
                bugListRes = bugListReq.open(url)
            except Exception as e:
                return 1
            # print(bugListRes.read().decode("utf-8"))
            bugListData = bugListParser_requirement()
            bugListData.feed(bugListRes.read().decode("utf-8"))
            bugListDataDict = bugListData.show()
            return bugListDataDict

    def return_reopenANDpending(self, idList):
        reopenNumber = 0
        pendingNumber = 0
        reopenANDpending = []
        headers = [
            ('Content-Type', 'application/x-www-form-urlencoded'),
            ('Cookie', 'sid=' + self.sid + ';windowWidth=1423;windowHeight=777')
        ]
        bugPageReq = request.build_opener()
        bugPageReq.addheaders = headers
        for id in idList:
            url = "http://pm.game.qiyi.domain/index.php?m=bug&f=view&bugID=" + id
            try:
                bugPageRes = bugPageReq.open(url)
            except Exception as e:
                return 1
            # print(bugListRes.read().decode("utf-8"))
            bugHistoryList = bugReopenANDPendingParser_requirement()
            bugHistoryList.feed(bugPageRes.read().decode("utf-8"))
            bugHistory = bugHistoryList.show()
            flag = ''
            for i in bugHistory:
                if i[0] == '创建':
                    flag = '创建'
                elif flag == '创建' and i[0] == '确认':
                    flag = '确认'
                elif flag == '确认' and i[0] == '解决' and i[1] != '延期处理':
                    flag = '解决'
                elif flag == '确认' and i[0] == '解决' and i[1] == '延期处理':
                    flag = '延期'
                elif flag == '创建' and i[0] == '解决' and i[1] != '延期处理':
                    flag = '解决'
                elif flag == '创建' and i[0] == '解决' and i[1] != '延期处理':
                    flag = '延期'
                elif flag == '解决' and i[0] == '激活':
                    flag = '重打开'
                elif flag == '重打开' and i[0] == '解决' and i[1] != '延期处理':
                    flag = '解决'
                elif flag == '重打开' and i[0] == '解决' and i[1] == '延期处理':
                    flag = '延期'
            if flag == '重打开':
                reopenNumber += 1
            elif flag == '延期':
                pendingNumber += 1
        reopenANDpending.append(reopenNumber)
        reopenANDpending.append(pendingNumber)
        # print(bugHistory)
        return reopenANDpending

    def getBugHistory(self, id):
        headers = [
            ('Content-Type', 'application/x-www-form-urlencoded'),
            ('Cookie', 'sid=' + self.sid + ';windowWidth=1423;windowHeight=777')
        ]
        bugHistoryReq = request.build_opener()
        bugHistoryReq.addheaders = headers
        # build_opener对象具有open方法，基本等同于urlopen
        # read方法读取open后返回的内容
        bugHtmlUrl = "http://pm.game.qiyi.domain/index.php?m=bug&f=view&bugID=" + id
        try:
            bugHistoryRes = bugHistoryReq.open(bugHtmlUrl)
        except Exception as e:
            return 1
        getBugHistory = bugHistoryParser_requirement()
        getBugHistory.feed(bugHistoryRes.read().decode("utf-8"))
        bugHistory = getBugHistory.show()
        # try:
        #     bugHistoryHtml = bugHistoryReq.open(bugHistoryUrl)
        # except Exception as e:
        #     return 1
        # bugHistory =
        self.bugHistoryDict[str(id)] = bugHistory

    def return_bugHistoryDictLens(self):
        return len(self.bugHistoryDict)

    def return_bugHistoryDict(self):
        return self.bugHistoryDict

# aaa = bug2xlsx_request()
# aaa.login_getCookie()
# aaa.getBugHistory('179481')
# print(aaa.return_bugHistoryDict())
# ccc = aaa.getBugList(bbb)
