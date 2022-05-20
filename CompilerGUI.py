from logging import disable
from kivy.config import Config
Config.set('kivy','window_icon','hacking.png')
from os import error
from typing import Text
import kivy
from kivy.app import App
from kivy.core import text
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
import pyperclip
from kivy.clock import Clock
from APE_Compiler import Compiler
from Trie.Trie import Trie




class CompilerLayout(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.compiler = Compiler()
        self.numberOfToken = Label(text="#")
        self.firstColName = Label(text="Token Name ")
        self.secondColName = Label(text="Token Value")
        self.trie = Trie()
    def run(self,superRoot):
        count = 0
        self.ids.suggestions.dismiss()
        parserResponse = self.compiler.compile(self.ids.tinyCode.text)
        self.ids.tinyCode.suggestion_text = "Hello"
        app = App.get_running_app()
        app.goCButton.disabled = False
        if(parserResponse == False):
            self.showError_Popup(parserError=parserResponse)

        pythonGeneratedCode = self.compiler.parser.getPythonCode()
        app.pythonCode =  app.cTextInput.text = pythonGeneratedCode

        
        app.table.clear_widgets()
        app.table.add_widget(self.numberOfToken)
        app.table.add_widget(self.firstColName)
        app.table.add_widget(self.secondColName)
        for token in self.compiler.s.getTokensList():
            tokenNum = TextInput(text=str(count+1),disabled=True,size=(100,100),size_hint=(0.3,1))
            tname = TextInput(text=str(token.value),disabled=True,size=(100,100),size_hint=(1,1))
            tval = TextInput(text=str(token.type.name),disabled=True,size=(100,100),size_hint=(0.3,1))
            app.table.add_widget(tokenNum)
            app.table.add_widget(tname)
            app.table.add_widget(tval)
            count = count +1 
            
        superRoot.root.current = "tableScreen"
        self.manager.transition.direction = "left"
    
    def configAutoComplete(self):
        app = App.get_running_app()
        
        #self.ids.suggestions.is_open = False
        if(self.ids.tinyCode.text != ""):
            app.searchingWord = self.ids.tinyCode.text.split()[-1]
            suggestions = self.trie.autoComplete(app.searchingWord)
            self.ids.suggestions.text = suggestions[0]
            self.ids.suggestions.values = suggestions[1:]
            if( len(suggestions)>1):
                self.ids.suggestions.is_open = True
            #self.ids.suggestions.open(self.ids.tinyCode)  
        
    def showError_Popup(self,parserError, scannerError):
        show = P() 
        popupWindow = Popup(title="Error", content=show, size_hint=(None,None),size=(400,400)) 
        app = App.get_running_app()
        if(scannerError ):
            app.cError.text = "Scanner Error"
        elif(parserError):
            app.goCButton.disabled = True
            app.cError.text = "Parser Error"
        popupWindow.open() 
        
class TokenTable(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.assign)
    
    def assign(self,dt):
        app = App.get_running_app()
        app.table = self.ids.tableLayout
        app.goCButton = self.ids.goToC
    
    


class P(BoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        app = App.get_running_app()
        app.cError = self.ids.errorLabel
class Code(Screen):
    
    def __init__(self, **kw):
        super(Code,self).__init__(**kw)
        Clock.schedule_once(self.assign)
    def assign(self,dt):
        app = App.get_running_app()
        app.cTextInput = self.ids.cTextInput
    def copy(self):
        app = App.get_running_app()
        pyperclip.copy(app.pythonCode)
class WindowManager(ScreenManager):
    pass
kv = Builder.load_file('compilerlayout.kv')


class MyApp(App): # <- Main Class
    code:str = ''

    def build(self):
        self.title = 'APE Charm'
        return kv

if __name__ == "__main__":
    MyApp().run()
