#-*- coding: utf-8 -*-
__author__ = 'wufeng_wb'
import time
import xlsxwriter

def sortList(list):
    aaa = []
    bbb = []
    ccc = []
    for i in list:
        row = list[i]
        if row[2] == 'P3-Norm':
            aaa.append([i,row[0],row[1],row[2],row[3]])
        elif row[2] == 'P2-High':
            bbb.append([i,row[0],row[1],row[2],row[3]])
        elif row[2] == 'P1-High':
            ccc.append([i,row[0],row[1],row[2],row[3]])
    return ccc+bbb+aaa

def countHistory(bugHistoryDict):
    newBugsDict = {}
    newBugsList = []
    resolvedBugsDict = {}
    resolvedBugsList = []
    bugCreateTimeList = []
    bugResolvedTimeList = []
    for i in bugHistoryDict:
        if len(newBugsDict) == 0:
            newBugsDict[bugHistoryDict[i]['createTime']] = 1
            bugCreateTimeList.append(bugHistoryDict[i]['createTime'])
        else:
            if bugHistoryDict[i]['createTime'] in bugCreateTimeList:
                newBugsDict[bugHistoryDict[i]['createTime']] = newBugsDict[bugHistoryDict[i]['createTime']] + 1
            else:
                newBugsDict[bugHistoryDict[i]['createTime']] = 1
                bugCreateTimeList.append(bugHistoryDict[i]['createTime'])
    for i in newBugsDict:
        if len(newBugsList) == 0:
            newBugsList.append([i,newBugsDict[i]])
        else:
            n = 0
            while n < len(newBugsList):
                if int(i.replace('-','')) < int(newBugsList[n][0].replace('-','')):
                    newBugsList.insert(n,[i,newBugsDict[i]])
                    break
                elif int(i.replace('-','')) > int(newBugsList[n][0].replace('-','')):
                    if n < len(newBugsList)-1:
                        n = n + 1
                    elif n == len(newBugsList)-1:
                        newBugsList.insert(n+1,[i,newBugsDict[i]])
                        break

    for i in bugHistoryDict:
        for j in bugHistoryDict[i]['resolvedTime']:
            if len(resolvedBugsDict) == 0:
                resolvedBugsDict[j] = 1
                bugResolvedTimeList.append(j)
            else:
                if j in bugResolvedTimeList:
                    resolvedBugsDict[j] = resolvedBugsDict[j] + 1
                else:
                    resolvedBugsDict[j] = 1
                    bugResolvedTimeList.append(j)
    for i in resolvedBugsDict:
        if len(resolvedBugsList) == 0:
            resolvedBugsList.append([i,resolvedBugsDict[i]])
        else:
            n = 0
            while n < len(resolvedBugsList):
                if int(i.replace('-','')) < int(resolvedBugsList[n][0].replace('-','')):
                    resolvedBugsList.insert(n,[i,resolvedBugsDict[i]])
                    break
                elif int(i.replace('-','')) > int(resolvedBugsList[n][0].replace('-','')):
                    if n < len(resolvedBugsList)-1:
                        n = n + 1
                    elif n == len(resolvedBugsList)-1:
                        resolvedBugsList.insert(n+1,[i,resolvedBugsDict[i]])
                        break

    # 现在有newBugsList和resolvedBugsList两张list,需要将resolvedBugsList中的修复bug数添加到newBugsList对应的日期中,若newBugsList中无此日期,则添加日期
    for i in resolvedBugsList:
        n = 0
        while n < len(newBugsList):
            if int(i[0].replace('-','')) < int(newBugsList[n][0].replace('-','')):
                newBugsList.insert(n,[i[0],0,i[1]])
                break
            elif int(i[0].replace('-','')) == int(newBugsList[n][0].replace('-','')):
                newBugsList[n].insert(2,i[1])
                break
            elif int(i[0].replace('-','')) > int(newBugsList[n][0].replace('-','')):
                    if n < len(newBugsList)-1:
                        n = n + 1
                    elif n == len(newBugsList)-1:
                        newBugsList.insert(n+1,[i[0],0,i[1]])
                        break
    for i in newBugsList:
        if len(i) == 2:
            i.insert(2,0)
    return newBugsList

def sortList_ChanDao(list,history):
    p4buglist = []
    p3buglist = []
    p2buglist = []
    p1buglist = []
    for i in list:
        if list[i][3] == '激活':
            if history[i]['reopenTime'] == []:
                pass
            else:
                if history[i]['resolvedTime'][len(history[i]['resolvedTime'])-1] < history[i]['reopenTime'][len(history[i]['reopenTime'])-1]:
                    list[i][3] = '重打开'
                    list[i][4] = ''
        row = list[i]
        if row[2] == '建议':
            if row[3] == '已解决' and row[4] == '延期处理':
                p4buglist.append([i,row[0],row[1],row[2],row[4]])
            else:
                p4buglist.append([i,row[0],row[1],row[2],row[3]])
        elif row[2] == '细微':
            if row[3] == '已解决' and row[4] == '延期处理':
                p3buglist.append([i,row[0],row[1],row[2],row[4]])
            else:
                p3buglist.append([i,row[0],row[1],row[2],row[3]])
        elif row[2] == '一般':
            if row[3] == '已解决' and row[4] == '延期处理':
                p2buglist.append([i,row[0],row[1],row[2],row[4]])
            else:
                p2buglist.append([i,row[0],row[1],row[2],row[3]])
        elif row[2] == '严重':
            if row[3] == '已解决' and row[4] == '延期处理':
                p1buglist.append([i,row[0],row[1],row[2],row[4]])
            else:
                p1buglist.append([i,row[0],row[1],row[2],row[3]])
    return p1buglist+p2buglist+p3buglist+p4buglist

def countHistory_ChanDao(bugHistoryDict):
    # 存放一次整理后的数据
    newBugsDict = {}
    # 存放二次排序后的数据
    newBugsList = []
    # 存放一次整理后的数据
    resolvedBugsDict = {}
    # 存放二次排序后的数据
    resolvedBugsList = []
    bugCreateTimeList = []
    bugResolvedTimeList = []
    reopenTimeDict = {}
    # 取bugHistoryDict中各bug的创建时间并汇总
    # 取第i个bug的各类时间
    for i in bugHistoryDict:
        # 当newBugsDict中为空时
        if len(newBugsDict) == 0:
            # 将第i个bug的创建时间增添入newBugsDict中,并且将newBugsDict中该创建时间的value值+1
            newBugsDict[bugHistoryDict[i]['createTime']] = 1
            # 将该创建时间增添入bugCreateTimeList中,用作重复校验
            bugCreateTimeList.append(bugHistoryDict[i]['createTime'])
        else:
            # 如果第i个bug的创建时间已经添加过
            if bugHistoryDict[i]['createTime'] in bugCreateTimeList:
                # 则newBugsDict中对应时间的value值+1
                newBugsDict[bugHistoryDict[i]['createTime']] = newBugsDict[bugHistoryDict[i]['createTime']] + 1
            else:
                # 否则将第i个bug的创建时间增添入newBugsDict中
                newBugsDict[bugHistoryDict[i]['createTime']] = 1
                # 并且将第i个bug的创建时间增添入bugCreateTimeList中,用作重复校验
                bugCreateTimeList.append(bugHistoryDict[i]['createTime'])
    # 将newBugsDict中的数据按照时间前后排序
    # 取newBugsDict中第i条创建时间数据
    for i in newBugsDict:
        # 若newBugsList为空时
        if len(newBugsList) == 0:
            # 将第一个读取的创建时间数据以List的形式加入到newBugsList中
            newBugsList.append([i,newBugsDict[i]])
        else:
            # 假定一个n值,用作序列
            n = 0
            # 循环比较i和newBugsList中的时间的大小
            while n < len(newBugsList):
                # 若i比newBugsList中第n位的时间小
                if i < newBugsList[n][0]:
                    # 则插入到newBugsList中原n位的位置
                    newBugsList.insert(n,[i,newBugsDict[i]])
                    # 跳出循环,因为再比较已经毫无疑义
                    break
                # 若i比newBugsList中第n位的时间大
                elif i > newBugsList[n][0]:
                    # 则当n所代表的newBugsList序号没有到最后一位时
                    if n < len(newBugsList)-1:
                        # 自加1
                        n = n + 1
                    # 反之,若n所代表的newBugsList序号已经为最后一位
                    elif n == len(newBugsList)-1:
                        # 则将i添加至newBugsList末尾
                        newBugsList.insert(n+1,[i,newBugsDict[i]])
                        # 跳出循环,因为再比较已经毫无疑义
                        break
    # 取bugHistoryDict中各bug的解决时间并汇总
    # 取第i个bug的各类时间
    for i in bugHistoryDict:
        for k in bugHistoryDict[i]['reopenTime']:
            if reopenTimeDict == {}:
                reopenTimeDict[k[0:10]] = k
            else:
                if k[0:10] in reopenTimeDict:
                    if k > reopenTimeDict[k[0:10]]:
                        reopenTimeDict[k[0:10]] = k
                    else:
                        pass
                else:
                    reopenTimeDict[k[0:10]] = k
        # 取该bug的第j个resolvedTime
        for j in bugHistoryDict[i]['resolvedTime']:
            if j[0:10] in reopenTimeDict:
                if j < reopenTimeDict[j[0:10]]:
                    pass
                else:
                    if len(resolvedBugsDict) == 0:
                        resolvedBugsDict[j[0:10]] = 1
                        bugResolvedTimeList.append(j[0:10])
                    else:
                        if j[0:10] in bugResolvedTimeList:
                            resolvedBugsDict[j[0:10]] = resolvedBugsDict[j[0:10]] + 1
                        else:
                            resolvedBugsDict[j[0:10]] = 1
                            bugResolvedTimeList.append(j[0:10])
            else:
                if len(resolvedBugsDict) == 0:
                        resolvedBugsDict[j[0:10]] = 1
                        bugResolvedTimeList.append(j[0:10])
                else:
                    if j[0:10] in bugResolvedTimeList:
                        resolvedBugsDict[j[0:10]] = resolvedBugsDict[j[0:10]] + 1
                    else:
                        resolvedBugsDict[j[0:10]] = 1
                        bugResolvedTimeList.append(j[0:10])
        reopenTimeDict = {}

    # 将resolvedBugsDict中的数据按照时间前后排序
    for i in resolvedBugsDict:
        if len(resolvedBugsList) == 0:
            resolvedBugsList.append([i,resolvedBugsDict[i]])
        else:
            n = 0
            while n < len(resolvedBugsList):
                if i < resolvedBugsList[n][0]:
                    resolvedBugsList.insert(n,[i,resolvedBugsDict[i]])
                    break
                elif i > resolvedBugsList[n][0]:
                    if n < len(resolvedBugsList)-1:
                        n = n + 1
                    elif n == len(resolvedBugsList)-1:
                        resolvedBugsList.insert(n+1,[i,resolvedBugsDict[i]])
                        break

    # 现在有newBugsList和resolvedBugsList两张list,需要将resolvedBugsList中的修复bug数添加到newBugsList对应的日期中,若newBugsList中无此日期,则添加日期
    for i in resolvedBugsList:
        n = 0
        while n < len(newBugsList):
            if i[0] < newBugsList[n][0]:
                newBugsList.insert(n,[i[0],0,i[1]])
                break
            elif i[0] == newBugsList[n][0]:
                newBugsList[n].insert(2,i[1])
                break
            elif i[0] > newBugsList[n][0]:
                    if n < len(newBugsList)-1:
                        n = n + 1
                    elif n == len(newBugsList)-1:
                        newBugsList.insert(n+1,[i[0],0,i[1]])
                        break
    for i in newBugsList:
        if len(i) == 2:
            i.insert(2,0)
    return newBugsList

class bugDataDict2xlsx():
    def __init__(self,mode,buglist,filedir,closedFlag,ChartDATA=None,reopenANDpending=None):
        self.mode = mode
        if self.mode == 0:
            self.buglist = sortList(buglist)
            self.closedFlag = closedFlag.replace(" ","")
            if ChartDATA == None:
                pass
            else:
                self.ChartDATA = countHistory(ChartDATA)
        elif self.mode == 2:
            self.buglist = sortList_ChanDao(buglist,ChartDATA)
            self.ChartDATA = countHistory_ChanDao(ChartDATA)
        # print(self.buglist)
        self.filedir = filedir

        # self.ChartDATA = [['2016-06-17', 5, 0], ['2016-06-20', 5, 4], ['2016-06-21', 5, 2], ['2016-06-22', 1, 6], ['2016-06-23', 0, 1], ['2016-06-24', 0, 4]]
        # print(self.ChartDATA)
        if reopenANDpending == None:
            pass
        else:
            self.reopenNumber = reopenANDpending[0]
            self.pendingNumber = reopenANDpending[1]

    def writebugListSheet(self):
        # 行码
        rowNum = 0
        # 列码
        colNum = 0
        # id宽,summary宽,assignee宽,Pri宽,status宽
        lenid = 0
        lensu = 0
        lenas = 8
        lenpr = 5
        lenst = 8
        for i in self.buglist:
            if lenid < len(i[0]):
                lenid = len(i[0])
            else:
                pass
            if lenas < len(i[2]):
                lenas = len(i[2])
            else:
                pass
            if lenpr < len(i[3]):
                lenpr = len(i[3])
            else:
                pass
            if lenst < len(i[4]):
                lenst = len(i[4])
            else:
                pass
        self.buglistSheet.set_column('A:A',lenid+1)
        self.buglistSheet.set_column('B:B',60)
        self.buglistSheet.set_column('C:C',lenas)
        self.buglistSheet.set_column('D:D',lenpr)
        self.buglistSheet.set_column('E:E',lenst+1)
        titleFormat = self.myBook.add_format({'font_name':'微软雅黑','align':'center','valign':'vcenter','border':1,'font_size':10})
        idFormat = self.myBook.add_format({'font_name':'微软雅黑','align':'center','valign':'vcenter','border':1,'font_size':10})
        suFormat = self.myBook.add_format({'font_name':'微软雅黑','border':1,'text_wrap':1,'font_size':10})
        asFormat = self.myBook.add_format({'font_name':'微软雅黑','align':'center','valign':'vcenter','border':1,'font_size':10})
        prFormat = self.myBook.add_format({'font_name':'微软雅黑','align':'center','valign':'vcenter','border':1,'font_size':10})
        stFormat = self.myBook.add_format({'font_name':'微软雅黑','align':'center','valign':'vcenter','border':1,'font_size':10})
        for title in ['ID','Summary','Assignee','Pri','Status']:
            self.buglistSheet.write(rowNum,colNum,title,titleFormat)
            colNum+=1
        rowNum = 1
        colNum = 0
        for i in self.buglist:
            colNum = 0
            self.buglistSheet.write(rowNum,colNum,i[0],idFormat)
            colNum = 1
            if self.mode == 0:
                bugurl = 'http://bugzilla.qiyi.domain/show_bug.cgi?id='+i[0]
                self.buglistSheet.write_url(rowNum,colNum,url=bugurl,string=i[1],cell_format=suFormat)
            elif self.mode == 2:
                bugurl = 'http://pm.game.qiyi.domain/index.php?m=bug&f=view&bugID='+i[0]
                self.buglistSheet.write_url(rowNum,colNum,url=bugurl,string=i[1],cell_format=suFormat)
            colNum = 2
            self.buglistSheet.write(rowNum,colNum,i[2],asFormat)
            colNum = 3
            self.buglistSheet.write(rowNum,colNum,i[3],prFormat)
            colNum = 4
            self.buglistSheet.write(rowNum,colNum,i[4],stFormat)
            if self.mode == 0:
                if i[4] != 'ASSI' and i[4] != 'REOP':
                    self.buglistSheet.set_row(rowNum,options={'hidden':True})
            elif self.mode == 2:
                if i[4] != '激活':
                    self.buglistSheet.set_row(rowNum,options={'hidden':True})
            rowNum += 1

    def writetotelbugSheet(self):
        rowNum = 1
        colNum = 0
        self.totelbugSheet.set_column('A:A',len('Total bug'))
        self.totelbugSheet.set_column('B:B',len('Resolved bug'))
        self.totelbugSheet.set_column('C:C',len('Open bug'))
        self.totelbugSheet.set_column('D:D',len('Pending'))
        self.totelbugSheet.set_column('E:E',len('Reopen bug'))
        self.totelbugSheet.set_column('F:F',len('Closed bug'))
        textFormat = self.myBook.add_format({'font_name':'微软雅黑','font_size':10,'align':'left','valign':'vcenter'})
        numFormat = self.myBook.add_format({'font_name':'微软雅黑','border':1,'font_size':10,'align':'left','valign':'vcenter',})
        self.totelbugSheet.write(0,0,'Total bug state:',textFormat)
        for title1 in ['Total bug','Resolved bug','Open bug','Pending','Reopen bug','Closed bug']:
            self.totelbugSheet.write(rowNum,colNum,title1,numFormat)
            colNum += 1
        if self.mode == 0:
            self.totelbugSheet.write_formula(2,0,'=COUNTA(BUG汇总列表!A:A)-1',numFormat)
            self.totelbugSheet.write_formula(2,1,'=COUNTIFS(BUG汇总列表!E:E,"RESO")',numFormat)
            self.totelbugSheet.write_formula(2,2,'=A3-B3-D3-E3-F3',numFormat)
            self.totelbugSheet.write_formula(2,3,'=COUNTIFS(BUG汇总列表!E:E,"PEND")',numFormat)
            self.totelbugSheet.write_formula(2,4,'=COUNTIFS(BUG汇总列表!E:E,"REOP")',numFormat)
            self.totelbugSheet.write_formula(2,5,'=COUNTIFS(BUG汇总列表!E:E,"'+self.closedFlag+'")',numFormat)
        elif self.mode == 2:
            self.totelbugSheet.write_formula(2,0,'=COUNTA(BUG汇总列表!A:A)-1',numFormat)
            self.totelbugSheet.write_formula(2,1,'=COUNTIFS(BUG汇总列表!E:E,"已解决")',numFormat)
            self.totelbugSheet.write_formula(2,2,'=A3-B3-D3-E3-F3',numFormat)
            self.totelbugSheet.write_formula(2,3,'=COUNTIFS(BUG汇总列表!E:E,"延期处理")',numFormat)
            # self.totelbugSheet.write(2,3,str(self.pendingNumber),numFormat)
            # self.totelbugSheet.write_formula(2,4,'=COUNTIFS(BUG汇总列表!E:E,"REOP")',numFormat)
            self.totelbugSheet.write(2,4,str(self.reopenNumber),numFormat)
            self.totelbugSheet.write_formula(2,5,'=COUNTIFS(BUG汇总列表!E:E,"已关闭")',numFormat)
        self.totelbugSheet.write(4,0,'Active bug state:',textFormat)
        colNum = 0
        if self.mode == 0:
            for title1 in ['Active Bug','P1','P2','P3']:
                self.totelbugSheet.write(5,colNum,title1,numFormat)
                colNum += 1
            self.totelbugSheet.write_formula(6,0,'=C3+E3',numFormat)
            self.totelbugSheet.write_formula(6,1,'=COUNTIFS(BUG汇总列表!D:D,"P1-High")-COUNTIFS(BUG汇总列表!D:D,"P1-High",BUG汇总列表!E:E,"RESO")-COUNTIFS(BUG汇总列表!D:D,"P1-High",BUG汇总列表!E:E,"PEND")-COUNTIFS(BUG汇总列表!D:D,"P1-High",BUG汇总列表!E:E,"'+self.closedFlag+'")',numFormat)
            self.totelbugSheet.write_formula(6,2,'=COUNTIFS(BUG汇总列表!D:D,"P2-High")-COUNTIFS(BUG汇总列表!D:D,"P2-High",BUG汇总列表!E:E,"RESO")-COUNTIFS(BUG汇总列表!D:D,"P2-High",BUG汇总列表!E:E,"PEND")-COUNTIFS(BUG汇总列表!D:D,"P2-High",BUG汇总列表!E:E,"'+self.closedFlag+'")',numFormat)
            self.totelbugSheet.write_formula(6,3,'=COUNTIFS(BUG汇总列表!D:D,"P3-Norm")-COUNTIFS(BUG汇总列表!D:D,"P3-Norm",BUG汇总列表!E:E,"RESO")-COUNTIFS(BUG汇总列表!D:D,"P3-Norm",BUG汇总列表!E:E,"PEND")-COUNTIFS(BUG汇总列表!D:D,"P3-Norm",BUG汇总列表!E:E,"'+self.closedFlag+'")',numFormat)
        elif self.mode == 2:
            for title1 in ['Active Bug','严重','一般','细微','建议']:
                self.totelbugSheet.write(5,colNum,title1,numFormat)
                colNum += 1
            self.totelbugSheet.write_formula(6,0,'=C3+E3',numFormat)
            self.totelbugSheet.write_formula(6,1,'=COUNTIFS(BUG汇总列表!D:D,"严重")-COUNTIFS(BUG汇总列表!D:D,"严重",BUG汇总列表!E:E,"已解决")-COUNTIFS(BUG汇总列表!D:D,"严重",BUG汇总列表!E:E,"延期处理")-COUNTIFS(BUG汇总列表!D:D,"严重",BUG汇总列表!E:E,"已关闭")',numFormat)
            self.totelbugSheet.write_formula(6,2,'=COUNTIFS(BUG汇总列表!D:D,"一般")-COUNTIFS(BUG汇总列表!D:D,"一般",BUG汇总列表!E:E,"已解决")-COUNTIFS(BUG汇总列表!D:D,"一般",BUG汇总列表!E:E,"延期处理")-COUNTIFS(BUG汇总列表!D:D,"一般",BUG汇总列表!E:E,"已关闭")',numFormat)
            self.totelbugSheet.write_formula(6,3,'=COUNTIFS(BUG汇总列表!D:D,"细微")-COUNTIFS(BUG汇总列表!D:D,"细微",BUG汇总列表!E:E,"已解决")-COUNTIFS(BUG汇总列表!D:D,"细微",BUG汇总列表!E:E,"延期处理")-COUNTIFS(BUG汇总列表!D:D,"细微",BUG汇总列表!E:E,"已关闭")',numFormat)
            self.totelbugSheet.write_formula(6,4,'=COUNTIFS(BUG汇总列表!D:D,"建议")-COUNTIFS(BUG汇总列表!D:D,"建议",BUG汇总列表!E:E,"已解决")-COUNTIFS(BUG汇总列表!D:D,"建议",BUG汇总列表!E:E,"延期处理")-COUNTIFS(BUG汇总列表!D:D,"建议",BUG汇总列表!E:E,"已关闭")',numFormat)


    def writeChartSheet(self):
        titleFormat = self.myBook.add_format({'font_name':'微软雅黑','align':'center','valign':'vcenter','border':1,'font_size':10})
        rowNum = 0
        colNum = 0
        self.chartSheet.set_column('A:A',10)
        self.chartSheet.set_column('B:B',10)
        self.chartSheet.set_column('C:C',10)
        self.chartSheet.set_column('D:D',10)
        for title in ['日期','BUG总数','新增BUG数','修复BUG数']:
            self.chartSheet.write(rowNum,colNum,title,titleFormat)
            if title == '修复BUG数':
                if self.mode == 0:
                    self.chartSheet.write_comment(rowNum,colNum,'本处统计的是resolved的BUG,并不是verified或者closed的BUG')
            colNum += 1
        rowNum = 1
        for data in self.ChartDATA:
            if rowNum == 1:
                colNum = 0
                self.chartSheet.write(rowNum,colNum,data[0],titleFormat)
                colNum = 1
                self.chartSheet.write(rowNum,colNum,data[1],titleFormat)
                colNum = 2
                self.chartSheet.write(rowNum,colNum,data[1],titleFormat)
                colNum = 3
                self.chartSheet.write(rowNum,colNum,data[2],titleFormat)
                rowNum += 1
            else:
                colNum = 0
                self.chartSheet.write(rowNum,colNum,data[0],titleFormat)
                colNum = 1
                self.chartSheet.write_formula(rowNum,colNum,'=B'+str(rowNum)+'+C'+str(rowNum+1),titleFormat)
                colNum = 2
                self.chartSheet.write(rowNum,colNum,data[1],titleFormat)
                colNum = 3
                self.chartSheet.write(rowNum,colNum,data[2],titleFormat)
                rowNum += 1
        self.totalChart.add_series({
                                    'name': '=BUG统计图表!$B$1',
                                    'categories': '=BUG统计图表!$A$2:$A$'+str(rowNum),
                                    'values': '=BUG统计图表!$B$2:$B$'+str(rowNum),
                                    'marker': {
                                        'type': 'diamond', 'size': 6, 'border': {'color': '#4F81BD'}, 'fill':   {'color': '#4F81BD'},
                                    },
                                    'data_labels': {'value': True, 'position': 'above'},
                                    'line': {
                                        'color':'#4F81BD', 'width': 3
                                    }
                                    })
        self.totalChart.add_series({
                                    'name': '=BUG统计图表!$C$1',
                                    'categories': '=BUG统计图表!$A$2:$A$'+str(rowNum),
                                    'values': '=BUG统计图表!$C$2:$C$'+str(rowNum),
                                    'marker': {
                                        'type': 'diamond', 'size': 6, 'border': {'color': '#D07C7A'}, 'fill':   {'color': '#D07C7A'},
                                    },
                                    'data_labels': {'value': True, 'position': 'left'},
                                    'line': {
                                        'color':'#D07C7A', 'width': 3
                                    }
                                    })
        self.totalChart.add_series({
                                    'name': '=BUG统计图表!$D$1',
                                    'categories': '=BUG统计图表!$A$2:$A$'+str(rowNum),
                                    'values': '=BUG统计图表!$D$2:$D$'+str(rowNum),
                                    'marker': {
                                        'type': 'diamond', 'size': 6, 'border': {'color': '#9BBB59'}, 'fill':   {'color': '#9BBB59'},
                                    },
                                    'data_labels': {'value': True, 'position': 'right'},
                                    'line': {
                                        'color':'#9BBB59', 'width': 3
                                    }
                                    })
        self.totalChart.set_title({'name': '当前项目BUG走势图', 'name_font': {'name': '微软雅黑', 'size': 16, 'bold': False}})
        self.totalChart.set_x_axis({
            'name': '日期', 'name_font': {'name ':'微软雅黑','size': 10, 'bold': False}
        })
        self.totalChart.set_y_axis({
            'name': '问题数', 'name_font': {'name ':'微软雅黑','size': 10, 'bold': False}
        })
        bugTotal = 0
        for i in self.ChartDATA:
            bugTotal = bugTotal + i[1]
        self.totalChart.set_size({'width': 110*len(self.ChartDATA)+100, 'height': 330})
        # self.totalChart.set_style(12)
        self.chartSheet.insert_chart('F1',self.totalChart)

    def create_xlsxNoChart(self):
        self.myTime = time.strftime('%Y%m%d%H%M%S',time.localtime())
        self.myBook = xlsxwriter.Workbook(self.filedir + 'BUGLIST_' + self.myTime + '.xlsx')
        self.buglistSheet = self.myBook.add_worksheet('BUG汇总列表')
        if self.mode == 0:
            self.buglistSheet.autofilter('E1:E'+ str(len(self.buglist)))
            self.buglistSheet.filter_column('E',"Status = REOP or Status = ASSI")
        elif self.mode == 2:
            self.buglistSheet.autofilter('E1:E'+ str(len(self.buglist)))
            self.buglistSheet.filter_column('E',"Status = 激活")
        self.writebugListSheet()
        self.totelbugSheet = self.myBook.add_worksheet('BUG统计情况')
        self.writetotelbugSheet()
        self.myBook.close()

    def create_xlsxWithChart(self):
        self.myTime = time.strftime('%Y%m%d%H%M%S',time.localtime())
        self.myBook = xlsxwriter.Workbook(self.filedir + 'BUGLIST_' + self.myTime + '.xlsx')
        self.buglistSheet = self.myBook.add_worksheet('BUG汇总列表')
        if self.mode == 0:
            self.buglistSheet.autofilter('E1:E'+ str(len(self.buglist)))
            self.buglistSheet.filter_column('E',"Status = REOP or Status = ASSI")
        elif self.mode == 2:
            self.buglistSheet.autofilter('E1:E'+ str(len(self.buglist)))
            self.buglistSheet.filter_column('E',"Status = 激活")
        self.writebugListSheet()
        self.totelbugSheet = self.myBook.add_worksheet('BUG统计情况')
        self.writetotelbugSheet()
        self.chartSheet = self.myBook.add_worksheet('BUG统计图表')
        self.totalChart = self.myBook.add_chart({'type': 'line'})
        self.writeChartSheet()
        self.myBook.close()
    #
    # def test(self):
    #     self.myTime = time.strftime('%Y%m%d%H%M%S',time.localtime())
    #     # self.myBook = xlsxwriter.Workbook(self.filedir + 'BUGLIST_' + self.myTime + '.xlsx')
    #     self.myBook = xlsxwriter.Workbook('BUGLIST_' + self.myTime + '.xlsx')
    #     self.chartSheet = self.myBook.add_worksheet('BUG统计图表')
    #     self.totalChart = self.myBook.add_chart({'type': 'line'})
    #     self.writeChartSheet()
    #     self.myBook.close()
#
# aa = bugDataDict2xlsx()
# aa.test()