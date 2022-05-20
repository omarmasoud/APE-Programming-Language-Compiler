from cgitb import text
import sys
from xml.etree.ElementTree import tostring
from APE_Compiler import Compiler
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QWidget,QGridLayout,QStackedWidget,QComboBox,QTableWidget,QApplication,QTableWidgetItem,QTextEdit,QTextBrowser,QTabWidget,QMenuBar,QMenu,QAction,QFileDialog,QPlainTextEdit,QLineEdit)
from PyQt5.QtCore import QEvent 
from PyQt5 import QtCore
from Trie.Trie import Trie

class CodeEditor(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.editor = QTextEdit()
        self.recommender = QComboBox()
        self.recommender.addItem("Hello World")
        self.addWidget(self.editor)
        self.addWidget(self.recommender)
    def keyPressEvent(self, event):
        #print(self.searchingWord)
        if(event.key()):
            print(event.text()) 
        super(CodeEditor, self).keyPressEvent(event)
    

class basicWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.currentTab = None
        self.tabNumber=0
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        self.setFixedSize(1200,800)
        self.setWindowTitle('MY Compiler')
        self.arrayOfTabs=[]
        self.setStyleSheet("font-size: 18px")
        
        self.searchingWord = ""


        ##BACKEND OBJECTS
        self.trie = Trie()
        self.compiler = Compiler()
        ##----------------------------------


        self.bottomTabWidget= QTabWidget()

        self.initTabWidget()
        self.createNewTab("main.ape")
        self.errorTab = self.createBottomTab("color: red;" "background-color: black;" "font-size:20px")
        self.pythonCode = self.createBottomTab("color: green;" "background-color: black;" "font-size:20px")
       
        self.tokenTab = QTableWidget()
        self.tokenTab.setStyleSheet("QTableWidgetItem{font-size:18px; color:black}") 
        self.tokenTab.insertColumn(self.tokenTab.columnCount())
        self.tokenTab.insertColumn(self.tokenTab.columnCount())
        self.tokenTab.setHorizontalHeaderLabels(['Token Item', 'Token Value' ])
        self.bottomTabWidget.addTab(self.errorTab, 'Errors')
        self.bottomTabWidget.addTab(self.tokenTab,'Tokens')


        

        menubar= QMenuBar()
        file_menu = menubar.addMenu('File')
        edit_menu = menubar.addMenu('Edit')
        run_menu = menubar.addMenu('Run')
       
        exit_action = QAction('&Exit', grid_layout)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(exit)
        
        save_action = QAction('&Save File',grid_layout)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save File')
        save_action.triggered.connect(self.file_save)

        open_tab = QAction('&New Tab',grid_layout)
        open_tab.setShortcut('Ctrl+U')
        open_tab.setStatusTip('Open New Tab')
        open_tab.triggered.connect(self.createNewTab)

        open_newFile = QAction('&Open File',grid_layout)
        open_newFile.setShortcut('Ctrl+O')
        open_newFile.setStatusTip('Open File')
        open_newFile.triggered.connect(self.open_file)


        
        file_menu.addAction(save_action)
        file_menu.addAction(open_newFile)
        file_menu.addAction(open_tab)
        file_menu.addAction(exit_action) 

        #Finished File Menu


        #Run menu starts

        run_action= QAction('&Run',grid_layout)
        run_action.setShortcut('Ctrl+R')
        run_action.setStatusTip('Run File')
        run_action.triggered.connect(self.run_file)

        tokenPreview_action =  QAction('&Show Tokens',grid_layout)
        tokenPreview_action.setShortcut('Ctrl+T')
        tokenPreview_action.setStatusTip('Show Tokens Table')
        tokenPreview_action.triggered.connect(self.show_tokens)

        run_menu.addAction(run_action)
        run_menu.addAction(tokenPreview_action)

        

        completer = self.createComboBox(["hello","world"])

        
        
        

        grid_layout.addWidget(self.tabWidget,1,0,1,1)    
        grid_layout.addWidget(self.bottomTabWidget,2,0,2,1)
        grid_layout.addWidget(menubar,0,0,1,1)
        #grid_layout.addWidget(completer,1,1,1,1)
    
    

       
    def createBottomTab(self,style):
            textBrowser = QTextBrowser()
            textBrowser.setStyleSheet(style)
            return textBrowser
    def initTabWidget(self):
        self.tabWidget = QTabWidget()
        self.tabWidget.setStyleSheet("QTextEdit{font-size:22px}") 

    def file_save(self):
        name = QFileDialog.getSaveFileName(self,'Save File','/','.txt')[0] 
        file = open(name,'w')
        tabnumber=self.tabWidget.currentIndex()
        text = self.arrayOfTabs[tabnumber].toPlainText()
        file.write(text)
        file.close()
    
    def open_file(self):
        fileName = QFileDialog.getOpenFileName()
        file = fileName[0]
        
        with open(file,"r") as f:
            text = f.readline()
            self.arrayOfTabs[self.tabWidget.currentIndex()].setText(text)
    
    def keyPressEvent(self, qKeyEvent):
        if(qKeyEvent.text() == " "):
            self.searchingWord = ""
        else:
            self.searchingWord += qKeyEvent.text()
        
       
    
    # def keyPressEvent(self, event):
    #     print("Inside event filter")
        
    def createComboBox(self, itemsList):
        temp = QComboBox()
        temp.addItems(itemsList)
        return temp
        


    
    
    def createNewTab(self,name = None):
        self.tabNumber=self.tabNumber+1
        self.currentTab = temp =  CodeEditor()
        temp.setStyleSheet("QPlainText{ border: none; }")
        self.arrayOfTabs.append(self.currentTab)
        tabnumber= "Tab {tabNum}".format(tabNum=self.tabNumber)
        self.tabWidget.addTab(self.arrayOfTabs[-1],name)
        self.update()
        return temp


    def run_file(self):
        print(self.tabNumber-1)
        code = self.arrayOfTabs[self.tabNumber-1].toPlainText()
        #print(code)
        self.compiler.compile(code)
        #self.new_Tab()
        #self.arrayOfTabs[self.tabNumber-1].setPlainText(self.compiler.parser.getPythonCode())
        temp = self.createNewTab("Generated Code")
        #temp.setStyle("{ background-color: %0 }")
        self.currentTab.setPlainText(self.compiler.parser.getPythonCode())
        self.bottomTabWidget.addTab(self.pythonCode, 'Generated Code')
        self.pythonCode.append(self.compiler.parser.getPythonCode())
    





    def show_tokens(self):

        row_count = self.tokenTab.rowCount()        
        self.tokenTab.insertRow(row_count)
        self.tokenTab.setItem(row_count,0,QTableWidgetItem("Row {num}".format(num=row_count)))
        

    
        
        
        
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    windowExample = basicWindow()
    windowExample.show()
    sys.exit(app.exec_())