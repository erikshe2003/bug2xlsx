# -*- coding: utf-8 -*-
__author__ = 'wufeng_wb'

import time, threading, re, os
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from packages.myRequests import bug2xlsx_request, bug2xlsx_request_ChanDao
from packages.data2xlsx import bugDataDict2xlsx
from packages.myWidgets import *

class errorWindow(QtWidgets.QDialog):
    def __init__(self):
        super(errorWindow, self).__init__()

    def initUI(self):
        # 设置QMainWindow属性
        self.setWindowTitle("error")
        self.setWindowIcon(QtGui.QIcon(':/icon02.ico'))
        # desk_width = app.desktop().width()
        # desk_height = app.desktop().height()
        win_width = 300
        win_height = 200
        self.setFixedWidth(win_width)
        self.setFixedHeight(win_height)
        # self.setGeometry((desk_width-desk_width%2)/2-(win_width-win_width%2)/2, (desk_height-desk_height%2)/2-(win_height-win_height%2)/2, win_width, win_height)
        # 去除系统边框
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

# 新建一个继承自QMainWindow的类,创建一个自定义的窗口
class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.outputMode = 0
        self.hasSubCategory = 0
        self.drawChart = 0
        self.type = 0
        self.productID = ''
        self.initUI()

    # 初始化界面
    def initUI(self):
        # 设置QMainWindow属性
        self.setWindowTitle("bug2xlsx")
        self.setWindowIcon(QtGui.QIcon(':/icon02.ico'))
        # desk_width = app.desktop().width()
        # desk_height = app.desktop().height()
        win_width = 480
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
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        # 新增一个QWidget,浮于Window上方,与Window等大。主要作用是背景
        self.main_widget = QtWidgets.QWidget(self)
        self.main_widget.setGeometry(0, 0, 480, 255)
        self.main_widget.setObjectName("main_widget")
        self.main_widget.setStyleSheet("#main_widget {background-image:url(:/shadow.png)}")
        # 新增一个最小化按钮,属于main_widget
        self.minWin_button = minButton(self)
        self.minWin_button.initStyle(enabled=True)
        self.minWin_button.setGeometry(386, 10, 42, 20)
        self.minWin_button.clicked.connect(self.showMinimized)
        # 新增一个关闭按钮,属于main_widget
        self.closeWin_button = closeButton(self)
        self.closeWin_button.initStyle(enabled=True)
        self.closeWin_button.setGeometry(428, 10, 42, 20)
        self.closeWin_button.clicked.connect(self.close)

        # 新增一个Qtab_widget
        self.tab_widget = QtWidgets.QTabWidget(self.main_widget)
        self.tab_widget.setGeometry(10, 10, 460, 230)
        self.tab_widget.setObjectName("tab_widget")
        # 如果不写::pane,会遗留左右下三条边框;如果使用setDocumentMode,会遗留上边框
        self.tab_widget.setStyleSheet("#tab_widget::pane {border:0}"
                                      "#tab_widget::tab-bar {left:24px}"
                                      )
        # 将tab_widget的tabBar命名为tab_widget_bar
        self.tab_widget.tabBar().setObjectName("tab_widget_bar")
        # self.tab_widget.setTabIcon()
        # self.tab_widget.tabBar().setStyleSheet("#tab_widget_bar::pane {left:20px}")
        # 去除变框比CSS样式的0px边框更加的彻底,但是有个问题,无法去掉上边框
        # self.tab_widget.setDocumentMode(True)
        # self.tab_widget.setTabPosition(2)

        # 新增第一个QWidget,隶属于Qtab_widget
        self.firstTab_widget = QtWidgets.QWidget(self.tab_widget)
        # self.icon01 = QtGui.QIcon(":/111.png")
        self.tab_widget.addTab(self.firstTab_widget, "   bug2xlsx")
        self.firstTab_widget.setObjectName("firstTab_widget")

        # 新增一个QTabWidget,隶属于firstTab_widget
        self.bug2xlsx_tabWidget = QtWidgets.QTabWidget(self.firstTab_widget)
        self.bug2xlsx_tabWidget.setGeometry(5, 0, 460, 230)
        self.bug2xlsx_tabWidget.setObjectName("bug2xlsx_tabWidget")
        # 如果不写::pane,会遗留左右下三条边框;如果使用setDocumentMode,会遗留上边框
        self.bug2xlsx_tabWidget.setStyleSheet("#bug2xlsx_tabWidget::pane {border:0}")
        # 将tab_widget的tabBar命名为tab_widget_bar
        self.bug2xlsx_tabWidget.tabBar().setObjectName("bug2xlsx_tabWidget_bar")
        self.bug2xlsx_tabWidget.setTabPosition(2)

        # 新增Bugzilla_tab,隶属于bug2xlsx_tabWidget
        self.Bugzilla_tab = QtWidgets.QWidget(self.bug2xlsx_tabWidget)
        # self.icon01 = QtGui.QIcon(":/111.png")
        self.bug2xlsx_tabWidget.addTab(self.Bugzilla_tab, "")
        self.Bugzilla_tab.setObjectName("Bugzilla")
        self.Bugzilla_tab.setStyleSheet("#Bugzilla {border:0;border-bottom-left-radius:4px;border-bottom-right-radius:4px;background-image:url(:/Bugzilla_widget.png)}")

        # 新增JIRA_tab,隶属于bug2xlsx_tabWidget
        self.JIRA_tab = QtWidgets.QWidget(self.bug2xlsx_tabWidget)
        # self.icon01 = QtGui.QIcon(":/111.png")
        self.bug2xlsx_tabWidget.addTab(self.JIRA_tab, "")
        self.JIRA_tab.setObjectName("JIRA")
        self.JIRA_tab.setStyleSheet("#JIRA {border:0;border-bottom-left-radius:4px;border-bottom-right-radius:4px;background-image:url(:/JIRA_widget.png)}")

        # 新增ChanDao_tab,隶属于bug2xlsx_tabWidget
        self.ChanDao_tab = QtWidgets.QWidget(self.bug2xlsx_tabWidget)
        # self.icon01 = QtGui.QIcon(":/111.png")
        self.bug2xlsx_tabWidget.addTab(self.ChanDao_tab, "")
        self.ChanDao_tab.setObjectName("ChanDao")
        self.ChanDao_tab.setStyleSheet("#ChanDao {border:0;border-bottom-left-radius:4px;border-bottom-right-radius:4px;background-image:url(:/ChanDao_widget.png)}")

        # 设置BUGID输入,隶属于Bugzilla_tab
        self.bugID_label = QtWidgets.QLabel(self.Bugzilla_tab)
        self.bugID_label.setText(u"输入汇总bug:")
        self.bugID_label.setObjectName("bugID_label")
        self.bugID_label.setStyleSheet("#bugID_label {font-family:微软雅黑;color:white;font-size:16px;}")
        self.bugID_label.setGeometry(10, 50, 105, 25)
        self.bugID_edit = QtWidgets.QLineEdit(self.Bugzilla_tab)
        self.bugID_edit.setObjectName("bugID_edit")
        self.bugID_edit.setStyleSheet(
            "#bugID_edit {font-family:微软雅黑;color:white;font-size:14px;padding-top:-2px;background-color:rgba(0,0,0,0.1);border-radius: 2px;border:1px solid lightgrey}")
        self.bugID_edit.setGeometry(119, 53, 80, 21)

        # 是否需要输出图表,隶属于Bugzilla_tab
        self.chart_label = QtWidgets.QLabel(self.Bugzilla_tab)
        self.chart_label.setText(u"是否输出图表:")
        self.chart_label.setObjectName("chart_label")
        self.chart_label.setStyleSheet("#chart_label {font-family:微软雅黑;color:white;font-size:16px;}")
        self.chart_label.setGeometry(212, 50, 110, 25)
        self.chart_group = QtWidgets.QWidget(self.Bugzilla_tab)
        self.chart_group.setGeometry(322, 49, 110, 30)
        self.chart_group.setObjectName("chart_group")
        # self.chart_group.setStyleSheet("#chart_group {font-family:微软雅黑;font-size:14px;}")
        self.chart01_radio = QtWidgets.QRadioButton(u'否', self.chart_group)
        self.chart01_radio.setObjectName("chart01_radio")
        self.chart01_radio.setStyleSheet(
            "#chart01_radio {font-family:微软雅黑;;color:white;font-size:13px;padding:4px;border:0;border-radius:7px;background-color:rgba(0,0,0,0.1)}")
        self.chart01_radio.setGeometry(0, 3, 45, 23)
        self.chart02_radio = QtWidgets.QRadioButton(u'是', self.chart_group)
        self.chart02_radio.setObjectName("chart02_radio")
        self.chart02_radio.setStyleSheet(
            "#chart02_radio {font-family:微软雅黑;;color:white;font-size:13px;padding:4px;border:0;border-radius:7px;background-color:rgba(0,0,0,0.1)}")
        self.chart02_radio.setGeometry(55, 3, 45, 23)

        # 创建两个个单选框,默认不选,隶属于Bugzilla_tab
        self.subCategory_label = QtWidgets.QLabel(u'二级汇总ID:', self.Bugzilla_tab)
        self.subCategory_label.setObjectName("subCategory_label")
        self.subCategory_label.setGeometry(10, 85, 100, 25)
        self.subCategory_label.setStyleSheet(
            "#subCategory_label {font-family:微软雅黑;color:white;font-size:16px;;border:0;border-radius:3px;background:rgba(0,0,0,0)}")
        # self.subCategory_label.setVisible(False)
        self.subCategory_group = QtWidgets.QWidget(self.Bugzilla_tab)
        self.subCategory_group.setGeometry(104, 84, 110, 30)
        # self.subCategory_group.setVisible(False)
        self.subCategory_group.setObjectName("chart_group")
        self.subCategory01_radio = QtWidgets.QRadioButton(u'无', self.subCategory_group)
        self.subCategory01_radio.setObjectName("subCategory01_radio")
        self.subCategory01_radio.setGeometry(0, 3, 45, 23)
        self.subCategory01_radio.setStyleSheet(
            "#subCategory01_radio {font-family:微软雅黑;;color:white;font-size:13px;padding:4px;border:0;border-radius:7px;background-color:rgba(0,0,0,0.1)}")
        self.subCategory02_radio = QtWidgets.QRadioButton(u'有', self.subCategory_group)
        self.subCategory02_radio.setObjectName("subCategory02_radio")
        self.subCategory02_radio.setGeometry(55, 3, 45, 23)
        self.subCategory02_radio.setStyleSheet(
            "#subCategory02_radio {font-family:微软雅黑;;color:white;font-size:13px;padding:4px;border:0;border-radius:7px;background-color:rgba(0,0,0,0.1)}")

        # 创建关闭问题单标识,隶属于Bugzilla_tab
        self.closedBug_label = QtWidgets.QLabel(self.Bugzilla_tab)
        self.closedBug_label.setText(u"BUG关闭标识:")
        self.closedBug_label.setObjectName("closedBug_label")
        self.closedBug_label.setStyleSheet("#closedBug_label {font-family:微软雅黑;font-size:16px;color:white;}")
        self.closedBug_label.setGeometry(214, 85, 105, 25)
        # self.closedBug_label.setVisible(False)
        self.closedBug_flag = QtWidgets.QComboBox(self.Bugzilla_tab)
        self.closedBug_flag.setObjectName("closedBug_flag")
        self.closedBug_flag.addItem("       VERI")
        self.closedBug_flag.addItem("       CLOS")
        self.closedBug_flag.setGeometry(323, 88, 100, 21)
        self.closedBug_flag.setStyleSheet(
            "#closedBug_flag {font-family:微软雅黑;;color:white;font-size:13px;padding:4px;border:0;border-radius:2px;background-color:rgba(0,0,0,0.1)} #closedBug_flag::drop-down{border:0} #closedBug_flag::down-arrow{margin-left:-10px;width:16px;height:16px;background-image:url(:/down_arrow.png)}")
        # self.closedBug_flag.setVisible(False)
        # self.comboBox.setItemText(0, _translate("Form", "新111"))
        # self.comboBox.setItemText(1, _translate("Form", "新建22"))

        # 创建一个文件夹路径部件标题Label,隶属于Bugzilla_tab
        self.chooseDir_label = QtWidgets.QLabel(u'xlsx保存路径:', self.Bugzilla_tab)
        self.chooseDir_label.setObjectName("chooseDir_label")
        self.chooseDir_label.setGeometry(13, 120, 110, 20)
        self.chooseDir_label.setStyleSheet("#chooseDir_label {font-family:微软雅黑;color:white;;font-size:16px;}")
        # 创建一个文件夹路径展示LineEdit
        self.chooseDir_edit = QtWidgets.QLineEdit(self.Bugzilla_tab)
        self.chooseDir_edit.setObjectName("chooseDir_edit")
        self.chooseDir_edit.setStyleSheet(
            "#chooseDir_edit {font-family:微软雅黑;font-size:14px;background-color:rgba(0,0,0,0.1);border-radius: 2px;border:1px solid lightgrey}")
        self.chooseDir_edit.setEnabled(False)
        self.chooseDir_edit.setGeometry(120, 122, 260, 21)
        # 创建一个文件夹选择Button
        self.chooseDir_button = chooseButton('....', self.Bugzilla_tab)
        self.chooseDir_button.setObjectName("chooseDir_button")
        self.chooseDir_button.setGeometry(390, 122, 35, 21)
        self.chooseDir_button.initStyle(enabled=True)
        self.chooseDir_button.clicked.connect(self.do_chooseDir_button)

        # 创建一个按钮,隶属于Bugzilla_tab
        self.enter_button = startButton('开始', self.Bugzilla_tab)
        # self.enter_button.setObjectName("enter_button")
        self.enter_button.setGeometry(345, 157, 80, 20)
        self.enter_button.initStyle(enabled=True)
        # self.enter_button.setStyleSheet("QPushButton{background-image:url(:/icon.ico);}")
        self.enter_button.clicked.connect(self.processMode)
        # self.enter_button.clicked.connect(self.test)

        # 创建内容验证后输出Label,隶属于Bugzilla_tab
        self.prompt_label = QtWidgets.QLabel(self.Bugzilla_tab)
        self.prompt_label.setObjectName("prompt_label")
        # label长度自适应
        # self.prompt_label.adjustSize()
        # label自动换行
        # self.prompt_label.setWordWrap(True)
        # 文字居中
        self.prompt_label.setAlignment(QtCore.Qt.AlignCenter)
        # self.prompt_label.setStyleSheet("#prompt_label {font-size:4px}")
        self.prompt_label.setGeometry(20, 176, 400, 20)

        # 创建一个进度条,隶属于Bugzilla_tab
        self.theBar_progress = QtWidgets.QProgressBar(self.Bugzilla_tab)
        self.theBar_progress.setObjectName("theBar_progress")
        self.theBar_progress.setStyleSheet(
            "#theBar_progress {border: 1px solid lightgrey;border-radius: 3px;background-color: #FFFFFF;} QProgressBar::chunk {background-color:#92B827;width: 20px}")
        self.theBar_progress.setGeometry(2, 197, 431, 6)
        self.theBar_progress.setMinimum(0)
        self.theBar_progress.setMaximum(3)
        self.theBar_progress.setTextVisible(False)
        self.theBar_progress.setVisible(False)

        # 输入相关任务or相关需求ID,隶属于ChanDao_tab
        self.missionId_flag = QtWidgets.QComboBox(self.ChanDao_tab)
        self.missionId_flag.setObjectName("missionId_flag")
        self.missionId_flag.addItem("相关任务ID:")
        self.missionId_flag.addItem("相关需求ID:")
        self.missionId_flag.setGeometry(10, 9, 110, 27)
        self.missionId_flag.setStyleSheet("#missionId_flag {font-family:微软雅黑;white;font-size:16px;padding:4px;border:1px solid lightgrey;border-radius:2px;background-color:rgba(0,0,0,0)} #missionId_flag::drop-down{top:1px;border:0} #missionId_flag::down-arrow{margin-left:-10px;width:16px;height:16px;background-image:url(:/down_arrow.png)}")
        self.missionId_edit = QtWidgets.QLineEdit(self.ChanDao_tab)
        self.missionId_edit.setObjectName("missionId_edit")
        self.missionId_edit.setStyleSheet(
            "#missionId_edit {font-family:微软雅黑;font-size:14px;padding-top:-2px;background-color:rgba(0,0,0,0.1);border-radius: 2px;border:1px solid lightgrey}")
        self.missionId_edit.setGeometry(125, 13, 80, 21)

        # 创建一个文件夹路径部件标题Label,隶属于Bugzilla_tab
        self.product_label = QtWidgets.QLabel(u'请选择产品:', self.ChanDao_tab)
        self.product_label.setObjectName("product_label")
        self.product_label.setGeometry(230, 12, 110, 20)
        self.product_label.setStyleSheet("#product_label {font-family:微软雅黑;font-size:16px;}")
        # 选择齐玩产品or游戏SDK,隶属于ChanDao_tab
         # self.closedBug_label.setVisible(False)
        self.product_flag = QtWidgets.QComboBox(self.ChanDao_tab)
        self.product_flag.setObjectName("product_flag")
        self.product_flag.addItem("    齐玩产品")
        self.product_flag.addItem("    游戏SDK")
        self.product_flag.setGeometry(323, 13, 100, 21)
        self.product_flag.setStyleSheet(
            "#product_flag {font-family:微软雅黑;font-size:13px;padding:4px;border:0;border-radius:2px;background-color:rgba(0,0,0,0.1)} #product_flag::drop-down{border:0} #product_flag::down-arrow{margin-left:-10px;width:16px;height:16px;background-image:url(:/down_arrow.png)}")

        # 创建一个文件夹路径部件标题Label,隶属于ChanDao_tab
        self.chooseDir_label3 = QtWidgets.QLabel(u'xlsx保存路径:', self.ChanDao_tab)
        self.chooseDir_label3.setObjectName("chooseDir_label3")
        self.chooseDir_label3.setGeometry(13, 45, 110, 20)
        self.chooseDir_label3.setStyleSheet("#chooseDir_label3 {font-family:微软雅黑;font-size:16px;}")
        # 创建一个文件夹路径展示LineEdit,隶属于ChanDao_tab
        self.chooseDir_edit3 = QtWidgets.QLineEdit(self.ChanDao_tab)
        self.chooseDir_edit3.setObjectName("chooseDir_edit3")
        self.chooseDir_edit3.setStyleSheet(
            "#chooseDir_edit3 {font-family:微软雅黑;font-size:14px;background-color:rgba(0,0,0,0.1);border-radius: 2px;border:1px solid lightgrey}")
        self.chooseDir_edit3.setEnabled(False)
        self.chooseDir_edit3.setGeometry(119, 46, 260, 21)
        # 创建一个文件夹选择Button,隶属于ChanDao_tab
        self.chooseDir_button3 = chooseButton('....', self.ChanDao_tab)
        self.chooseDir_button3.setObjectName("chooseDir_button3")
        self.chooseDir_button3.setGeometry(390, 46, 35, 21)
        self.chooseDir_button3.initStyle(enabled=True)
        self.chooseDir_button3.clicked.connect(self.do_chooseDir_button)

        # 创建一个按钮,隶属于ChanDao_tab
        self.enter_button3 = startButton('开始', self.ChanDao_tab)
        # self.enter_button.setObjectName("enter_button")
        self.enter_button3.setGeometry(345, 157, 80, 20)
        self.enter_button3.initStyle(enabled=True)
        # self.enter_button.setStyleSheet("QPushButton{background-image:url(:/icon.ico);}")
        self.enter_button3.clicked.connect(self.processMode)
        # self.enter_button.clicked.connect(self.test)

        # 创建内容验证后输出Label,隶属于ChanDao_tab
        self.prompt_label3 = QtWidgets.QLabel(self.ChanDao_tab)
        self.prompt_label3.setObjectName("prompt_label3")
        # label长度自适应
        # self.prompt_label.adjustSize()
        # label自动换行
        # self.prompt_label.setWordWrap(True)
        # 文字居中
        self.prompt_label3.setAlignment(QtCore.Qt.AlignCenter)
        # self.prompt_label.setStyleSheet("#prompt_label {font-size:4px}")
        self.prompt_label3.setGeometry(20, 176, 400, 20)

        # 创建一个进度条,隶属于ChanDao_tab
        self.theBar_progress3 = QtWidgets.QProgressBar(self.ChanDao_tab)
        self.theBar_progress3.setObjectName("theBar_progress3")
        self.theBar_progress3.setStyleSheet(
            "#theBar_progress3 {border: 1px solid lightgrey;border-radius: 3px;background-color: #FFFFFF;} QProgressBar3::chunk {background-color:#92B827;width: 20px}")
        self.theBar_progress3.setGeometry(2, 197, 431, 6)
        self.theBar_progress3.setMinimum(0)
        self.theBar_progress3.setMaximum(3)
        self.theBar_progress3.setTextVisible(False)
        self.theBar_progress3.setVisible(False)

        # 新增第二个QWidget,隶属于Qtab_widget
        self.secondTab_widget = QtWidgets.QWidget(self.tab_widget)
        self.tab_widget.addTab(self.secondTab_widget, "  settings")
        self.secondTab_widget.setObjectName("secondTab_widget")
        self.secondTab_widget.setStyleSheet(
            "#secondTab_widget {border:0;border-bottom-left-radius:4px;border-bottom-right-radius:4px;background-image:url(:/settings.png)}")
        # bugzilla
        self.bugzilla_label = QtWidgets.QLabel(self.secondTab_widget)
        self.bugzilla_label.setText(u"bugzilla账户配置:")
        self.bugzilla_label.setObjectName("bugzilla_label")
        self.bugzilla_label.setStyleSheet("#bugzilla_label {font-family:微软雅黑;color:black;font-size:16px;}")
        self.bugzilla_label.setGeometry(35, 5, 145, 25)
        # 设置username输入
        self.bugzilla_username_label = QtWidgets.QLabel(self.secondTab_widget)
        self.bugzilla_username_label.setText(u"用户名:")
        self.bugzilla_username_label.setObjectName("bugzilla_username_label")
        self.bugzilla_username_label.setStyleSheet("#bugzilla_username_label {font-family:微软雅黑;color:black;font-size:16px;}")
        self.bugzilla_username_label.setGeometry(35, 35, 105, 25)
        self.bugzilla_username_edit = QtWidgets.QLineEdit(self.secondTab_widget)
        self.bugzilla_username_edit.setObjectName("bugzilla_username_edit")
        self.bugzilla_username_edit.setStyleSheet(
            "#bugzilla_username_edit {font-family:微软雅黑;color:black;font-size:14px;padding-top:-2px;background-color:rgba(0,0,0,0.1);border-radius: 2px;border:1px solid lightgrey}")
        self.bugzilla_username_edit.setGeometry(100, 39, 120, 21)
        # 设置passwd输入
        self.bugzilla_passwd_label = QtWidgets.QLabel(self.secondTab_widget)
        self.bugzilla_passwd_label.setText(u"密码:")
        self.bugzilla_passwd_label.setObjectName("bugzilla_passwd_label")
        self.bugzilla_passwd_label.setStyleSheet("#bugzilla_passwd_label {font-family:微软雅黑;color:black;font-size:16px;}")
        self.bugzilla_passwd_label.setGeometry(51, 65, 105, 25)
        self.bugzilla_passwd_edit = QtWidgets.QLineEdit(self.secondTab_widget)
        self.bugzilla_passwd_edit.setObjectName("bugzilla_passwd_edit")
        self.bugzilla_passwd_edit.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.bugzilla_passwd_edit.setStyleSheet(
            "#bugzilla_passwd_edit {font-family:微软雅黑;color:black;font-size:14px;padding-top:-2px;background-color:rgba(0,0,0,0.1);border-radius: 2px;border:1px solid lightgrey}")
        self.bugzilla_passwd_edit.setGeometry(100, 69, 120, 21)
        # 创建一个按钮
        self.save_button = startButton('保存', self.secondTab_widget)
        self.save_button.setGeometry(370, 167, 80, 20)
        self.save_button.initStyle(enabled=True)
        self.save_button.clicked.connect(self.save_userinfo)
        # 创建内容验证后输出Label
        self.settings_prompt_label = QtWidgets.QLabel(self.secondTab_widget)
        self.settings_prompt_label.setObjectName("settings_prompt_label")
        self.settings_prompt_label.setAlignment(QtCore.Qt.AlignCenter)
        self.settings_prompt_label.setGeometry(40, 176, 400, 20)
        # 禅道
        self.chandao_label = QtWidgets.QLabel(self.secondTab_widget)
        self.chandao_label.setText(u"禅道账户配置:")
        self.chandao_label.setObjectName("chandao_label")
        self.chandao_label.setStyleSheet("#chandao_label {font-family:微软雅黑;color:black;font-size:16px;}")
        self.chandao_label.setGeometry(235, 5, 145, 25)
        # 设置username输入
        self.chandao_username_label = QtWidgets.QLabel(self.secondTab_widget)
        self.chandao_username_label.setText(u"用户名:")
        self.chandao_username_label.setObjectName("chandao_username_label")
        self.chandao_username_label.setStyleSheet(
            "#chandao_username_label {font-family:微软雅黑;color:black;font-size:16px;}")
        self.chandao_username_label.setGeometry(235, 35, 105, 25)
        self.chandao_username_edit = QtWidgets.QLineEdit(self.secondTab_widget)
        self.chandao_username_edit.setObjectName("chandao_username_edit")
        self.chandao_username_edit.setStyleSheet(
            "#chandao_username_edit {font-family:微软雅黑;color:black;font-size:14px;padding-top:-2px;background-color:rgba(0,0,0,0.1);border-radius: 2px;border:1px solid lightgrey}")
        self.chandao_username_edit.setGeometry(300, 39, 120, 21)
        # 设置passwd输入
        self.chandao_passwd_label = QtWidgets.QLabel(self.secondTab_widget)
        self.chandao_passwd_label.setText(u"密码:")
        self.chandao_passwd_label.setObjectName("chandao_passwd_label")
        self.chandao_passwd_label.setStyleSheet(
            "#chandao_passwd_label {font-family:微软雅黑;color:black;font-size:16px;}")
        self.chandao_passwd_label.setGeometry(251, 65, 105, 25)
        self.chandao_passwd_edit = QtWidgets.QLineEdit(self.secondTab_widget)
        self.chandao_passwd_edit.setObjectName("chandao_passwd_edit")
        self.chandao_passwd_edit.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.chandao_passwd_edit.setStyleSheet(
            "#chandao_passwd_edit {font-family:微软雅黑;color:black;font-size:14px;padding-top:-2px;background-color:rgba(0,0,0,0.1);border-radius: 2px;border:1px solid lightgrey}")
        self.chandao_passwd_edit.setGeometry(300, 69, 120, 21)
        # 创建一个按钮
        self.save_button = startButton('保存', self.secondTab_widget)
        self.save_button.setGeometry(370, 167, 80, 20)
        self.save_button.initStyle(enabled=True)
        self.save_button.clicked.connect(self.save_userinfo)
        # 创建内容验证后输出Label
        self.settings_prompt_label = QtWidgets.QLabel(self.secondTab_widget)
        self.settings_prompt_label.setObjectName("settings_prompt_label")
        self.settings_prompt_label.setAlignment(QtCore.Qt.AlignCenter)
        self.settings_prompt_label.setGeometry(40, 176, 400, 20)
        config = open('config.txt', mode='r', encoding='utf-8')
        for i in config.readlines():
            if i[0] == '#':
                pass
            else:
                if i.startswith('username=') == True:
                    try:
                        username = re.match('username=(.+)', i).group(1)
                        self.bugzilla_username_edit.setText(username)
                    except Exception as e:
                        pass
                if i.startswith('passwd=') == True:
                    try:
                        passwd = re.match('passwd=(.+)', i).group(1)
                        self.bugzilla_passwd_edit.setText(passwd)
                    except Exception as e:
                        pass
                if i.startswith('cusername=') == True:
                    try:
                        cusername = re.match('cusername=(.+)', i).group(1)
                        self.chandao_username_edit.setText(cusername)
                    except Exception as e:
                        pass
                if i.startswith('cpasswd=') == True:
                    try:
                        cpasswd = re.match('cpasswd=(.+)', i).group(1)
                        self.chandao_passwd_edit.setText(cpasswd)
                    except Exception as e:
                        pass
        config.close()

        # 新增第三个QWidget,隶属于Qtab_widget
        self.thirdTab_widget = QtWidgets.QWidget(self.tab_widget)
        self.tab_widget.addTab(self.thirdTab_widget, "  ?-_-help")
        self.thirdTab_widget.setObjectName("thirdTab_widget")
        self.thirdTab_widget.setStyleSheet(
            "#thirdTab_widget {border:0;border-bottom-left-radius:4px;border-bottom-right-radius:4px;background-image:url(:/help.png)}")
        # 多次设定styleSheet会只去最后一个,所以一次性设定
        self.tab_widget.tabBar().setStyleSheet(
            "#tab_widget_bar::tab {color:white;font-family:Arial;font-size:15px;font-weight:900;background-image:url(:/tabWidgetTab_selected.png);position:absolute;width:85px;height:25px;border-radius:3px}"
            "#tab_widget_bar::tab::selected {border:0;}"
            "#tab_widget_bar::tab::!selected {background-image:url(:/tabWidgetTab_!selected.png);border:0;}"
            # "#tab_widget_bar::tab::first {margin-left:20px;background-image:url(:/bug2xlsxTab_selected.png);position:absolute;left:5px;width:80px;height:25px;border-radius:3px}"
            # "#tab_widget_bar::tab::first::selected {margin-left:20px;top:3px;border:0;}"
            # "#tab_widget_bar::tab::first::!selected {margin-left:20px;background-image:url(:/bug2xlsxTab_!selected.png);top:6px;border:0;}"
            # "#tab_widget_bar::tab::last {background-image:url(:/helpTab_selected.png);left:1px;width:80px;height:25px;border-radius:3px}"
            # "#tab_widget_bar::tab::last::selected {top:3px;border:0;}"
            # "#tab_widget_bar::tab::last::!selected {background-image:url(:/helpTab_!selected.png);top:6px;border:0;}"
        )
        # self.tab_widget.setTabIcon(self, 1, QIcon=QtGui.QIcon())
        self.bug2xlsx_tabWidget.tabBar().setStyleSheet(
            # "bug2xlsx_tabWidget_bar"
            "#bug2xlsx_tabWidget_bar::tab::first {width:20px;height:50px;}"
            "#bug2xlsx_tabWidget_bar::tab::first::selected {background-image:url(:/BugzillaTab_selected.png);border:0;}"
            "#bug2xlsx_tabWidget_bar::tab::first::!selected {background-image:url(:/BugzillaTab_!selected.png);border:0;}"
            "#bug2xlsx_tabWidget_bar::tab::middle {width:20px;height:50px;}"
            "#bug2xlsx_tabWidget_bar::tab::middle::selected {background-image:url(:/JIRATab_selected.png);border:0;}"
            "#bug2xlsx_tabWidget_bar::tab::middle::!selected {background-image:url(:/JIRATab_!selected.png);border:0;}"
            "#bug2xlsx_tabWidget_bar::tab::last {width:20px;height:50px;}"
            "#bug2xlsx_tabWidget_bar::tab::last::selected {background-image:url(:/ChanDaoTab_selected.png);border:0;}"
            "#bug2xlsx_tabWidget_bar::tab::last::!selected {background-image:url(:/ChanDaoTab_!selected.png);border:0;}"
        )
        # 帮助信息
        # self.helpImfor = QtWidgets.QWidget(self.thirdTab_widget)
        # self.helpImfor.setObjectName("helpImfor")
        # self.helpImfor.setGeometry(20,15,200,110)
        # self.helpImfor.setStyleSheet("#helpImfor {background-color:rgba(0,0,0,0);border:0;border-radius:3px}")
        self.intro_edit = QtWidgets.QTextEdit(self.thirdTab_widget)
        self.intro_edit.setGeometry(40, 15, 215, 70)
        self.intro_edit.setObjectName("intro_edit")
        self.intro_edit.setText("    写这个工具一是为了提高工作效率,二是写着玩.本工具会不定期更新功能,更新后会立刻通知大家哦~")
        self.intro_edit.setStyleSheet(
            "#intro_edit {color:white;font-family:微软雅黑;font-size:13px;background-color:rgba(0,0,0,0.12);border-radius:3px}")
        self.intro_edit.setEnabled(False)
        self.contact_label = QtWidgets.QTextEdit(self.thirdTab_widget)
        self.contact_label.setGeometry(40, 95, 215, 65)
        self.contact_label.setObjectName("contact_label")
        self.contact_label.setStyleSheet(
            "#contact_label {;color:white;font-family:微软雅黑;font-size:13px;background-color:rgba(0,0,0,0.12);border-radius:3px}")
        self.contact_label.setText("                   联系方式:\n企鹅852353148\n邮箱wufeng_wb@qiyi.com")
        self.contact_label.setEnabled(False)

        # self.tab_widget.setEnabled()


    # 获取文件保存地址
    def do_chooseDir_button(self):
        if self.sender() == self.chooseDir_button:
            filedir = QtWidgets.QFileDialog.getExistingDirectory()
            if filedir:
                filedir = filedir + "/"
                self.chooseDir_edit.setText(filedir)
            else:
                self.chooseDir_edit.setText(filedir)
        elif self.sender() == self.chooseDir_button3:
            filedir = QtWidgets.QFileDialog.getExistingDirectory()
            if filedir:
                filedir = filedir + "/"
                self.chooseDir_edit3.setText(filedir)
            else:
                self.chooseDir_edit3.setText(filedir)

    # 有空研究一下原理
    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.LeftButton):
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            # QtWidgets.QApplication.postEvent(self, QtCore.QEvent(1))
            event.accept()
            # if(event.button() == QtCore.Qt.RightButton):
            #     print('111')

    # 有空研究一下原理
    def mouseMoveEvent(self, event):
        if (event.buttons() == QtCore.Qt.LeftButton):
            # print(event.globalPos())
            try:
                self.move(event.globalPos() - self.dragPosition)
            except Exception as e:
                print(e)
            event.accept()

    def processMode(self):
        if self.sender() == self.enter_button:
            # 0代表按照Bugzilla的规则来
            self.outputMode = 0
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
                        self.prompt_label.setStyleSheet("#prompt_label {font-family:微软雅黑;;font-size:16px;color:#FF4D4D}")
                        self.prompt_label.setText(u"是否输出图表?")
                else:
                    self.prompt_label.setStyleSheet("#prompt_label {font-family:微软雅黑;;font-size:16px;color:#FF4D4D}")
                    self.prompt_label.setText(u"是否存在二级分类?")
            else:
                self.prompt_label.setStyleSheet("#prompt_label {font-family:微软雅黑;;font-size:16px;color:#FF4D4D}")
                self.prompt_label.setText(u"请输入正确的数字ID!")
        elif self.sender() == self.enter_button3:
            # 判断产品
            if self.product_flag.currentText() == "    齐玩产品":
                self.productID = 1
            elif self.product_flag.currentText() == "    游戏SDK":
                self.productID = 6
            # 2代表按照ChanDao的规则来
            self.outputMode = 2
            if self.missionId_flag.currentText() == "相关任务ID:":
                self.type = 0
                if self.missionId_edit.text().isdigit() == True:
                    self.hasSubCategory = 0
                    self.drawChart = 1
                    self.theBar_progress3.setMaximum(5)
                    self.createThread()
                else:
                    self.prompt_label3.setStyleSheet("#prompt_label3 {font-family:微软雅黑;;font-size:16px;color:#FF4D4D}")
                    self.prompt_label3.setText(u"请输入正确的相关任务ID!")
            elif self.missionId_flag.currentText() == "相关需求ID:":
                self.type = 1
                if self.missionId_edit.text().isdigit() == True:
                    # 生成图表
                    self.hasSubCategory = 0
                    self.drawChart = 1
                    self.theBar_progress3.setMaximum(5)
                    self.createThread()
                else:
                    self.prompt_label3.setStyleSheet("#prompt_label3 {font-family:微软雅黑;;font-size:16px;color:#FF4D4D}")
                    self.prompt_label3.setText(u"请输入正确的相关需求ID!")

    # 进度条状态
    def theBar_display(self, params):
        if self.outputMode == 0:
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
                self.tab_widget.setEnabled(False)
                self.bug2xlsx_tabWidget.setEnabled(False)
                # 告知用户任务马上开始,放开进度栏的展示
                self.prompt_label.setStyleSheet("#prompt_label {font-family:微软雅黑;;font-size:15px;color:#92B827}")
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
                self.bug2xlsx_tabWidget.setEnabled(True)
                self.tab_widget.setEnabled(True)
            elif params[0] == 3:
                self.doThread.terminate()
                self.prompt_label.setStyleSheet("#prompt_label {font-family:微软雅黑;;font-size:15px;color:#FF4D4D}")
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
                self.theBar_progress.setVisible(False)
                self.bug2xlsx_tabWidget.setEnabled(True)
                self.tab_widget.setEnabled(True)
        elif self.outputMode == 2:
            # status为0即为任务开始状态,需要禁用页面上所有按钮/复选框/输入框,需要给出文字提示,且设定进度条
            if params[0] == 0:
                self.minWin_button.initStyle(enabled=False)
                self.minWin_button.setEnabled(False)
                self.closeWin_button.initStyle(enabled=False)
                self.closeWin_button.setEnabled(False)
                self.missionId_edit.setEnabled(False)
                self.missionId_flag.setEnabled(False)
                self.chooseDir_button3.initStyle(enabled=False)
                self.chooseDir_button3.setEnabled(False)
                self.enter_button3.setText('请稍候')
                self.enter_button3.initStyle(enabled=False)
                self.enter_button3.setEnabled(False)
                self.tab_widget.setEnabled(False)
                self.bug2xlsx_tabWidget.setEnabled(False)
                # 告知用户任务马上开始,放开进度栏的展示
                self.prompt_label3.setStyleSheet("#prompt_label3 {font-family:微软雅黑;;font-size:15px;color:#92B827}")
                self.prompt_label3.setText(params[2])
                self.theBar_progress3.setValue(params[1])
                self.theBar_progress3.setVisible(True)
            # status为1即任务进行中,需要给出文字提示,且设定进度条
            elif params[0] == 1:
                self.prompt_label3.setText(params[2])
                self.theBar_progress3.setValue(params[1])
            # status为2即任务进行执行成功,需要启用页面上所有按钮/复选框/输入框,需要给出文字提示,且设定进度条
            elif params[0] == 2:
                self.prompt_label3.setText(params[2])
                self.theBar_progress3.setValue(params[1])
                # 启用页面上所有按钮/复选框/输入框
                self.minWin_button.initStyle(enabled=True)
                self.minWin_button.setEnabled(True)
                self.closeWin_button.initStyle(enabled=True)
                self.closeWin_button.setEnabled(True)
                self.missionId_edit.setEnabled(True)
                self.missionId_flag.setEnabled(True)
                self.chooseDir_button3.initStyle(enabled=True)
                self.chooseDir_button3.setEnabled(True)
                self.enter_button3.setText('再次开始')
                self.enter_button3.initStyle(enabled=True)
                self.enter_button3.setEnabled(True)
                self.bug2xlsx_tabWidget.setEnabled(True)
                self.tab_widget.setEnabled(True)
            elif params[0] == 3:
                self.doThread.terminate()
                self.prompt_label3.setStyleSheet("#prompt_label3 {font-family:微软雅黑;;font-size:15px;color:#FF4D4D}")
                self.prompt_label3.setText(params[2])
                self.theBar_progress3.setValue(params[1])
                # 启用页面上所有按钮/复选框/输入框
                self.minWin_button.initStyle(enabled=True)
                self.minWin_button.setEnabled(True)
                self.closeWin_button.initStyle(enabled=True)
                self.closeWin_button.setEnabled(True)
                self.missionId_edit.setEnabled(True)
                self.missionId_flag.setEnabled(True)
                self.chooseDir_button3.initStyle(enabled=True)
                self.chooseDir_button3.setEnabled(True)
                self.enter_button3.setText('再次开始')
                self.enter_button3.initStyle(enabled=True)
                self.enter_button3.setEnabled(True)
                self.theBar_progress3.setVisible(False)
                self.bug2xlsx_tabWidget.setEnabled(True)
                self.tab_widget.setEnabled(True)

    # 新建信息收集与处理线程
    def createThread(self):
        bugID = 0
        fileDIR = ""
        if self.outputMode == 0:
            bugID = self.bugID_edit.text()
            fileDIR = self.chooseDir_edit.text()
        elif self.outputMode == 2:
            bugID = self.missionId_edit.text()
            fileDIR = self.chooseDir_edit3.text()
        self.doThread = thread(mode=self.outputMode, bugid=bugID, filedir=fileDIR, drawChart=self.drawChart,
                               closedFlag=self.closedBug_flag.currentText(), hasSubCategory=self.hasSubCategory,type=self.type,productID=self.productID)
        self.doThread.trigger.connect(self.theBar_display)
        self.doThread.trigger2.connect(self.stop_or_continue)
        self.doThread.start()

    def save_userinfo(self):
        username = self.bugzilla_username_edit.text()
        passwd = self.bugzilla_passwd_edit.text()
        cusername = self.chandao_username_edit.text()
        cpasswd = self.chandao_passwd_edit.text()
        config = open('config.txt', mode='w', encoding='utf-8')
        config.write(
            '#配置bugzilla用户名\nusername=' + username + '\n#配置bugzilla用户密码\npasswd=' + passwd + '\n#配置禅道用户名\ncusername=' + cusername + '\n#配置禅道用户密码\ncpasswd=' + cpasswd)
        message = '保存成功!'
        config.close()
        self.settings_prompt_label.setStyleSheet("#settings_prompt_label {font-family:微软雅黑;;font-size:16px;color:#FF4D4D}")
        self.settings_prompt_label.setText(message)


    def stop_or_continue(self, j):
        if j == 'wait':
            ccc = QtCore.QWaitCondition()
            self.doThread.wait()
            reply = QtWidgets.QMessageBox.question(self, '那啥', '检测到当前一级汇总ID下存在大于十个的二级汇总ID,确定要继续？',
                                                   QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                                                   QtWidgets.QMessageBox.Ok)
            if reply == QtWidgets.QMessageBox.Ok:
                self.doThread.wait(1)
            elif reply == QtWidgets.QMessageBox.Cancel or reply == QtWidgets.QMessageBox.close:
                params = [3, 0, '任务已终止!']
                self.theBar_display(params)


    def test(self):
        print(self.closedBug_flag.currentText())

# 任务线程
class thread(QtCore.QThread):
    trigger = QtCore.pyqtSignal(list)
    trigger2 = QtCore.pyqtSignal(str)


    def __init__(self, mode, bugid, filedir, drawChart, closedFlag, hasSubCategory, type, productID=None):
        super(thread, self).__init__()
        self.mode = mode
        self.bugid = bugid
        self.filedir = filedir
        self.hasSubCategory = hasSubCategory
        self.drawChart = drawChart
        self.closedFlag = closedFlag
        self.type = type
        if productID == '':
            pass
        else:
            self.productID = productID

    # 执行
    def gogogo(self):
        # errorWindow.exec()
        if self.mode == 0:
            # j = 'wait'
            # self.trigger2.emit(j)
            # 程序已准备好,告诉用户任务马上开始
            params = [0, 0, '任务马上开始,请稍候...']
            self.trigger.emit(params)
            time.sleep(1)
            # 判断是否有二级,若无二级,则告知用户即将请求汇总bug下的所有bug的id并生成为列表以供使用;
            # 若有二级,则告知用户首先需要请求汇总bug下的各二级汇总bug的id;
            if self.hasSubCategory == 0:
                # 此时告知用户正在请求汇总bug下所有bug的id
                params = [1, 1, '正在请求汇总bug下所有bug的id...']
                self.trigger.emit(params)
                aid = str(self.bugid)
                bugData = bug2xlsx_request()
                # 预登录取cookie
                login_result = bugData.login_getCookie()
                if login_result == 2:
                    params = [3, 0, '请先配置账号信息!']
                    self.trigger.emit(params)
                elif login_result == 1:
                    params = [3, 0, '账号名或密码错误!']
                    self.trigger.emit(params)
                else:
                    cidList = bugData.return_idList(aid)
                    if cidList == []:
                        params = [3, 0, '汇总id下未发现挂靠BUG,请确认id是否正确!']
                        self.trigger.emit(params)
                    elif cidList == 1:
                        params = [3, 0, '网络或服务器异常!']
                        self.trigger.emit(params)
                    else:
                        if self.drawChart == 0:
                            # 此时告知用户正在请求buglist页
                            params = [1, 2, '正在根据bugid请求buglist页...']
                            self.trigger.emit(params)
                            bugDataDict = bugData.getBugList(cidList)
                            if bugDataDict == 1:
                                params = [3, 0, '网络或服务器异常!']
                                self.trigger.emit(params)
                            else:
                                # 此时告知用户正在生成无图表的xlsx
                                params = [1, 3, '正在生成无图表的xlsx...']
                                self.trigger.emit(params)
                                createXlsx = bugDataDict2xlsx(mode=0,buglist=bugDataDict, filedir=self.filedir,
                                                              closedFlag=self.closedFlag)
                                createXlsx.create_xlsxNoChart()
                                # 此时告知用户xlsx生成成功
                                params = [2, 4, 'xlsx生成成功,点击开始可再次生成']
                                self.trigger.emit(params)
                        else:
                            # 此时告知用户正在请求bug历史记录
                            params = [1, 2, '正在根据bugid搜集bug历史记录...']
                            self.trigger.emit(params)
                            # 每个cid新建一个线程,每个线程负责取得每个cid对应bug的历史记录
                            # 每个线程的执行开始时间间隔1s
                            # 每个线程之间不需要互相等待,独立运行
                            # 主函数等待搜集的历史记录中记录数等于cid数量后继续执行
                            # 线程取得bug的历史记录后即刻添加至历史记录dict中
                            for cid in cidList:
                                threading.Thread(target=bugData.getBugHistory, args=(cid,)).start()
                                time.sleep(0.5)
                            while bugData.return_bugHistoryDictLens() < len(cidList):
                                time.sleep(1)
                            bugHistoryDict = bugData.return_bugHistoryDict()
                            # print(bugHistoryDict)
                            # 此时告知用户正在请求buglist页
                            params = [1, 3, '正在根据bugid请求buglist页...']
                            self.trigger.emit(params)
                            bugDataDict = bugData.getBugList(cidList)
                            if bugDataDict == 1:
                                params = [3, 0, '网络或服务器异常!']
                                self.trigger.emit(params)
                            else:
                                # 此时告知用户正在生成带图表的xlsx
                                params = [1, 4, '正在生成带图表的xlsx...']
                                self.trigger.emit(params)
                                createXlsx = bugDataDict2xlsx(mode=0,buglist=bugDataDict, filedir=self.filedir,
                                                              ChartDATA=bugHistoryDict, closedFlag=self.closedFlag)
                                createXlsx.create_xlsxWithChart()
                                # 此时告知用户xlsx生成成功
                                params = [2, 5, 'xlsx生成成功,点击开始可再次生成']
                                self.trigger.emit(params)
            else:
                # 此时告知用户正在请求汇总bug下所有二级汇总bug的id
                params = [1, 1, '正在请求汇总bug下所有二级汇总bug的id...']
                self.trigger.emit(params)
                aid = str(self.bugid)
                bugData = bug2xlsx_request()
                # 预登录取cookie
                login_result = bugData.login_getCookie()
                if login_result == 2:
                    params = [3, 0, '请先配置账号信息!']
                    self.trigger.emit(params)
                elif login_result == 1:
                    params = [3, 0, '账号名或密码错误!']
                    self.trigger.emit(params)
                else:
                    bidList = bugData.return_idList(aid)
                    if bidList == '':
                        params = [3, 0, '汇总id下未发现挂靠分汇总id,请确认id是否正确!']
                        self.trigger.emit(params)
                    elif bidList == 1:
                        params = [3, 0, '网络或服务器异常!']
                        self.trigger.emit(params)
                    elif bidList == 2:
                        params = [3, 0, '请先配置账号信息!']
                        self.trigger.emit(params)
                    # elif len(bidList) > 10:
                    #     aaa = errorWindow
                    #     aaa.exec()
                    cidList = []
                    i = 0
                    for id in bidList:
                        # 此时告知用户正在请求各二级汇总bug下所有bug的id
                        params = [1, 2, '正在请求第' + str(i + 1) + '个(共' + str(len(bidList)) + '个)二级汇总bug下所有bug的id...']
                        self.trigger.emit(params)
                        ccidList = bugData.return_idList(id)
                        if ccidList == 1:
                            params = [3, 0, '网络或服务器异常!']
                            self.trigger.emit(params)
                        else:
                            cidList = cidList + ccidList
                            i = i + 1
                    if cidList == []:
                        params = [3, 0, '分汇总id下未发现挂靠bug,请确认id是否正确!']
                        self.trigger.emit(params)
                    else:
                        if self.drawChart == 0:
                            params = [1, 3, '正在根据bugid请求buglist页...']
                            self.trigger.emit(params)
                            bugDataDict = bugData.getBugList(cidList)
                            if bugDataDict == 1:
                                params = [3, 0, '网络或服务器异常!']
                                self.trigger.emit(params)
                            else:
                                # 此时告知用户正在生成无图表的xlsx
                                params = [1, 4, '正在生成无图表的xlsx...']
                                self.trigger.emit(params)
                                createXlsx = bugDataDict2xlsx(mode=0,buglist=bugDataDict, filedir=self.filedir,
                                                              closedFlag=self.closedFlag)
                                createXlsx.create_xlsxNoChart()
                                # 此时告知用户xlsx生成成功
                                params = [2, 5, 'xlsx生成成功,点击开始可再次生成']
                                self.trigger.emit(params)
                        else:
                            # 此时告知用户正在请求bug历史记录
                            params = [1, 3, '正在根据bugid搜集bug历史记录...']
                            self.trigger.emit(params)
                            # 每个cid新建一个线程,每个线程负责取得每个cid对应bug的历史记录
                            # 每个线程的执行开始时间间隔1s
                            # 每个线程之间不需要互相等待,独立运行
                            # 主函数等待搜集的历史记录中记录数等于cid数量后继续执行
                            # 线程取得bug的历史记录后即刻添加至历史记录dict中
                            for cid in cidList:
                                threading.Thread(target=bugData.getBugHistory, args=(cid,)).start()
                                time.sleep(0.5)
                            while bugData.return_bugHistoryDictLens() < len(cidList):
                                time.sleep(1)
                            bugHistoryDict = bugData.return_bugHistoryDict()
                            # print(bugHistoryDict)
                            # 此时告知用户正在请求buglist页
                            params = [1, 4, '正在根据bugid请求buglist页...']
                            self.trigger.emit(params)
                            bugDataDict = bugData.getBugList(cidList)
                            if bugDataDict == 1:
                                params = [3, 0, '网络或服务器异常!']
                                self.trigger.emit(params)
                            else:
                                # 此时告知用户正在生成无图表的xlsx
                                params = [1, 5, '正在生成带图表的xlsx...']
                                self.trigger.emit(params)
                                createXlsx = bugDataDict2xlsx(mode=0,buglist=bugDataDict, filedir=self.filedir,
                                                              ChartDATA=bugHistoryDict, closedFlag=self.closedFlag)
                                createXlsx.create_xlsxWithChart()
                                # 此时告知用户xlsx生成成功
                                params = [2, 6, 'xlsx生成成功,点击开始可再次生成']
                                self.trigger.emit(params)
        elif self.mode == 2:
            searchKeyword = ''
            if self.type == 0:
                searchKeyword = 'task'
            elif self.type == 1:
                searchKeyword = 'story'
            # j = 'wait'
            # self.trigger2.emit(j)
            # 程序已准备好,告诉用户任务马上开始
            params = [0, 0, '任务马上开始,请稍候...']
            self.trigger.emit(params)
            time.sleep(1)
            params = [1, 1, '正在查询符合条件的所有bug的id...']
            self.trigger.emit(params)
            aid = str(self.bugid)
            bugData = bug2xlsx_request_ChanDao()
            # 预登录取cookie
            login_result = bugData.setAuthentication()
            if login_result == 2:
                params = [3, 0, '请先配置账号信息!']
                self.trigger.emit(params)
            elif login_result == 1:
                params = [3, 0, '网络或服务器异常!']
                self.trigger.emit(params)
            else:
                bugIdList = bugData.return_idList(id=aid, keyword=searchKeyword, productID=self.productID)
                # print(bugIdList)
                if bugIdList == []:
                    params = [3, 0, '当前查询条件下未发现BUG,请确认id是否正确!']
                    self.trigger.emit(params)
                elif bugIdList == 1:
                    params = [3, 0, '网络或服务器异常!']
                    self.trigger.emit(params)
                else:
                    # 此时需要抓取各个bug当天的历史记录
                    params = [1, 2, '正在抓取所有bug的历史记录...']
                    self.trigger.emit(params)
                    reopenANDpending = bugData.return_reopenANDpending(bugIdList)
                    for id in bugIdList:
                        threading.Thread(target=bugData.getBugHistory, args=(id,)).start()
                        time.sleep(0.5)
                    while bugData.return_bugHistoryDictLens() < len(bugIdList):
                        time.sleep(1)
                    bugHistoryDict = bugData.return_bugHistoryDict()
                    # 此时需要抓取整个的buglist
                    params = [1, 3, '正在抓取buglist...']
                    self.trigger.emit(params)
                    bugListDict = bugData.return_bugList(aid, keyword=searchKeyword, productID=self.productID)
                    # 此时告知用户正在生成xlsx
                    params = [1, 4, '正在生成xlsx...']
                    self.trigger.emit(params)
                    createXlsx = bugDataDict2xlsx(mode=2, buglist=bugListDict, filedir=self.filedir,
                                                  ChartDATA=bugHistoryDict, closedFlag=self.closedFlag, reopenANDpending=reopenANDpending)
                    createXlsx.create_xlsxWithChart()
                    # 此时告知用户xlsx生成成功
                    params = [2, 5, 'xlsx生成成功,点击开始可再次生成']
                    self.trigger.emit(params)
    def run(self):
        self.gogogo()
