from APE_parser import Parser
from APEScanner import scanner,Token
import settings

class Compiler:
    def __init__(self,code):
        self.s = scanner()
        self.s.scan(code)
        
        t = Token(settings.TokensTypes.EOF,123)
        print("\nPrinting list of tokens : ")
        tokens = self.s.getTokensList()
        # for i in tokens:
        #     print(i.value, " {}".format(i.type.name))
        print("Done .. \n")
        tokens.append(t)
        tokens.append(t)
        self.parser = Parser(tokens)
        self.parser.parse()
