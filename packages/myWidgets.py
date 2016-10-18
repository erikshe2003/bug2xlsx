#-*- coding: utf-8 -*-
__author__ = 'wufeng_wb'

import images
from PyQt5 import QtWidgets, QtCore

class mybutton(QtWidgets.QPushButton):
    def mouseMoveEvent(self, event):
        pass

class minButton(mybutton):
    def initStyle(self,enabled):
        self.setObjectName("minButton")
        self.enabled = enabled
        if enabled == False:
            self.url = "#minButton {background-image:url(:/minWin_disabled.png);border:0}"
            self.url_hover = "#minButton {background-image:url(:/minWin_disabled.png);border:0}"
            self.setStyleSheet(self.url)
        elif enabled == True:
            self.url = "#minButton {background-image:url(:/minWin.png);border:0;border:0}"
            self.url_hover = "#minButton {background-image:url(:/minWin_hover.png);border:0}"
            self.setStyleSheet(self.url)
    def enterEvent(self, *args, **kwargs):
        self.setStyleSheet(self.url_hover)
    def leaveEvent(self, *args, **kwargs):
        self.setStyleSheet(self.url)

class closeButton(mybutton):
    def initStyle(self,enabled):
        self.setObjectName("closeButton")
        self.enabled = enabled
        if enabled == False:
            self.url = "#closeButton {background-image:url(:/closeWin_disabled.png);border:0}"
            self.url_hover = "#closeButton {background-image:url(:/closeWin_disabled.png);border:0}"
            self.setStyleSheet(self.url)
        elif enabled == True:
            self.url = "#closeButton {background-image:url(:/closeWin.png);border:0}"
            self.url_hover = "#closeButton {background-image:url(:/closeWin_hover.png);border:0}"
            self.setStyleSheet(self.url)
    def enterEvent(self, *args, **kwargs):
        self.setStyleSheet(self.url_hover)
    def leaveEvent(self, *args, **kwargs):
        self.setStyleSheet(self.url)

class startButton(mybutton):
    def initStyle(self,enabled):
        self.setObjectName("startButton")
        self.enabled = enabled
        if enabled == False:
            self.url = "#startButton {font-family:幼圆;background-color:#C3C3C3;color:white;border:1px solid lightgrey;border-radius:3px}"
            self.url_hover = "#startButton {font-family:幼圆;background-color:#C3C3C3;color:white;border:1px solid lightgrey;border-radius:3px}"
            self.setStyleSheet(self.url)
        elif enabled == True:
            self.url = "#startButton {font-family:幼圆;background-color:white;color:black;border:1px solid lightgrey;border-radius:3px}"
            self.url_hover = "#startButton {font-family:幼圆;background-color:rgba(122,144,190,1);color:white;border:1px solid lightgrey;border-radius:3px}"
            self.setStyleSheet(self.url)
    def enterEvent(self, *args, **kwargs):
        self.setStyleSheet(self.url_hover)
    def leaveEvent(self, *args, **kwargs):
        self.setStyleSheet(self.url)

class chooseButton(mybutton):
    def initStyle(self,enabled):
        self.enabled = enabled
        self.setObjectName("chooseButton")
        if enabled == False:
            self.url = "#chooseButton {background-color:#C3C3C3;color:white;border:1px solid lightgrey;border-radius:3px}"
            self.url_hover = "#chooseButton {background-color:#C3C3C3;color:white;border:1px solid lightgrey;border-radius:3px}"
            self.setStyleSheet(self.url)
        elif enabled == True:
            self.url = "#chooseButton {background-color:white;color:black;border:1px solid lightgrey;border-radius:3px}"
            self.url_hover = "#chooseButton {background-color:rgba(122,144,190,1);color:white;border:1px solid lightgrey;border-radius:3px}"
            self.setStyleSheet(self.url)
    def enterEvent(self, *args, **kwargs):
        self.setStyleSheet(self.url_hover)
    def leaveEvent(self, *args, **kwargs):
        self.setStyleSheet(self.url)