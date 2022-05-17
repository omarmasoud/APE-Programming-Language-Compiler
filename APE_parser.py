from ast import Raise

from re import L
import string
from tokenize import Token

from sqlalchemy import false
from sympy import N
import settings
from settings import TokensTypes as Types



class Parser:
    def __init__(self, tokenList):
        self.tokens = tokenList
        self.tokenSize = len(self.tokens)+1
        self.nextToken = self.tokens[1]
        self.currentToken = self.tokens[0]
        self.tokenIndex = 1
        self.finished = False
        self.error = False
        self.nodes = []
        self.edges = []
        self.parseTree = []

    
    def checkCurrentTokenByType(self, tokenType):
        return self.currentToken.type == tokenType

    def checkCurrentTokenByVal(self, tokenVal):
       return self.currentToken.value == tokenVal

    def checkNextTokenByType(self, tokenType):
        return self.nextToken.type == tokenType

    def checkNextTokenByVal(self, tokenVal):
       return self.nextToken.value == tokenVal

    ## Match token     
    def match(self,foundVal, checkbyValue= False):
        # is there any tokens left?
        #print("HELLOOOOO{}".format(foundVal.name))
        if(self.currentToken.type.name != "EOF"):
            # matched or not ?
            if(checkbyValue):
                if(self.checkCurrentTokenByVal(foundVal)):
                    print("\nDone Parsing {}".format(self.currentToken.value))
                    #print("Which is  {} \n".format(self.currentToken.value))
                    # if(self.nextToken != "*EOF"):
                    #     print("next is  {}".format(self.nextToken.value))
                    self.stepOneToken()
                else:
                    raise ValueError('TokenType Mismatch', self.currentToken)
            else:
                if(self.checkCurrentTokenByType(foundVal)):
                    print("Done Parsing {}".format(self.currentToken.value))
                    #print("Which is  {}".format(self.currentToken.value))
                    # if(self.nextToken != "*EOF"):
                    #     print("next is  {}".format(self.nextToken.value))
                    self.stepOneToken()
                else:
                    
                    raise ValueError('TokenType Mismatch', self.currentToken)

        else:
            print("Finished!!!")
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
        
        if self.tokenIndex < self.tokenSize:
            self.tokenIndex += 1
            self.currentToken = self.nextToken
            self.nextToken = self.tokens[self.tokenIndex]
            #print("current token {}".format(self.currentToken.type.name))
            if(self.currentToken.type.name == "EOF"):
                self.exit()
            
            
    def parse(self):
        self.Program()

   
    def exit(self):
            print("Finished Parsing!")
    

    def statement(self):
        # #print("3 Statement")
        # print("\t current token {}".format(self.currentToken.type.name))
        # print(self.currentToken.type.name)
        # print("\t next token {}".format(self.nextToken.type.name))
        # print(self.nextToken.type.name)
        if(self.peek(Types.identifier) and self.peekNext(Types.leftbracket) == False):
            #print("Assiging Statement now!")
            return self.assignStmt()
        if(self.peek("panic",checkbyValue=True)):
            return self.printStmt()
        if(self.peek("listen", checkbyValue=True)):
            return self.listenStmt()
        if(self.peek("when",checkbyValue=True) or self.peek("within",checkbyValue=True)):
            return self.loopStmt()
        if(self.peek("routine", checkbyValue=True)):
            return self.funcDef()
        if(self.peek("familyof",checkbyValue=True)):
            return self.classDef()
        if(self.peek("return",checkbyValue=True)):
            return self.returnStmt()
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
                self.match(Types.comma)
                self.exp()
            return True
        return False
            


        ####---------------------OBJECT------------------------------------------------
    
    def obj(self):
        if(self.peek("new",checkbyValue=True)):
            self.match("new",checkbyValue=True)
            self.match(Types.identifier)
            self.matchBetweenBrackets("()",self.params,optional=True)
            while(self.peek(Types.dot)):
                self.match(Types.dot)
                self.match(Types.identifier)
                self.matchBetweenBrackets("()",self.params,optional=True)
            return True
        return False
                                    





        ####---------------------IDENTIFIER------------------------------------------------
    def identifier(self):
        #print(self.currentToken.value)
        if(self.peek(Types.identifier)):
            self.match(Types.identifier)
            if(self.peek(Types.dot)):
                self.match(Types.dot)
                if(self.peek(Types.identifier)):
                    self.match(Types.identifier)
                    if(self.peek(Types.leftbracket)):
                        self.matchBetweenBrackets("()",self.params, optional=True)
                    return True
                
            
            return True
        return False


    

        #### --------------------Operators--------------------------------------------
    def comparisonOp(self):
        if(self.peek(Types.greaterthanoperator)):
            self.match(Types.greaterthanoperator)
            return True
        elif(self.peek(Types.lessthanoperator)):
            self.match(Types.lessthanoperator)
            return True
        elif(self.peek(Types.greaterthanorequaloperator)):
            self.match(Types.greaterthanorequaloperator)
            return True
        elif(self.peek(Types.lessthanorequaloperator)):
            self.match(Types.lessthanorequaloperator)
            return True
        elif(self.peek(Types.equaloperator)):
            self.match(Types.equaloperator)
            return True
        elif(self.peek(Types.notequaloperator)):
            self.match(Types.notequaloperator)
            return True
        else:
            return False
    def multiplicationOp(self):
        if(self.peek(Types.multiplicationoperator)):
            self.match(Types.multiplicationoperator)
            return True
        elif(self.peek(Types.divisionoperator)):
            self.match(Types.divisionoperator)
            return True
        return False
    def additionOp(self):
        if(self.peek(Types.additionoperator)):
            self.match(Types.additionoperator)
            return True
        elif(self.peek(Types.subtractionoperator)):
            self.match(Types.subtractionoperator)
            return True
        return False
    def logicalOp(self):
        if(self.peek(Types.logical_operator) ):
            self.match(Types.logical_operator)
            return True
        return False

        ###----------------------------------------------------------------------------------
    ###-------------------------------EXPRESSIONS---------------------------------------------------    
    def exp(self):
        if(self.peek(Types.string)):
            self.match(Types.string)
            return True
        else:
            return self.explow()


    def explow(self):
        if(self.explowlow()):
            while(self.peek(Types.logical_operator)):
                self.logicalOp()
                self.explowlow()
            return True
        return False




    def explowlow(self):
        if(self.simpleExp()):
            #print(self.checkforComparisonOp())
            while(self.checkforComparisonOp()):
                #print(" \n inside check for comparison op while loop \n")
                self.comparisonOp()
                self.simpleExp()
            return True
        return False



    def simpleExp(self):
        if(self.term()):
            while(self.peek(Types.additionoperator) or self.peek(Types.subtractionoperator)):
                self.additionOp()
                self.term()
            return True
        return False


    def term(self):
        if(self.primaryExpr()):
            while(self.peek(Types.multiplicationoperator) or self.peek(Types.divisionoperator)):
                self.multiplicationOp()
                self.primaryExpr()
            return True
        return False

    def primaryExpr(self):
        if(self.peek(Types.number)):
            self.match(Types.number)
            return True
        elif(self.identifier()):
            #print(" \n \n \nthis is identifier!\n\n\n")
            return True
        elif(self.peek(Types.leftbracket)):
            self.match(Types.leftbracket)
            if(self.exp()):
                self.match(Types.rightbracket)
                return True
        elif(self.obj()):
            return True
        
        else:
            return False
            

    ###----------------------------------------------------------------------------------

    ###---------------------------------STATEMENTS-------------------------------------------------
    def assignStmt(self):
        if(self.identifier()):
            if(self.peek(Types.assignmentoperator)):
                self.match(Types.assignmentoperator)
                if(self.exp() or self.obj()):
                    return True
                return False


    def returnStmt(self):
        if(self.peek("return",checkbyValue=True)):
            self.match("return",checkbyValue=True)
            self.exp()
            return True
        return False

    def ifStmt(self): 
        if(self.peek("if",checkbyValue=True)):
            self.match("if",checkbyValue=True)
            self.matchBetweenBrackets("()", self.exp)
            self.matchstmtseq()
            while(self.peek("elseif",checkbyValue=True)):
                self.matchBetweenBrackets("()",self.exp)
                self.matchstmtseq()
            if(self.peek("else",checkbyValue=True)):
                self.matchstmtseq()
            return True
        return False


    def printStmt(self):
        self.match("panic",checkbyValue=True)
        if(self.peek(Types.leftbracket)):
            self.match(Types.leftbracket)
            if(self.exp()):
                self.match(Types.rightbracket)
                return True
            elif(self.obj()):
                self.match(Types.rightbracket)
                return True
        return False



    def listenStmt(self):
        if(self.peek("listen", checkbyValue=1)):
            self.match("listen",checkbyValue=True)
            self.match(Types.leftbracket)
            self.match(Types.identifier)
            self.match(Types.rightbracket)
            return True
        return False

    
        
    def loopStmt(self):
        if(self.withinLoop() or self.whenLoop()):
            return True
        return False

    def withinLoop(self):
        
        if(self.peek("within",checkbyValue=True)):
            self.match("within",checkbyValue=True)
            self.match(Types.leftbracket)
            self.assignStmt()
            self.exp()
            self.match(Types.semicolon)
            self.assignStmt()
            self.match(Types.rightbracket)
            self.matchstmtseq()

    def whenLoop(self):
        if(self.peek("when",checkbyValue=True)):
            self.match("when",checkbyValue=True)
            self.matchBetweenBrackets("()",self.exp)
            self.match("do",checkbyValue=True)
            self.matchstmtseq()
            return True
        return False
    
    def funcDef(self):
        if(self.peek("routine",checkbyValue=True)):
            self.match("routine",checkbyValue=True)
            self.match(Types.identifier)
            self.matchBetweenBrackets("()",self.params,optional=True)
            self.matchstmtseq()
            return True
        return False 
    def funcCall(self):
        if(self.peek(Types.identifier)):
            self.match(Types.identifier)
            self.matchBetweenBrackets("()",self.params,optional=True)
            return True
        return False


    def classDef(self):
        if(self.peek("familyof",checkbyValue=True)):
            self.match("familyof",checkbyValue=True)
            self.match(Types.identifier)
            if(self.peek("inherit",checkbyValue=True)):
                self.match("inherit",checkbyValue=True)
                self.match(Types.identifier)
                self.matchstmtseq()
            else:
                self.matchstmtseq()
            return True
        return False




    def Program(self):
        return self.StatementSequence()
    def StatementSequence(self):
        if(self.statement()):
            if(self.peek(Types.semicolon) == False):
                raise SyntaxError('semi color messing!')
            while(self.peek(Types.semicolon)):
                self.match(Types.semicolon)
                if(self.currentToken.type != Types.EOF and (self.currentToken.value not in [")","}","]"])):
                    self.statement()
                    #print("returned from statement")
            return True
        return False

    def matchstmtseq(self):
        self.match(Types.leftcurlybracket)
        if(self.StatementSequence()):
            self.match(Types.rightcurlybracket)

    def matchBetweenBrackets(self, bracket, tokenFunc, optional = 0):
        if(bracket == '[]'):
            self.match(Types.leftsquarebracket)
            if(tokenFunc() or optional):
                self.match(Types.rightsquarebracket)
        elif(bracket == '()'):
            self.match(Types.leftbracket)
            if(tokenFunc() or optional):
                self.match(Types.rightbracket)
        elif(bracket == '{ }'):
            self.match(Types.leftcurlybracket)
            if(tokenFunc() or optional):
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
   
    