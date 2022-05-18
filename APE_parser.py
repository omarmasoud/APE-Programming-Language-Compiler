

from settings import TokensTypes as Types
#from anytree import Node,RenderTree,DoubleStyle,AsciiStyle,AbstractStyle


class Parser:
    def __init__(self, tokenList):
        self.tokens = tokenList
        self.tokenSize = len(self.tokens)
        self.nextToken = self.tokens[1]
        self.currentToken = self.tokens[0]
        self.tokenIndex = 1
        self.finished = False
        self.tabsNumber = 0
        self.pythonLines =""
        self.currentClass = ''
        self.classVariables = {}
        

    
    def checkCurrentTokenByType(self, tokenType):
        return self.currentToken.type == tokenType

    def checkCurrentTokenByVal(self, tokenVal):
       return self.currentToken.value == tokenVal

    def checkNextTokenByType(self, tokenType):
        return self.nextToken.type == tokenType

    def checkNextTokenByVal(self, tokenVal):
       return self.nextToken.value == tokenVal

    def getTabsString(self):
        a = ""
        for i in range(self.tabsNumber):
            a += "\t"
        return a 
    def getPythonCode(self):
        return self.pythonLines
    ## Match token     
    def match(self,foundVal, checkbyValue= False):
        if(self.currentToken.type.name != "EOF"):
            # matched or not ?
            if(checkbyValue):
                if(self.checkCurrentTokenByVal(foundVal)):
                    print("\nDone Parsing {}".format(self.currentToken.value))
                    self.stepOneToken()
                else:
                    raise ValueError('TokenType Mismatch', self.currentToken)
            else:
                if(self.checkCurrentTokenByType(foundVal)):
                    print("Done Parsing {}".format(self.currentToken.value))
                    self.stepOneToken()
                else:
                
                    
                    raise ValueError('TokenType Mismatch', self.currentToken.value)

        else:
            print("Finished Parsing ")
            self.finished = True
        
        
    def peek(self,val,checkbyValue= False):
        if(checkbyValue):
            return self.checkCurrentTokenByVal(val)
        else:
            return self.checkCurrentTokenByType(val)

    def peekNext(self,val,checkbyValue= False):
        if(checkbyValue):
            return self.checkNextTokenByVal(val)
        else:
            return self.checkNextTokenByType(val)



    def stepOneToken(self):
        
        if self.tokenIndex < self.tokenSize + 1:
            self.tokenIndex += 1
            self.currentToken = self.nextToken
            self.nextToken = self.tokens[self.tokenIndex]
            if(self.currentToken.type.name == "EOF"):
                self.match(Types.EOF)
            
            
    def parse(self):
        self.Program()

   
    

    def statement(self,isClass:bool = False,init=False):
        
        if(self.peek(Types.identifier) and self.peekNext(Types.leftbracket) == False):
            return self.assignStmt(isClass,init)
        if(self.peek("panic",checkbyValue=True)):
            return self.printStmt()
        if(self.peek("listen", checkbyValue=True)):
            return self.listenStmt()
        if(self.peek("when",checkbyValue=True) or self.peek("within",checkbyValue=True)):
            return self.loopStmt()
        if(self.peek("routine", checkbyValue=True)):
            return self.funcDef(isClass)
        if(self.peek("familyof",checkbyValue=True)):
            return self.classDef()
        if(self.peek("return",checkbyValue=True)):
            return self.returnStmt(isClass)
        if(self.peek("if",checkbyValue=True)):
            return self.ifStmt()
        if(self.peek(Types.identifier) and self.peekNext(Types.leftbracket)):
            return self.funcCall()
        else:
            raise ValueError('Dont know this statement :(', self.currentToken.value)
        
    
        ####---------------------PARAMS------------------------------------------------
    def params(self):
        if(self.exp()):
            while(self.peek(Types.comma)):
                self.pythonLines += self.currentToken.value
                self.match(Types.comma)
                self.exp()
            return True
        return False
            


        ####---------------------OBJECT------------------------------------------------
    
    def obj(self):
        #self.pythonLines += self.getTabsString()
        if(self.peek("new",checkbyValue=True)):
            self.match("new",checkbyValue=True)
            self.pythonLines += self.currentToken.value
            self.match(Types.identifier)
            self.matchBetweenBrackets("()",self.params,optional=True)
            while(self.peek(Types.dot)):
                self.pythonLines += self.currentToken.value
                self.match(Types.dot)
                self.pythonLines += self.currentToken.value
                self.match(Types.identifier)
                self.matchBetweenBrackets("()",self.params,optional=True)
            return True
        elif(self.peek(Types.identifier)):
            pass
            # self.pythonLines += self.currentToken.value
            # self.match(Types.identifier)
            # self.pythonLines += self.currentToken.value
            # self.match(Types.leftsquarebracket)
            # self.pythonLines += self.currentToken.value
            # self.match(Types.number)
            # self.pythonLines += self.currentToken.value
            # self.match(Types.rightsquarebracket)
            # return True
        return False
                                    





        ####---------------------IDENTIFIER------------------------------------------------
    def identifier(self,isClass=False,init=False,secondInit=False):
        print("==============")
        print("flags state")
        print(isClass,init,secondInit)
        if(self.peek(Types.identifier)):
            if isClass:
                if init:
                    self.pythonLines += 'self.'+ self.currentToken.value
                    self.classVariables[self.currentClass].append(self.currentToken.value)
                elif secondInit:
                    self.pythonLines += self.currentToken.value
                else:
                    if self.currentToken.value in self.classVariables[self.currentClass]:
                        self.pythonLines += 'self.'+ self.currentToken.value
                    else:
                        self.pythonLines += self.currentToken.value

            
            else:    
                self.pythonLines += self.currentToken.value
                # self.pythonLines += self.currentToken.value
            self.match(Types.identifier)
            if(self.peek(Types.dot)):
                self.pythonLines += "."
                self.match(Types.dot)
                if(self.peek(Types.identifier)):
                    self.pythonLines += self.currentToken.value
                    self.match(Types.identifier)
                    if(self.peek(Types.leftbracket)):
                        self.matchBetweenBrackets("()",self.params, optional=True)
                        if(self.peek(Types.dot) == False):
                            self.pythonLines += "\n"
                    return True
                
            
            return True
        return False


    

        #### --------------------Operators--------------------------------------------
    def comparisonOp(self):
        if(self.peek(Types.greaterthanoperator)):
            self.pythonLines += self.currentToken.value
            self.match(Types.greaterthanoperator)
            return True
        elif(self.peek(Types.lessthanoperator)):
            self.pythonLines += self.currentToken.value
            self.match(Types.lessthanoperator)
            return True
        elif(self.peek(Types.greaterthanorequaloperator)):
            self.pythonLines += self.currentToken.value
            self.match(Types.greaterthanorequaloperator)
            return True
        elif(self.peek(Types.lessthanorequaloperator)):
            self.pythonLines += self.currentToken.value
            self.match(Types.lessthanorequaloperator)
            return True
        elif(self.peek(Types.equaloperator)):
            self.pythonLines += "=="
            self.match(Types.equaloperator)
            return True
        elif(self.peek(Types.notequaloperator)):
            self.pythonLines += self.currentToken.value
            self.match(Types.notequaloperator)
            return True
        else:
            return False
    def multiplicationOp(self):
        if(self.peek(Types.multiplicationoperator)):
            self.pythonLines += self.currentToken.value
            self.match(Types.multiplicationoperator)
            return True
        elif(self.peek(Types.divisionoperator)):
            self.pythonLines += self.currentToken.value
            self.match(Types.divisionoperator)
            return True
        return False
    def additionOp(self):
        if(self.peek(Types.additionoperator)):
   
            self.pythonLines += self.currentToken.value
            self.match(Types.additionoperator)
            return True
        elif(self.peek(Types.subtractionoperator)):
      
            self.pythonLines += self.currentToken.value
            self.match(Types.subtractionoperator)
            return True
        return False
    def logicalOp(self):
        if(self.peek(Types.logical_operator) ):
            self.pythonLines += self.currentToken.value
            self.match(Types.logical_operator)
            return True
        return False

        ###----------------------------------------------------------------------------------
    ###-------------------------------EXPRESSIONS---------------------------------------------------    
    def exp(self,isClass=False,init=False,secondInit=False):
        if(self.peek(Types.string)):

            self.pythonLines +=  self.currentToken.value 
            self.match(Types.string)
            return True
        else:

            return self.explow(isClass,init,secondInit)


    def explow(self,isClass=False,init=False,secondInit=False):
        if(self.explowlow(isClass,init,secondInit)):
            while(self.peek(Types.logical_operator)):
                self.logicalOp()
                self.explowlow()
            return True
        return False




    def explowlow(self,isClass=False,init=False,secondInit=False):
        if(self.simpleExp(isClass,init,secondInit)):
            #print("CURRENT VALUE: ")
            #print(self.currentToken.value)
            while(self.checkforComparisonOp()):
                #print("before compop")
                self.comparisonOp()
                #print("after compop")
                self.simpleExp()
            return True
        #print("before leaving explowlow")
        return False



    def simpleExp(self,isClass=False,init=False,secondInit=False):
        if(self.term(isClass,init,secondInit)):

            while(self.peek(Types.additionoperator) or self.peek(Types.subtractionoperator)):
                self.additionOp()
                self.term()
            return True
        return False


    def term(self,isClass=False,init=False,secondInit=False):
        if(self.primaryExpr(isClass,init,secondInit)):
            while(self.peek(Types.multiplicationoperator) or self.peek(Types.divisionoperator)):
                self.multiplicationOp()
                self.primaryExpr()
            return True
        return False

    def primaryExpr(self,isClass=False,init=False,secondInit=False):
        if(self.peek(Types.number)):
            self.pythonLines += self.currentToken.value

            self.match(Types.number)
            return True
        
        elif(self.identifier(isClass,init,secondInit)):
            
            return True
        elif(self.peek(Types.leftbracket)):
            self.pythonLines += self.currentToken.value
            self.match(Types.leftbracket)
            if(self.exp()):
                self.pythonLines += self.currentToken.value
                self.match(Types.rightbracket)
                return True
        elif(self.obj()):
            return True
        
        else:
            return False
            

    ###----------------------------------------------------------------------------------

    ###---------------------------------STATEMENTS-------------------------------------------------
    def assignStmt(self,isClass=False,init=False):

        self.pythonLines += self.getTabsString()
        if(self.identifier(isClass,init)):
            if(self.peek(Types.assignmentoperator)):
         
                self.pythonLines += "="
                self.match(Types.assignmentoperator)
                temp =True
                if init == True:
                    temp = False
                print(isClass,temp)
                if(self.exp(isClass,False,True) or self.obj()):
                    self.pythonLines += "\n"
                    return True
                self.pythonLines += "\n"
        return False


    def returnStmt(self,isClass=False):
        self.pythonLines += self.getTabsString()
        if(self.peek("return",checkbyValue=True)):
            self.pythonLines += "return "
            self.match("return",checkbyValue=True)
            self.exp(isClass)
            self.pythonLines += "\n"
            return True
        
        self.pythonLines += "\n"
        return False

    def ifStmt(self): 
        self.pythonLines += self.getTabsString()
        if(self.peek("if",checkbyValue=True)):
            self.pythonLines += "if ("
            self.match("if",checkbyValue=True)
            self.matchBetweenBrackets("()", self.exp)
            self.pythonLines += "):\n"
            self.matchstmtseq()
            while(self.peek("elseif",checkbyValue=True)):
                self.pythonLines += "elif ("
                self.match("elseif",checkbyValue=True)
                self.matchBetweenBrackets("()",self.exp)
                self.pythonLines += "):\n"
                self.matchstmtseq()
            if(self.peek("else",checkbyValue=True)):
                self.pythonLines += "else: \n"
                self.match("else",checkbyValue=True)
                self.matchstmtseq()
            return True
        return False


    def printStmt(self):
        self.pythonLines += self.getTabsString()
        self.pythonLines += ("print")
        self.match("panic",checkbyValue=True)
        if(self.peek(Types.leftbracket)):
            self.pythonLines += self.currentToken.value
            self.match(Types.leftbracket)
            if(self.exp()):
                self.pythonLines += self.currentToken.value
                self.match(Types.rightbracket)
                self.pythonLines += "\n"
                return True
            elif(self.obj()):
                self.pythonLines += self.currentToken.value
                self.match(Types.rightbracket)
                self.pythonLines += "\n"
                return True
        self.pythonLines += "\n"
        return False



    def listenStmt(self):
        self.pythonLines += self.getTabsString()
        if(self.peek("listen", checkbyValue=1)):
            self.match("listen",checkbyValue=True)
            self.match(Types.leftbracket)
            id = self.currentToken.value
            self.match(Types.identifier)
            self.match(Types.rightbracket)
            self.pythonLines += "{} = input() \n".format(id)
            return True
        self.pythonLines += "\n"
        
        return False

    
        
    def loopStmt(self):
        self.pythonLines += self.getTabsString()
        if(self.withinLoop() or self.whenLoop()):
            return True
        return False

    def withinLoop(self):
    
        if(self.peek("within",checkbyValue=True)):
            self.match("within",checkbyValue=True)
            self.match(Types.leftbracket)
            self.assignStmt()
            self.match(Types.semicolon)
            self.pythonLines += "while("
            self.exp()
            self.pythonLines += "): \n"
            self.tabsNumber += 1
            self.match(Types.semicolon)
            #self.pythonLines += self.getTabsString()
            self.assignStmt()
            condLine = 0
            #print("PythonLines: \n {} \n".format(self.pythonLines))
            for i in range(len(self.pythonLines)-1,0,-1):
                if(self.pythonLines[i] == ":"):
                    condLine = i+2
                    break
                    
            endLine = self.pythonLines[condLine+1:]
            print("Endline : \n {}".format(endLine))
            print("Before reassign :  \n {}".format(self.pythonLines[:condLine+1]))
            self.pythonLines = self.pythonLines[:condLine+1]
            
            
            self.match(Types.semicolon)
            self.match(Types.rightbracket)
            self.match(Types.leftcurlybracket)
            print("TABS : {}".format(self.tabsNumber))
            
            if(self.StatementSequence()):
                self.pythonLines += self.getTabsString()
                self.pythonLines += endLine
                self.match(Types.rightcurlybracket)
            
            self.tabsNumber -=1
            return True
        return False

    def whenLoop(self, parentNode=None):
        if(self.peek("when",checkbyValue=True)):
            self.pythonLines += "while("
            self.match("when",checkbyValue=True)
            self.matchBetweenBrackets("()",self.exp)
            self.pythonLines += "):\n"
            self.match("do",checkbyValue=True)
            self.matchstmtseq()
            return True
        return False
    
    def funcDef(self, isClass = False):
        self.pythonLines += self.getTabsString()
        if(self.peek("routine",checkbyValue=True)):
            self.pythonLines += "def "
            self.match("routine",checkbyValue=True)
            if isClass:

                if(self.peek("init",checkbyValue=True)):
                    self.match(Types.identifier)
                    self.pythonLines += "__init__(self,"
                    self.match(Types.leftbracket)
                    self.params()
                    self.pythonLines += self.currentToken.value
                    self.match(Types.rightbracket)
                    self.pythonLines += ":\n"
                    self.matchstmtseq(isClass,True)
                else:
                    self.pythonLines += self.currentToken.value
                    self.match(Types.identifier)
                    self.pythonLines += "("
                    self.match(Types.leftbracket)
                    self.pythonLines += "self,"
                    self.params()
                    self.pythonLines += ")"
                    self.match(Types.rightbracket)
                    self.pythonLines += ":\n"
                    self.matchstmtseq(isClass)

            else:
                self.pythonLines += self.currentToken.value
                self.match(Types.identifier)
                self.matchBetweenBrackets("()",self.params,optional=True)
                self.pythonLines += ":\n"
                self.matchstmtseq()
            return True
        return False 
    def funcCall(self):
        #funcCall->id “(” [ params] “)”
        self.pythonLines += self.getTabsString()
        if(self.peek(Types.identifier)):
            self.pythonLines += self.currentToken.value
            self.match(Types.identifier)
            self.matchBetweenBrackets("()",self.params,optional=True)
            return True
        return False


    def classDef(self,):
        self.pythonLines += self.getTabsString()
        if(self.peek("familyof",checkbyValue=True)):
            self.pythonLines += "class "
            self.match("familyof",checkbyValue=True)
            self.currentClass = self.currentToken.value
            self.classVariables[self.currentClass] = []
            self.pythonLines += self.currentToken.value
            self.match(Types.identifier)
            if(self.peek("inherit",checkbyValue=True)):
                
                self.match("inherit",checkbyValue=True)
                self.pythonLines += "("  + self.currentToken.value + "):\n"
                self.match(Types.identifier)
                self.matchstmtseq(True)
            else:
                self.pythonLines += ":\n"
                self.matchstmtseq(isClass=True)
            
            return True
        return False




    def Program(self):
        return self.StatementSequence()
    def StatementSequence(self,isClass:bool = False,init=False):
        
        if(self.statement(isClass,init)):
            if(self.peek(Types.semicolon) == False):
                raise SyntaxError('semi colon messing!')
            
            while(self.peek(Types.semicolon)):
                
                self.match(Types.semicolon)
                if(self.currentToken.type != Types.EOF and (self.currentToken.value not in [")","}","]"])):
                    self.statement(isClass,init)
            return True
        return False

    def matchstmtseq(self,isClass:bool = False,init=False):
        self.tabsNumber += 1
        self.match(Types.leftcurlybracket)
        if(self.StatementSequence(isClass,init)):
            self.match(Types.rightcurlybracket)
        self.tabsNumber -=1

    def matchBetweenBrackets(self, bracket, tokenFunc, optional = 0):
        if(bracket == '[]'):
            self.pythonLines += self.currentToken.value
            self.match(Types.leftsquarebracket)
            if(tokenFunc() or optional):
                self.pythonLines += self.currentToken.value
                self.match(Types.rightsquarebracket)
        elif(bracket == '()'):
            self.pythonLines += self.currentToken.value
            self.match(Types.leftbracket)
            if(tokenFunc() or optional):
                self.pythonLines += self.currentToken.value
                self.match(Types.rightbracket)
        elif(bracket == '{ }'):
            self.pythonLines += self.currentToken.value
            self.match(Types.leftcurlybracket)
            if(tokenFunc() or optional):
                self.pythonLines += self.currentToken.value
                self.match(Types.rightcurlybracket)

    def checkforComparisonOp(self):
        if(self.peek(Types.greaterthanoperator)):
            return True
        elif(self.peek(Types.lessthanoperator)):
            return True
        elif(self.peek(Types.greaterthanorequaloperator)):
            return True
        elif(self.peek(Types.lessthanorequaloperator)):
            return True
        elif(self.peek(Types.equaloperator)):
            return True
        elif(self.peek(Types.notequaloperator)):
            return True
        else:
            return False
   
    