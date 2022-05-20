from APE_parser import Parser
from APEScanner import scanner,Token
import settings

class Compiler:
    def __init__(self):
        self.s = scanner()
        self.parser = None
        self.fileCounter = 1
        #self.code = code
        
    def compile(self,text):
        self.s.resetScanner(resetTokens=True)
        self.s.scan(text)
        t = Token(settings.TokensTypes.EOF,123)
        print("\nPrinting list of tokens : ")
        tokens = self.s.getTokensList()
        for token in tokens:
            print(token.value)
        print("Done .. \n")
        tokens.append(t)
        tokens.append(t)
        self.parser = Parser(tokens)
        self.parser.parse()
        with open('output{}.py'.format(self.fileCounter),'w') as f:
            self.fileCounter += 1
            f.write(self.parser.pythonLines)
        





