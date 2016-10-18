# -*- coding: utf-8 -*-
__author__ = 'wufeng_wb'

import sys
import time,threading
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from packages.myRequests import bug2xlsx_request
from packages.data2xlsx import bugDataDict2xlsx
from packages.myWidgets import *

# 新建一个继承自QMainWindow的类,创建一个自定义的窗口
class bug2xlsx(QtWidgets.QMainWindow):
    def __init__(self):
        super(bug2xlsx, self).__init__()
        self.hasSubCategory = 0
        self.drawChart = 0
        self.initUI()

    # 初始化界面
    def initUI(self):
        #设置QMainWindow属性
        self.setWindowTitle("测试工具集")
        self.setWindowIcon(QtGui.QIcon('resource/icon02.ico'))
        # desk_width = app.desktop().width()
        # desk_height = app.desktop().height()
        win_width = 460
        win_height = 255
        self.setFixedWidth(win_width)
        self.setFixedHeight(win_height)
        # self.setGeometry((desk_width-desk_width%2)/2-(win_width-win_width%2)/2, (desk_height-desk_height%2)/2-(win_height-win_height%2)/2, win_width, win_height)
        # 去除系统边框
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # 子部件阴影,可应用于系统边框,若边框去除,则无效
        # mainShadow = QtWidgets.QGraphicsDropShadowEffect()
        # mainShadow.setColor(QtCore.Qt.black)
        # mainShadow.setOffset(10,10)
        # mainShadow.setBlurRadius(2)
        # self.setGraphicsEffect(mainShadow)
        # 背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground,True)

        # 新增一个QWidget,浮于Window上方,与Window等大。主要作用是背景
        self.main_widget = QtWidgets.QWidget(self)
        self.main_widget.setGeometry(0,0,460,255)
        self.main_widget.setObjectName("main_widget")
        self.main_widget.setStyleSheet("#main_widget {background-image:url(resource/shadow.png)}")
        # 新增一个最小化按钮,属于main_widget
        self.minWin_button = minButton(self)
        self.minWin_button.initStyle(enabled=True)
        self.minWin_button.setGeometry(361,10,42,20)
        self.minWin_button.clicked.connect(self.showMinimized)
        # 新增一个关闭按钮,属于main_widget
        self.closeWin_button = closeButton(self)
        self.closeWin_button.initStyle(enabled=True)
        self.closeWin_button.setGeometry(403,10,42,20)
        self.closeWin_button.clicked.connect(self.close)

        # 新增一个Qtab_widget
        self.tab_widget = QtWidgets.QTabWidget(self.main_widget)
        self.tab_widget.setGeometry(10,10,440,230)
        self.tab_widget.setObjectName("tab_widget")
        # 如果不写::pane,会遗留左右下三条边框;如果使用setDocumentMode,会遗留上边框
        self.tab_widget.setStyleSheet("#tab_widget::pane {border:0}")
        # 将tab_widget的tabBar命名为tab_widget_bar
        self.tab_widget.tabBar().setObjectName("tab_widget_bar")
        # self.tab_widget.tabBar().setStyleSheet("#tab_widget_bar::pane {left:20px}")
        # 去除变框比CSS样式的0px边框更加的彻底,但是有个问题,无法去掉上边框
        # self.tab_widget.setDocumentMode(True)
        # self.tab_widget.setTabPosition(2)

        # 新增第一个QWidget,隶属于Qtab_widget
        self.firstTab_widget = QtWidgets.QWidget(self.tab_widget)
        # self.icon01 = QtGui.QIcon("resource/111.png")
        self.tab_widget.addTab(self.firstTab_widget,"")
        self.firstTab_widget.setObjectName("firstTab_widget")
        self.firstTab_widget.setStyleSheet("#firstTab_widget {border:0;border-bottom-left-radius:4px;border-bottom-right-radius:4px;background-image:url(resource/bug2xlsx.png)}")

        #新增一个QTabWidget,隶属于firstTab_widget
        self.bug2xlsx_tabWidget = QtWidgets.QTabWidget(self.firstTab_widget)
        self.bug2xlsx_tabWidget.setGeometry(5,0,440,230)
        self.bug2xlsx_tabWidget.setObjectName("bug2xlsx_tabWidget")
        # 如果不写::pane,会遗留左右下三条边框;如果使用setDocumentMode,会遗留上边框
        self.bug2xlsx_tabWidget.setStyleSheet("#bug2xlsx_tabWidget::pane {border:0}")
        # 将tab_widget的tabBar命名为tab_widget_bar
        self.bug2xlsx_tabWidget.tabBar().setObjectName("bug2xlsx_tabWidget_bar")
        self.bug2xlsx_tabWidget.setTabPosition(2)

        # 新增JIRA_tab,隶属于bug2xlsx_tabWidget
        self.JIRA_tab = QtWidgets.QWidget(self.bug2xlsx_tabWidget)
        # self.icon01 = QtGui.QIcon("resource/111.png")
        self.bug2xlsx_tabWidget.addTab(self.JIRA_tab,"")
        self.JIRA_tab.setObjectName("JIRA")
        self.JIRA_tab.setStyleSheet("#JIRA {border:0;border-bottom-left-radius:4px;border-bottom-right-radius:4px;}")

        # 新增Bugzilla_tab,隶属于bug2xlsx_tabWidget
        self.Bugzilla_tab = QtWidgets.QWidget(self.bug2xlsx_tabWidget)
        # self.icon01 = QtGui.QIcon("resource/111.png")
        self.bug2xlsx_tabWidget.addTab(self.Bugzilla_tab,"")
        self.Bugzilla_tab.setObjectName("Bugzilla")
        self.Bugzilla_tab.setStyleSheet("#Bugzilla {border:0;border-bottom-left-radius:4px;border-bottom-right-radius:4px;}")

        # 新增ChanDao_tab,隶属于bug2xlsx_tabWidget
        self.ChanDao_tab = QtWidgets.QWidget(self.bug2xlsx_tabWidget)
        # self.icon01 = QtGui.QIcon("resource/111.png")
        self.bug2xlsx_tabWidget.addTab(self.ChanDao_tab,"")
        self.ChanDao_tab.setObjectName("ChanDao")
        self.ChanDao_tab.setStyleSheet("#ChanDao {border:0;border-bottom-left-radius:4px;border-bottom-right-radius:4px;}")

        #设置BUGID输入
        self.bugID_label = QtWidgets.QLabel(self.Bugzilla_tab)
        self.bugID_label.setText(u"输入汇总bug:")
        self.bugID_label.setObjectName("bugID_label")
        self.bugID_label.setStyleSheet("#bugID_label {font-family:幼圆;font-size:14px;}")
        self.bugID_label.setGeometry(29,10,100,20)
        self.bugID_edit = QtWidgets.QLineEdit(self.Bugzilla_tab)
        self.bugID_edit.setObjectName("bugID_edit")
        self.bugID_edit.setStyleSheet("#bugID_edit {font-family:幼圆;font-size:14px;background-color:rgba(0,0,0,0.1);border-radius: 2px;border:1px solid lightgrey}")
        self.bugID_edit.setGeometry(102,11,100,20)

        # 是否需要输出图表
        self.chart_label = QtWidgets.QLabel(self.Bugzilla_tab)
        self.chart_label.setText(u"是否输出图表:")
        self.chart_label.setObjectName("chart_label")
        self.chart_label.setStyleSheet("#chart_label {font-family:幼圆;font-size:14px;}")
        self.chart_label.setGeometry(217,10,105,20)
        self.chart_group = QtWidgets.QWidget(self.Bugzilla_tab)
        self.chart_group.setGeometry(310,6,100,30)
        self.chart_group.setObjectName("chart_group")
        # self.chart_group.setStyleSheet("#chart_group {font-family:幼圆;font-size:14px;}")
        self.chart01_radio = QtWidgets.QRadioButton(u'否',self.chart_group)
        self.chart01_radio.setObjectName("chart01_radio")
        self.chart01_radio.setStyleSheet("#chart01_radio {font-family:幼圆;font-size:13px;padding:4px;border:0;border-radius:7px;background-color:rgba(0,0,0,0.1)}")
        self.chart01_radio.setGeometry(0,3,45,23)
        self.chart02_radio = QtWidgets.QRadioButton(u'是',self.chart_group)
        self.chart02_radio.setObjectName("chart02_radio")
        self.chart02_radio.setStyleSheet("#chart02_radio {font-family:幼圆;font-size:13px;padding:4px;border:0;border-radius:7px;background-color:rgba(0,0,0,0.1)}")
        self.chart02_radio.setGeometry(50,3,45,23)



        # 创建关闭问题单标识
        self.closedBug_label = QtWidgets.QLabel(self.Bugzilla_tab)
        self.closedBug_label.setText(u"问题单关闭标识:")
        self.closedBug_label.setObjectName("closedBug_label")
        self.closedBug_label.setStyleSheet("#closedBug_label {font-family:幼圆;font-size:14px;}")
        self.closedBug_label.setGeometry(203,70,105,20)
        # self.closedBug_label.setVisible(False)
        self.closedBug_flag = QtWidgets.QComboBox(self.Bugzilla_tab)
        self.closedBug_flag.setObjectName("closedBug_flag")
        self.closedBug_flag.addItem("    VERI")
        self.closedBug_flag.addItem("    CLOS")
        self.closedBug_flag.setGeometry(308,71,100,20)
        self.closedBug_flag.setStyleSheet("#closedBug_flag {font-family:幼圆;font-size:13px;padding:4px;border:0;border-radius:2px;background-color:rgba(0,0,0,0.1)} #closedBug_flag::drop-down{border:0} #closedBug_flag::down-arrow{margin-left:-10px;width:16px;height:16px;background-image:url(resource/down_arrow.png)}")
        # self.closedBug_flag.setVisible(False)
        # self.comboBox.setItemText(0, _translate("Form", "新111"))
        # self.comboBox.setItemText(1, _translate("Form", "新建22"))

        #创建一个文件夹路径部件标题Label
        self.chooseDir_label = QtWidgets.QLabel(u'xlsx保存路径:',self.Bugzilla_tab)
        self.chooseDir_label.setObjectName("chooseDir_label")
        self.chooseDir_label.setGeometry(13,155,100,20)
        self.chooseDir_label.setStyleSheet("#chooseDir_label {font-family:幼圆;font-size:14px;}")
        #创建一个文件夹路径展示LineEdit
        self.chooseDir_edit = QtWidgets.QLineEdit(self.Bugzilla_tab)
        self.chooseDir_edit.setObjectName("chooseDir_edit")
        self.chooseDir_edit.setStyleSheet("#chooseDir_edit {font-family:幼圆;font-size:14px;background-color:rgba(0,0,0,0.1);border-radius: 2px;border:1px solid lightgrey}")
        self.chooseDir_edit.setEnabled(False)
        self.chooseDir_edit.setGeometry(103,155,270,20)
        #创建一个文件夹选择Button
        self.chooseDir_button = chooseButton('...',self.Bugzilla_tab)
        self.chooseDir_button.setObjectName("chooseDir_button")
        self.chooseDir_button.setGeometry(380,155,30,20)
        self.chooseDir_button.initStyle(enabled=True)
        self.chooseDir_button.clicked.connect(self.do_chooseDir_button)

        #创建内容验证后输出Label
        self.prompt_label = QtWidgets.QLabel(self.Bugzilla_tab)
        self.prompt_label.setObjectName("prompt_label")
        # label长度自适应
        # self.prompt_label.adjustSize()
        # label自动换行
        # self.prompt_label.setWordWrap(True)
        # 文字居中
        self.prompt_label.setAlignment(QtCore.Qt.AlignCenter)
        # self.prompt_label.setStyleSheet("#prompt_label {font-size:4px}")
        self.prompt_label.setGeometry(20,105,400,20)

        #创建一个进度条
        self.theBar_progress = QtWidgets.QProgressBar(self.Bugzilla_tab)
        self.theBar_progress.setObjectName("theBar_progress")
        self.theBar_progress.setStyleSheet("#theBar_progress {border: 1px solid lightgrey;border-radius: 5px;background-color: #FFFFFF;} QProgressBar::chunk {background-color:#92B827;width: 20px}")
        self.theBar_progress.setGeometry(20,135,380,20)
        self.theBar_progress.setMinimum(0)
        self.theBar_progress.setMaximum(3)
        self.theBar_progress.setTextVisible(False)
        self.theBar_progress.setVisible(False)

        #创建两个个单选框,默认不选
        self.subCategory_label = QtWidgets.QLabel(u'二级汇总ID:',self.Bugzilla_tab)
        self.subCategory_label.setObjectName("subCategory_label")
        self.subCategory_label.setGeometry(27,70,100,20)
        self.subCategory_label.setStyleSheet("#subCategory_label {font-family:幼圆;font-size:14px;border:0;border-radius:3px;background:rgba(0,0,0,0)}")
        # self.subCategory_label.setVisible(False)
        self.subCategory_group = QtWidgets.QWidget(self.Bugzilla_tab)
        self.subCategory_group.setGeometry(105,66,100,30)
        # self.subCategory_group.setVisible(False)
        self.subCategory_group.setObjectName("chart_group")
        self.subCategory01_radio = QtWidgets.QRadioButton(u'无',self.subCategory_group)
        self.subCategory01_radio.setObjectName("subCategory01_radio")
        self.subCategory01_radio.setGeometry(0,3,45,23)
        self.subCategory01_radio.setStyleSheet("#subCategory01_radio {font-family:幼圆;font-size:13px;padding:4px;border:0;border-radius:7px;background-color:rgba(0,0,0,0.1)}")
        self.subCategory02_radio = QtWidgets.QRadioButton(u'有',self.subCategory_group)
        self.subCategory02_radio.setObjectName("subCategory02_radio")
        self.subCategory02_radio.setGeometry(50,3,45,23)
        self.subCategory02_radio.setStyleSheet("#subCategory02_radio {font-family:幼圆;font-size:13px;padding:4px;border:0;border-radius:7px;background-color:rgba(0,0,0,0.1)}")


        # 创建一个按钮
        self.enter_button = startButton('开始', self.Bugzilla_tab)
        # self.enter_button.setObjectName("enter_button")
        self.enter_button.setGeometry(330,180,80,20)
        self.enter_button.initStyle(enabled=True)
        # self.enter_button.setStyleSheet("QPushButton{background-image:url(resource/icon.ico);}")
        self.enter_button.clicked.connect(self.processMode)
        # self.enter_button.clicked.connect(self.test)


        # 新增第二个QWidget,隶属于Qtab_widget
        self.secondTab_widget = QtWidgets.QWidget(self.tab_widget)
        self.tab_widget.addTab(self.secondTab_widget,"")
        self.secondTab_widget.setObjectName("secondTab_widget")
        self.secondTab_widget.setStyleSheet("#secondTab_widget {border:0;border-bottom-left-radius:4px;border-bottom-right-radius:4px;background-image:url(resource/help.png)}")
        # 多次设定styleSheet会只去最后一个,所以一次性设定
        self.tab_widget.tabBar().setStyleSheet(
                                              # "#tab_widget_bar::tab {margin-left:20px}"
                                              "#tab_widget_bar::tab::first {margin-left:20px;background-image:url(resource/bug2xlsxTab_selected.png);position:absolute;left:5px;width:80px;height:25px;border-radius:3px}"
                                              "#tab_widget_bar::tab::first::selected {margin-left:20px;top:3px;border:0;}"
                                              "#tab_widget_bar::tab::first::!selected {margin-left:20px;background-image:url(resource/bug2xlsxTab_!selected.png);top:6px;border:0;}"
                                              "#tab_widget_bar::tab::last {background-image:url(resource/helpTab_selected.png);left:1px;width:80px;height:25px;border-radius:3px}"
                                              "#tab_widget_bar::tab::last::selected {top:3px;border:0;}"
                                              "#tab_widget_bar::tab::last::!selected {background-image:url(resource/helpTab_!selected.png);top:6px;border:0;}"
                                              )
        self.bug2xlsx_tabWidget.tabBar().setStyleSheet(
                                              # "bug2xlsx_tabWidget_bar"
                                              "#bug2xlsx_tabWidget_bar::tab::first {border-radius:3px}"
                                              "#bug2xlsx_tabWidget_bar::tab::first::selected {border:0;}"
                                              "#bug2xlsx_tabWidget_bar::tab::first::!selected {border:0;}"
                                              "#bug2xlsx_tabWidget_bar::tab::middle {border-radius:3px}"
                                              "#bug2xlsx_tabWidget_bar::tab::middle::selected {border:0;}"
                                              "#bug2xlsx_tabWidget_bar::tab::middle::!selected {border:0;}"
                                              "#bug2xlsx_tabWidget_bar::tab::last {border-radius:3px}"
                                              "#bug2xlsx_tabWidget_bar::tab::last::selected {border:0;}"
                                              "#bug2xlsx_tabWidget_bar::tab::last::!selected {border:0;}"
                                              )
        # 帮助信息
        # self.helpImfor = QtWidgets.QWidget(self.secondTab_widget)
        # self.helpImfor.setObjectName("helpImfor")
        # self.helpImfor.setGeometry(20,15,200,110)
        # self.helpImfor.setStyleSheet("#helpImfor {background-color:rgba(0,0,0,0);border:0;border-radius:3px}")
        self.intro_edit = QtWidgets.QTextEdit(self.secondTab_widget)
        self.intro_edit.setGeometry(40,15,215,70)
        self.intro_edit.setObjectName("intro_edit")
        self.intro_edit.setText("    写这个工具一是为了提高工作效率,二是写着玩.本工具会不定期更新功能,更新后会立刻通知大家哦~")
        self.intro_edit.setStyleSheet("#intro_edit {font-weight:bold;color:white;font-family:幼圆;font-size:14px;background-color:rgba(0,0,0,0.12);border-radius:3px}")
        self.intro_edit.setEnabled(False)
        self.contact_label = QtWidgets.QTextEdit(self.secondTab_widget)
        self.contact_label.setGeometry(40,95,215,55)
        self.contact_label.setObjectName("contact_label")
        self.contact_label.setStyleSheet("#contact_label {font-weight:bold;color:white;font-family:幼圆;font-size:14px;background-color:rgba(0,0,0,0.12);border-radius:3px}")
        self.contact_label.setText("         联系方式:\n企鹅852353148\n邮箱wufeng_wb@qiyi.com")
        self.contact_label.setEnabled(False)

    #获取文件保存地址
    def do_chooseDir_button(self):
        filedir = QtWidgets.QFileDialog.getExistingDirectory()
        if filedir:
            filedir = filedir + "/"
            self.chooseDir_edit.setText(filedir)
        else:
            self.chooseDir_edit.setText(filedir)

    # 有空研究一下原理
    def mousePressEvent(self, event):
        if(event.button() == QtCore.Qt.LeftButton):
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            # QtWidgets.QApplication.postEvent(self, QtCore.QEvent(1))
            event.accept()
        # if(event.button() == QtCore.Qt.RightButton):
        #     print('111')
    # 有空研究一下原理
    def mouseMoveEvent(self, event):
        if(event.buttons() == QtCore.Qt.LeftButton):
            # print(event.globalPos())
            try:
                self.move(event.globalPos() - self.dragPosition)
            except Exception as e:
                print(e)
            event.accept()

    def processMode(self):
        if self.bugID_edit.text().isdigit() == True:
            if self.subCategory01_radio.isChecked() == True or self.subCategory02_radio.isChecked() == True:
                if self.chart01_radio.isChecked() == True or self.chart02_radio.isChecked() == True:
                    # 无二级
                    if self.subCategory01_radio.isChecked() == True:
                        # 不生成图表
                        if self.chart01_radio.isChecked() == True:
                            self.hasSubCategory = 0
                            self.drawChart = 0
                            self.theBar_progress.setMaximum(4)
                            self.createThread()
                        # 生成图表
                        elif self.chart02_radio.isChecked() == True:
                            self.hasSubCategory = 0
                            self.drawChart = 1
                            self.theBar_progress.setMaximum(5)
                            self.createThread()
                    # 有二级
                    elif self.subCategory02_radio.isChecked() == True:
                        # 不生成图表
                        if self.chart01_radio.isChecked() == True:
                            self.hasSubCategory = 1
                            self.drawChart = 0
                            self.theBar_progress.setMaximum(5)
                            self.createThread()
                        # 生成图表
                        elif self.chart02_radio.isChecked() == True:
                            self.hasSubCategory = 1
                            self.drawChart = 1
                            self.theBar_progress.setMaximum(6)
                            self.createThread()
                else:
                    self.prompt_label.setStyleSheet("#prompt_label {font-family:幼圆;font-weight:bold;font-size:16px;color:#FF4D4D}")
                    self.prompt_label.setText(u"是否输出图表?")
            else:
                self.prompt_label.setStyleSheet("#prompt_label {font-family:幼圆;font-weight:bold;font-size:16px;color:#FF4D4D}")
                self.prompt_label.setText(u"是否存在二级分类?")
        else:
            self.prompt_label.setStyleSheet("#prompt_label {font-family:幼圆;font-weight:bold;font-size:16px;color:#FF4D4D}")
            self.prompt_label.setText(u"请输入正确的数字ID!")

    #进度条状态
    def theBar_display(self,params):
        # status为0即为任务开始状态,需要禁用页面上所有按钮/复选框/输入框,需要给出文字提示,且设定进度条
        if params[0] == 0:
            self.minWin_button.initStyle(enabled=False)
            self.minWin_button.setEnabled(False)
            self.closeWin_button.initStyle(enabled=False)
            self.closeWin_button.setEnabled(False)
            self.bugID_edit.setEnabled(False)
            self.chart01_radio.setEnabled(False)
            self.chart02_radio.setEnabled(False)
            self.subCategory01_radio.setEnabled(False)
            self.subCategory02_radio.setEnabled(False)
            self.chooseDir_button.initStyle(enabled=False)
            self.chooseDir_button.setEnabled(False)
            self.enter_button.setText('请稍候')
            self.enter_button.initStyle(enabled=False)
            self.enter_button.setEnabled(False)
            self.closedBug_flag.setEnabled(False)
            # 告知用户任务马上开始,放开进度栏的展示
            self.prompt_label.setStyleSheet("#prompt_label {font-family:幼圆;font-weight:bold;font-size:14px;color:#487707}")
            self.prompt_label.setText(params[2])
            self.theBar_progress.setValue(params[1])
            self.theBar_progress.setVisible(True)
        # status为1即任务进行中,需要给出文字提示,且设定进度条
        elif params[0] == 1:
            self.prompt_label.setText(params[2])
            self.theBar_progress.setValue(params[1])
        # status为2即任务进行执行成功,需要启用页面上所有按钮/复选框/输入框,需要给出文字提示,且设定进度条
        elif params[0] == 2:
            self.prompt_label.setText(params[2])
            self.theBar_progress.setValue(params[1])
            # 启用页面上所有按钮/复选框/输入框
            self.minWin_button.initStyle(enabled=True)
            self.minWin_button.setEnabled(True)
            self.closeWin_button.initStyle(enabled=True)
            self.closeWin_button.setEnabled(True)
            self.bugID_edit.setEnabled(True)
            self.chart01_radio.setEnabled(True)
            self.chart02_radio.setEnabled(True)
            self.subCategory01_radio.setEnabled(True)
            self.subCategory02_radio.setEnabled(True)
            self.chooseDir_button.initStyle(enabled=True)
            self.chooseDir_button.setEnabled(True)
            self.enter_button.setText('再次开始')
            self.enter_button.initStyle(enabled=True)
            self.enter_button.setEnabled(True)
            self.closedBug_flag.setEnabled(True)
        elif params[0] == 3:
            self.doThread.terminate()
            self.prompt_label.setStyleSheet("#prompt_label {font-family:幼圆;font-weight:bold;font-size:16px;color:#FF4D4D}")
            self.prompt_label.setText(params[2])
            self.theBar_progress.setValue(params[1])
            # 启用页面上所有按钮/复选框/输入框
            self.minWin_button.initStyle(enabled=True)
            self.minWin_button.setEnabled(True)
            self.closeWin_button.initStyle(enabled=True)
            self.closeWin_button.setEnabled(True)
            self.bugID_edit.setEnabled(True)
            self.chart01_radio.setEnabled(True)
            self.chart02_radio.setEnabled(True)
            self.subCategory01_radio.setEnabled(True)
            self.subCategory02_radio.setEnabled(True)
            self.chooseDir_button.initStyle(enabled=True)
            self.chooseDir_button.setEnabled(True)
            self.enter_button.setText('再次开始')
            self.enter_button.initStyle(enabled=True)
            self.enter_button.setEnabled(True)
            self.closedBug_flag.setEnabled(True)

    # 新建信息收集与处理线程
    def createThread(self):
        bugID = self.bugID_edit.text()
        fileDIR = self.chooseDir_edit.text()
        self.doThread = thread(bugid=bugID,filedir=fileDIR,hasSubCategory=self.hasSubCategory,drawChart=self.drawChart,closedFlag=self.closedBug_flag.currentText())
        self.doThread.trigger.connect(self.theBar_display)
        self.doThread.trigger2.connect(self.stop_or_continue)
        self.doThread.start()

    def stop_or_continue(self,j):
        if j == 'wait':
            ccc = QtCore.QWaitCondition()
            self.doThread.wait()
            reply = QtWidgets.QMessageBox.question(self,'那啥','检测到当前一级汇总ID下存在大于十个的二级汇总ID,确定要继续？',QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel,QtWidgets.QMessageBox.Ok)
            if reply == QtWidgets.QMessageBox.Ok:
                self.doThread.wait(1)
            elif reply == QtWidgets.QMessageBox.Cancel or reply == QtWidgets.QMessageBox.close:
                params = [3,0,'任务已终止!']
                self.theBar_display(params)

    def test(self):
        print(self.closedBug_flag.currentText())
# 任务线程
class thread(QtCore.QThread):
    trigger = QtCore.pyqtSignal(list)
    trigger2 = QtCore.pyqtSignal(str)
    def __init__(self,bugid,filedir,hasSubCategory,drawChart,closedFlag):
        super(thread,self).__init__()
        self.bugid = bugid
        self.filedir = filedir
        self.hasSubCategory = hasSubCategory
        self.drawChart = drawChart
        self.closedFlag = closedFlag
        # self.type = type

    # 执行
    def gogogo(self):
        # j = 'wait'
        # self.trigger2.emit(j)
        # 程序已准备好,告诉用户任务马上开始
        params = [0,0,'任务马上开始,请稍候...']
        self.trigger.emit(params)
        time.sleep(1)
        # 判断是否有二级,若无二级,则告知用户即将请求汇总bug下的所有bug的id并生成为列表以供使用;
        # 若有二级,则告知用户首先需要请求汇总bug下的各二级汇总bug的id;
        if self.hasSubCategory == 0:
            # 此时告知用户正在请求汇总bug下所有bug的id
            params = [1,1,'正在请求汇总bug下所有bug的id...']
            self.trigger.emit(params)
            aid = str(self.bugid)
            bugData = bug2xlsx_request()
            cidList = bugData.return_idList(aid)
            if cidList == []:
                params = [3,0,'汇总id下未发现挂靠BUG,请确认id是否正确!']
                self.trigger.emit(params)
            elif cidList == 1:
                params = [3,0,'网络或服务器异常!']
                self.trigger.emit(params)
            else:
                if self.drawChart == 0:
                    # 此时告知用户正在请求buglist页
                    params = [1,2,'正在根据bugid请求buglist页...']
                    self.trigger.emit(params)
                    bugDataDict = bugData.getBugList(cidList)
                    if bugDataDict == 1:
                        params = [3,0,'网络或服务器异常!']
                        self.trigger.emit(params)
                    else:
                        # 此时告知用户正在生成无图表的xlsx
                        params = [1,3,'正在生成无图表的xlsx...']
                        self.trigger.emit(params)
                        createXlsx = bugDataDict2xlsx(buglist=bugDataDict,filedir=self.filedir,closedFlag=self.closedFlag)
                        createXlsx.create_xlsxNoChart()
                        # 此时告知用户xlsx生成成功
                        params = [2,4,'xlsx生成成功,点击开始可再次生成']
                        self.trigger.emit(params)
                else:
                    # 此时告知用户正在请求bug历史记录
                    params = [1,2,'正在根据bugid搜集bug历史记录...']
                    self.trigger.emit(params)
                    # 每个cid新建一个线程,每个线程负责取得每个cid对应bug的历史记录
                    # 每个线程的执行开始时间间隔1s
                    # 每个线程之间不需要互相等待,独立运行
                    # 主函数等待搜集的历史记录中记录数等于cid数量后继续执行
                    # 线程取得bug的历史记录后即刻添加至历史记录dict中
                    for cid in cidList:
                        threading.Thread(target=bugData.getBugHistory,args=(cid,)).start()
                        time.sleep(0.5)
                    while bugData.return_bugHistoryDictLens() < len(cidList):
                        time.sleep(1)
                    bugHistoryDict = bugData.return_bugHistoryDict()
                    # 此时告知用户正在请求buglist页
                    params = [1,3,'正在根据bugid请求buglist页...']
                    self.trigger.emit(params)
                    bugDataDict = bugData.getBugList(cidList)
                    if bugDataDict == 1:
                        params = [3,0,'网络或服务器异常!']
                        self.trigger.emit(params)
                    else:
                        # 此时告知用户正在生成带图表的xlsx
                        params = [1,4,'正在生成带图表的xlsx...']
                        self.trigger.emit(params)
                        createXlsx = bugDataDict2xlsx(buglist=bugDataDict,filedir=self.filedir,ChartDATA=bugHistoryDict,closedFlag=self.closedFlag)
                        createXlsx.create_xlsxWithChart()
                        # 此时告知用户xlsx生成成功
                        params = [2,5,'xlsx生成成功,点击开始可再次生成']
                        self.trigger.emit(params)
        else:
            # 此时告知用户正在请求汇总bug下所有二级汇总bug的id
            params = [1,1,'正在请求汇总bug下所有二级汇总bug的id...']
            self.trigger.emit(params)
            aid = str(self.bugid)
            bugData = bug2xlsx_request()
            bidList = bugData.return_idList(aid)
            if bidList == '':
                params = [3,0,'汇总id下未发现挂靠分汇总id,请确认id是否正确!']
                self.trigger.emit(params)
            elif bidList == 1:
                params = [3,0,'网络或服务器异常!']
                self.trigger.emit(params)
            # elif len(bidList) > 10:
            #     j = 'wait'
            #     self.trigger2.emit(j)
            cidList = []
            i = 0
            for id in bidList:
                # 此时告知用户正在请求各二级汇总bug下所有bug的id
                params = [1,2,'正在请求第'+str(i+1)+'个(共'+str(len(bidList))+'个)二级汇总bug下所有bug的id...']
                self.trigger.emit(params)
                ccidList = bugData.return_idList(id)
                if ccidList == 1:
                    params = [3,0,'网络或服务器异常!']
                    self.trigger.emit(params)
                else:
                    cidList = cidList + ccidList
                    i = i + 1
            if cidList == []:
                params = [3,0,'分汇总id下未发现挂靠bug,请确认id是否正确!']
                self.trigger.emit(params)
            else:
                if self.drawChart == 0:
                    params = [1,3,'正在根据bugid请求buglist页...']
                    self.trigger.emit(params)
                    bugDataDict = bugData.getBugList(cidList)
                    if bugDataDict == 1:
                        params = [3,0,'网络或服务器异常!']
                        self.trigger.emit(params)
                    else:
                        # 此时告知用户正在生成无图表的xlsx
                        params = [1,4,'正在生成无图表的xlsx...']
                        self.trigger.emit(params)
                        createXlsx = bugDataDict2xlsx(buglist=bugDataDict,filedir=self.filedir,closedFlag=self.closedFlag)
                        createXlsx.create_xlsxNoChart()
                        # 此时告知用户xlsx生成成功
                        params = [2,5,'xlsx生成成功,点击开始可再次生成']
                        self.trigger.emit(params)
                else:
                    # 此时告知用户正在请求bug历史记录
                    params = [1,3,'正在根据bugid搜集bug历史记录...']
                    self.trigger.emit(params)
                    # 每个cid新建一个线程,每个线程负责取得每个cid对应bug的历史记录
                    # 每个线程的执行开始时间间隔1s
                    # 每个线程之间不需要互相等待,独立运行
                    # 主函数等待搜集的历史记录中记录数等于cid数量后继续执行
                    # 线程取得bug的历史记录后即刻添加至历史记录dict中
                    for cid in cidList:
                        threading.Thread(target=bugData.getBugHistory,args=(cid,)).start()
                        time.sleep(0.5)
                    while bugData.return_bugHistoryDictLens() < len(cidList):
                        time.sleep(1)
                    bugHistoryDict = bugData.return_bugHistoryDict()
                    # 此时告知用户正在请求buglist页
                    params = [1,4,'正在根据bugid请求buglist页...']
                    self.trigger.emit(params)
                    bugDataDict = bugData.getBugList(cidList)
                    if bugDataDict == 1:
                        params = [3,0,'网络或服务器异常!']
                        self.trigger.emit(params)
                    else:
                        # 此时告知用户正在生成无图表的xlsx
                        params = [1,5,'正在生成带图表的xlsx...']
                        self.trigger.emit(params)
                        createXlsx = bugDataDict2xlsx(buglist=bugDataDict,filedir=self.filedir,ChartDATA=bugHistoryDict,closedFlag=self.closedFlag)
                        createXlsx.create_xlsxWithChart()
                        # 此时告知用户xlsx生成成功
                        params = [2,6,'xlsx生成成功,点击开始可再次生成']
                        self.trigger.emit(params)


    def run(self):
        self.gogogo()



app = QtWidgets.QApplication(sys.argv)
bug2xlsx = bug2xlsx()
bug2xlsx.show()
sys.exit(app.exec_())
