from logging import disable
from kivy.config import Config
Config.set('kivy','window_icon','hacking.png')
from os import error
from typing import Text
import kivy
from kivy.app import App
from kivy.core import text
from kivy.core.window import Window
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


class Editor(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.curText = []
        self.lastWord = ''
        self.startIndex = 0

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        comp = self.parent.parent.parent
        if keycode[0] in self.interesting_keys:
            if keycode[1] == 'enter':
                print('yoooo')
                comp.trie.add(self.lastWord)
            self.lastWord = ''
        elif  keycode[1] != 'spacebar' and keycode[1] != 'tab' and keycode[1] != '.' :
            self.lastWord += keycode[1]
            comp.configAutoComplete(self.lastWord)
        else:
            comp.trie.add(self.lastWord)
            print('hoooooo')
            self.lastWord = ''
        
        return super().keyboard_on_key_down(window, keycode, text, modifiers)
        
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
        app = App.get_running_app()
        #self.ids.suggestions.dismiss()
        
        app.goCButton.disabled = False
        try:
            print(self.ids.edit.text)
            self.compiler.compile(self.ids.edit.text)
        except (ValueError,SyntaxError,Exception) as e:
             self.showError_Popup(str(e))
        #self.ids.tinyCode.suggestion_text = "Hello"
        
        #app.goCButton.disabled = False
        # if(parserResponse == False):
        #     self.showError_Popup(parserError=parserResponse)
       
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
    def buttonHandler(self,button):
        text = self.ids.edit.text.split()
        print(text)
        text = text[:-1]
        text.append(button.text)
        self.ids.edit.text = ' '.join(text)
        self.ids.edit.lastWord = ''
    def configAutoComplete(self,word):
        
        #self.ids.suggestions.is_open = False
        if(self.ids.edit.text != ""):
            
            suggestions = self.trie.autoComplete(word)
            print(suggestions)
            self.ids.suggestions.clear_widgets()
            layout = GridLayout(cols=1, spacing=10, size_hint_y=None, row_default_height='50dp', row_force_default= True)
            for element in suggestions:
                print(element)
                button = Button(text=element,size=(100,100),size_hint=(0.3,1),on_press=self.buttonHandler)
                button.bind
                layout.add_widget(button)
            self.ids.suggestions.add_widget(layout )
            # if len(suggestions)>0: 
            #     self.ids.suggestions.text = 'auto complete'
            #     self.ids.suggestions.values = suggestions
            #     if( len(suggestions)>1):
            #         self.ids.suggestions.is_open = True
            # self.ids.suggestions.open(self.ids.tinyCode)  
        
    def showError_Popup(self,error):
        show = P() 
        popupWindow = Popup(title="Error", content=show, size_hint=(None,None),size=(400,400)) 
        app = App.get_running_app()
        
        app.goCButton.disabled = True
        app.cError.text = error 
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
