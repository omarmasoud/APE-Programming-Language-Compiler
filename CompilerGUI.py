from cgitb import text
import code
import sys
from xml.etree.ElementTree import tostring
from APE_Compiler import Compiler
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QWidget,QGridLayout,QTableWidget,QApplication,QTableWidgetItem,QTextEdit,QTextBrowser,QTabWidget,QMenuBar,QMenu,QAction,QFileDialog,QPlainTextEdit)
from PyQt5.QtCore import QEvent 
from PyQt5 import QtCore
from Trie.Trie import Trie

class CodeEditor(QPlainTextEdit):
    def keyPressEvent(self, event):
        #print(self.searchingWord)
        if(event.key()):
            print(event.text()) 
        super(CodeEditor, self).keyPressEvent(event)

class basicWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.currentTab = None
        self.tabNumber=1
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        self.setFixedSize(1200,800)
        self.setWindowTitle('MY Compiler')
        self.arrayOfTabs=[]
        self.setStyleSheet("font-size: 18px")
        self.trie = Trie()
        self.searchingWord = ""
        

        self.compiler = Compiler()
        
        

        self.bottomTabWidget= QTabWidget()

        self.tabWidget = QTabWidget()
        self.tabWidget.setStyleSheet("QTextEdit{font-size:22px}")
        
        self.maintab = CodeEditor() #Tab 1 in editor
        self.tabWidget.addTab(self.maintab,"TAB1")
        self.arrayOfTabs.append(self.maintab)
       

       
       

        self.errorTab = QTextBrowser()
        self.errorTab.setStyleSheet("color: red;" "background-color: black;" "font-size:20px")

        self.pythonCode = QTextBrowser()
        self.pythonCode.setStyleSheet("color: green;" "background-color: black;" "font-size:20px")
       
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
        open_tab.triggered.connect(self.new_Tab)

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
        
        
        

        grid_layout.addWidget(self.tabWidget,1,0,1,1)    
        grid_layout.addWidget(self.bottomTabWidget,2,0,2,1)
        grid_layout.addWidget(menubar,0,0,1,1) 
    
    

       

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
        

        


    
    
    def new_Tab(self):
        self.tabNumber=self.tabNumber+1
        self.currentTab = QTextEdit(self)
        print(self.currentTab)
        #self.currentTab.installEventFilter(self)
        #temptextEdit.keyPressEvent = self.keyPressEvent
        self.arrayOfTabs.append(self.currentTab)

        tabnumber= "Tab {tabNum}".format(tabNum=self.tabNumber)
        self.tabWidget.addTab(self.arrayOfTabs[-1],tabnumber)
        self.update()


    def run_file(self):
        print(self.tabNumber-1)
        code = self.arrayOfTabs[self.tabNumber-1].toPlainText()
        #print(code)
        self.compiler.compile(code)
        #self.new_Tab()
        #self.arrayOfTabs[self.tabNumber-1].setPlainText(self.compiler.parser.getPythonCode())
        self.bottomTabWidget.addTab(self.pythonCode, 'Generated Code')
        self.pythonCode.append(self.compiler.parser.getPythonCode())
    





    def show_tokens(self):

        
        code = self.arrayOfTabs[self.tabNumber-1].toPlainText()
        self.compiler.compile(code)

        try:
            tokenList= self.compiler.s.getTokensList()
            for i in tokenList:
                row_count = self.tokenTab.rowCount()
                self.tokenTab.insertRow(self.tokenTab.rowCount())
                self.tokenTab.setItem(row_count,1,QTableWidgetItem(" {num}".format(num=i.value)))
                self.tokenTab.setItem(row_count,0,QTableWidgetItem(" {num}".format(num=i.type.name)))

            print(tokenList)
        except Exception as e:
            print('entered except')
            print(e)


        
        
        

    
        
        
        
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    windowExample = basicWindow()
    windowExample.show()
    sys.exit(app.exec_())