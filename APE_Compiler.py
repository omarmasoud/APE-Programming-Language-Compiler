from APE_parser import Parser
from APEScanner import scanner,Token
import settings

class Compiler:
    def __init__(self,code):
        self.s = scanner()
        self.code = code
        
    def compile(self):
        self.s.scan(self.code)
        t = Token(settings.TokensTypes.EOF,123)
        print("\nPrinting list of tokens : ")
        tokens = self.s.getTokensList()
        print("Done .. \n")
        tokens.append(t)
        tokens.append(t)
        self.parser = Parser(tokens)
        self.parser.parse()
        with open('output.py','w') as f:
            f.write(self.parser.pythonLines)

