import sys
from xml.etree.ElementTree import tostring
from PyQt5.QtWidgets import (QWidget,QGridLayout,QPushButton, QApplication,QTextEdit,QTextBrowser,QTabWidget,QMenuBar,QMenu,QAction,QFileDialog)

class basicWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.tabNumber=1
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        self.setFixedSize(1200,800)
        self.setWindowTitle('MY Compiler')
        self.arrayOfTabs=[]
        

        self.textBrowser= QTextBrowser()
        self.tabWidget = QTabWidget()
        
        self.maintab = QTextEdit()
        self.tabWidget.addTab(self.maintab,"TAB1")
        self.arrayOfTabs.append(self.maintab)
       

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


        file_menu.addAction(save_action)
        file_menu.addAction(open_tab)
        file_menu.addAction(exit_action) 
        
        
        

        grid_layout.addWidget(self.tabWidget,1,0,1,1)    
        grid_layout.addWidget(self.textBrowser,2,0,2,1)
        grid_layout.addWidget(menubar,0,0,1,1) 
       

    def file_save(self):
        name = QFileDialog.getSaveFileName(self,'Save File','/','.txt')[0] 
        file = open(name,'w')
        tabnumber=self.tabWidget.currentIndex()
        text = self.arrayOfTabs[tabnumber].toPlainText()
        file.write(text)
        file.close()
    
    
    
    def new_Tab(self):
        self.tabNumber=self.tabNumber+1
        self.arrayOfTabs.append(QTextEdit())
        tabnumber= "Tab {tabNum}".format(tabNum=self.tabNumber)
        self.tabWidget.addTab(self.arrayOfTabs[-1],tabnumber)
        self.update()


    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    windowExample = basicWindow()
    windowExample.show()
    sys.exit(app.exec_())