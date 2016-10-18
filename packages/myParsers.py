#-*- coding: utf-8 -*-
__author__ = 'wufeng_wb'

from html.parser import HTMLParser

class bugIdParser(HTMLParser):
    def __init__(self):
        super(bugIdParser,self).__init__()
        self.buglist = ''
    def handle_starttag(self, tag, attrs):
        try:
            if tag == 'input' and attrs[0][1] == 'dependson':
                self.buglist = attrs[3][1]
                # print(attrs[3][1])
            else:
                pass
        except UnicodeEncodeError:
            pass
    def show(self):
        return self.buglist

class bugListParser(HTMLParser):
    def __init__(self):
        super(bugListParser,self).__init__()
        self.flag = ''
        self.data_key = ''
        self.data_list = []
        self.DATA_INIT = {}
    def handle_starttag(self, tag, attrs):
        # if tag == 'td' and ('class','first-child bz_id_column') in attrs:
        if tag == 'td' and ('class','first-child bz_id_column') in attrs:
            self.flag = 'ID_0'
        elif tag == 'td' and ('class','bz_short_desc_column') in attrs:
            self.flag = 'SUMMARY_0'
        elif tag == 'td' and ('class','bz_assigned_to_column') in attrs:
            self.flag = 'ASSIGNED_0'
        elif tag == 'td' and ('class','bz_priority_column') in attrs:
            self.flag = 'PRIORITY_0'
        elif tag == 'td' and ('class','bz_bug_status_column') in attrs:
            self.flag = 'BUGSTATE_0'
        elif tag == 'a' and self.flag == 'ID_0':
            self.flag = 'ID_1'
        elif tag == 'a' and self.flag == 'SUMMARY_0':
            self.flag = 'SUMMARY_1'
        elif tag == 'span' and self.flag == 'ASSIGNED_0':
            self.flag = 'ASSIGNED_1'
        elif tag == 'span' and self.flag == 'PRIORITY_0':
            self.flag = 'PRIORITY_1'
        elif tag == 'span' and self.flag == 'BUGSTATE_0':
            self.flag = 'BUGSTATE_1'
        else:
            self.flag = ''
            pass

    def handle_data(self, data):
        if self.flag == 'ID_1':
            self.data_key = data
            self.flag = ''
        elif self.flag == 'SUMMARY_1':
            self.data_list.append(data.rstrip())
            self.flag = ''
        elif self.flag == 'ASSIGNED_1':
            self.data_list.append(data.rstrip())
            self.flag = ''
        elif self.flag == 'PRIORITY_1':
            self.data_list.append(data.rstrip())
            self.flag = ''
        elif self.flag == 'BUGSTATE_1':
            self.data_list.append(data.rstrip())
            self.DATA_INIT[self.data_key] = self.data_list
            self.data_key = 0
            self.data_list = []
            self.flag = ''
        else:
            pass

    def show(self):
        return self.DATA_INIT

class bugCreateTimeParser(HTMLParser):
    def __init__(self):
        super(bugCreateTimeParser, self).__init__()
        self.createTime = {}
        self.flag = ''

    def handle_starttag(self, tag, attrs):
        # 检测到标签th与符合要求的attr,则flag置为好像是
        if tag == 'th' and ('class','field_label') in attrs:
            self.flag = 'Reported_0'
        # 检测到标签td,此时flag置为等待添加list
        elif self.flag == 'Reported_1' and tag == 'td':
            self.flag = 'standby'
        # 若标签不是th,则flag置为空
        else:
            self.flag = ''

    def handle_data(self, data):
        # 此时坐标位于标签th,检测th内data,如果是Reported则flag置为确信.接下来一个标签内的数据就是我要的
        if 'Reported:' in data:
            self.flag = 'Reported_1'
        elif 'Modified:' in data:
            self.flag = ''
        # 若data内无Reported,则flag置为空\
        # 如果检测到flag为standby状态,则直接将data添加到list.添加完毕后flag置为空
        if self.flag == 'standby':
            self.createTime['createTime'] = data[0:10]
            self.flag = ''

    def show(self):
        return self.createTime

class bugResolvedTimeParser(HTMLParser):
    def __init__(self):
        super(bugResolvedTimeParser,self).__init__()
        self.resolvedTimeDict = {'resolvedTime':[]}
        self.resolvedTime = ''
        self.lastTag = ''
        self.flag = 0
        self.lastTime = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.lastTag = 'tr'
        elif self.lastTag == 'tr' and tag == 'td':
            self.lastTag = 'td'
        elif self.lastTag == 'td' and tag == 'td':
            self.lastTag = 'td2'
        elif self.lastTag == 'td2' and tag == 'td':
            self.lastTag = 'td3'
        elif self.lastTag == 'td3' and tag == 'td':
            self.lastTag = 'td4'
        elif self.lastTag == 'td4' and tag == 'td':
            self.lastTag = 'td5'
        # else:
        #     self.flag = 0

    def handle_data(self, data):
        if self.lastTag == 'td2' and 'CST' in data:
            self.resolvedTime = data[0:10]
        elif self.lastTag == 'td3' and 'Status' in data:
            self.flag = 1
        elif self.flag == 1 and self.lastTag == 'td5' and 'RESOLVED' in data:
            if self.resolvedTime != self.lastTime:
                self.lastTime = self.resolvedTime
                self.resolvedTimeDict['resolvedTime'].append(self.lastTime)
                self.resolvedTime = ''
                self.lastTag = ''
                self.flag = 0
            else:
                pass
        # else:
        #     self.resolvedTime = ''

    def show(self):
        return self.resolvedTimeDict

class bugIdParser_requirement(HTMLParser):
    def __init__(self):
        super(bugIdParser_requirement,self).__init__()
        self.a = 0
        self.flag = ''
        self.id_list = []

    def handle_starttag(self, tag, attrs):
        self.a = 0
        if self.flag == '' and tag == 'tr' and ('class','text-center') in attrs:
            self.flag = 'tr'
        elif self.flag == 'tr' and tag == 'td':
            self.flag = 'tr_td1'
        elif self.flag == 'tr_td1' and tag == 'input':
            self.flag = 'tr_td1_input'
        elif self.flag == 'tr_td1_input' and tag == 'a':
            self.flag = 'tr_td1_input_a'

    def handle_data(self, data):
        if self.a == 0 and self.flag == 'tr_td1_input_a':
            self.flag = ''
            self.id_list.append(data)
        self.a = 1

    def show(self):
        return self.id_list

class bugListParser_requirement(HTMLParser):
    def __init__(self):
        super(bugListParser_requirement,self).__init__()
        self.a = 0
        self.flag = ''
        self.data_key = ''
        self.data_list = []
        self.DATA_INIT = {}

    def handle_starttag(self, tag, attrs):
        self.a = 0
        if self.flag == '' and tag == 'tr' and ('class','text-center') in attrs:
            self.flag = 'tr'
        elif self.flag == 'tr' and tag == 'td':
            self.flag = 'tr_td1'
        elif self.flag == 'tr_td1' and tag == 'input':
            self.flag = 'tr_td1_input'
        elif self.flag == 'tr_td1_input' and tag == 'a':
            self.flag = 'tr_td1_input_a'
        elif self.flag == 'tr_td1' and tag == 'td':
            self.flag = 'tr_td2'
        elif self.flag == 'tr_td2' and tag == 'span':
            self.flag = 'tr_td2_span'
        elif self.flag == 'tr_td2' and tag == 'td':
            self.flag = 'tr_td3'
        elif self.flag == 'tr_td3' and tag == 'td':
            self.flag = 'tr_td4'
        elif self.flag == 'tr_td4' and tag == 'span':
            self.flag = 'tr_td4_span'
        elif self.flag == 'tr_td4_span' and tag == 'a':
            self.flag = 'tr_td4_span_a'
        elif self.flag == 'tr_td4' and tag == 'td':
            self.flag = 'tr_td5'
        elif self.flag == 'tr_td5' and tag == 'td':
            self.flag = 'tr_td6'
        elif self.flag == 'tr_td6' and tag == 'td':
            self.flag = 'tr_td7'
        elif self.flag == 'tr_td7' and tag == 'td':
            self.flag = 'tr_td8'
        elif self.flag == 'tr_td8' and tag == 'td':
            self.flag = 'tr_td9'
        elif self.flag == 'tr_td9' and tag == 'td':
            self.flag = 'tr_td10'

    def handle_data(self, data):
        if self.a == 0 and self.flag == 'tr_td1_input_a':
            self.flag = 'tr_td1'
            self.data_key = data
        elif self.a == 0 and self.flag == 'tr_td2_span':
            self.flag = 'tr_td2'
            self.data_list.insert(0,data)
        elif self.a == 0 and self.flag == 'tr_td4_span_a':
            self.flag = 'tr_td4'
            self.data_list.insert(0,data)
        elif self.a == 0 and self.flag == 'tr_td5':
            self.flag = 'tr_td5'
            self.data_list.insert(2,data)
        elif self.a == 0 and self.flag == 'tr_td8':
            self.flag = 'tr_td8'
            self.data_list.insert(1,data)
        elif self.a == 0 and self.flag == 'tr_td10':
            self.flag = ''
            self.data_list.append(data)
            self.DATA_INIT[self.data_key] = self.data_list
            self.data_list = []
        self.a = 1

    def show(self):
        return self.DATA_INIT

class bugHistoryParser_requirement(HTMLParser):
    def __init__(self):
        super(bugHistoryParser_requirement,self).__init__()
        self.a = 0
        self.flag = ''
        self.theTime = ''
        self.historyDict = {'createTime': '', 'resolvedTime': [], 'reopenTime': []}

    def handle_starttag(self, tag, attrs):
        self.a = 0
        if self.flag == '' and tag == 'ol' and ('id','historyItem'):
            self.flag = 'ol'
        elif self.flag == 'ol' and tag == 'li':
            self.flag = 'ol_li'
        elif self.flag == 'ol_li' and tag == 'span':
            self.flag = 'ol_li_span'
        elif self.flag == 'ol_li_span' and tag == 'strong':
            self.flag = 'ol_li_span_strong'
        elif self.flag == 'ol_li_span_strong_skip' and tag == 'li':
            self.flag = 'ol_li'


    def handle_data(self, data):
        if self.a == 0 and self.flag == 'ol_li_span':
            self.theTime = data.replace('\n        ','').replace(', 由 ','')
            # print(self.createTime)
            self.a = 1
        elif self.a == 0 and self.flag == 'ol_li_span_strong':
            self.flag = 'ol_li_span_strong_skip'
            self.a = 1
        elif self.a == 1 and self.flag == 'ol_li_span_strong_skip':
            if data.replace(' ','')[0:2] == '创建':
                self.historyDict['createTime'] = self.theTime[0:10]
                self.theTime = ''
                self.flag = 'ol_li'
                self.a = 0
            elif data.replace(' ','')[0:2] == '解决':
                self.historyDict['resolvedTime'].append(self.theTime[0:19])
                self.theTime = ''
                self.flag = 'ol_li'
                self.a = 0
            elif data.replace(' ','')[0:2] == '激活':
                self.historyDict['reopenTime'].append(self.theTime[0:19])
                self.theTime = ''
                self.flag = 'ol_li'
                self.a = 0

    def show(self):
        return self.historyDict

class bugReopenANDPendingParser_requirement(HTMLParser):
    def __init__(self):
        super(bugReopenANDPendingParser_requirement,self).__init__()
        self.a = 0
        self.flag = ''
        self.statusChange = []
        self.bugHistory = []

    def handle_starttag(self, tag, attrs):
        self.a = 0
        if self.flag == '' and tag == 'ol' and ('id','historyItem'):
            self.flag = 'ol'
        elif self.flag == 'ol' and tag == 'li':
            self.flag = 'ol_li'
        elif self.flag == 'ol_li' and tag == 'span':
            self.flag = 'ol_li_span'
        elif self.flag == 'ol_li_span' and tag == 'strong':
            self.flag = 'ol_li_span_strong'
        elif self.flag == 'ol_li_span_strong_skip' and tag == 'li':
            self.flag = 'ol_li'
        elif self.flag == 'ol_li_span_strong_skip' and tag == 'strong':
            self.flag = 'ol_li_span_strong_skip_strong'


    def handle_data(self, data):
        if self.a == 0 and self.flag == 'ol_li_span_strong':
            self.flag = 'ol_li_span_strong_skip'
            self.a = 1
        elif self.a == 1 and self.flag == 'ol_li_span_strong_skip':
            self.statusChange.append(data.replace(' ','')[0:2])
            self.bugHistory.append(self.statusChange)
            self.statusChange = []
            self.a = 0
        elif self.a == 0 and self.flag == 'ol_li_span_strong_skip_strong':
            self.bugHistory[len(self.bugHistory)-1].append(data)
            self.flag = 'ol_li'

    def show(self):
        return self.bugHistory


