import enum
import string

class scanner:
    def __init__(self) :
        self.__scanningIndex=0
        self.__linenumber=1
        self.__reserved_keywords=['new','if','else','elseif','return',\
                                'familyof','inherit','panic','listen',\
                                'routine','when','within','do','break']

        self.__special_characters=['(',')','{','}','[',']',';','.',':']

        self.__arithmetic_operators=['+','-','*','/']

        self.__comparison_operators=['>','<','=','!']

        self.__logical_operators=['and','or','not']

        self.__numbers=list()
        for i in range(0,10):
            self.__numbers.append(str(i))
        print('numbers are')
        print(self.__numbers)

        self.__letters=list(string.ascii_letters)

        self.__State=ScanningState.Start

        self.__tokens=list()
    def getTokensList(self):
        return self.__tokens

    def scan(self,code:str):
        tokenvalue=''
        tokentype=''
        print('code length is  {}'.format(len(code)))
        while (self.__scanningIndex<len(code)):
            print('scanning at character index {} at line {} '.format(self.__scanningIndex,self.__linenumber))
            if self.__State==ScanningState.Start:
                if code[self.__scanningIndex] in self.__numbers:
                    self.__State=ScanningState.Number

                elif code[self.__scanningIndex] in self.__letters:
                    self.__State=ScanningState.Identifier

                elif code[self.__scanningIndex] == '"':
                    self.__State=ScanningState.String

                elif code[self.__scanningIndex] == ':':
                    self.__State=ScanningState.Assign

                elif code[self.__scanningIndex] == '\n':
                    self.__scanningIndex+=1
                    self.__linenumber+=1
                    self.__State=ScanningState.Start

                elif code[self.__scanningIndex] == ' ':
                    self.__scanningIndex+=1
                    self.__State=ScanningState.Start

                else:
                    self.__State=ScanningState.Other


            elif self.__State==ScanningState.End:
                #resetting tokenizer values
                tokenvalue=''
                tokentype=''
                self.__State=ScanningState.Start
            elif self.__State==ScanningState.Identifier:
                if len(code)-self.__scanningIndex>1:# guard condition in order not to scan out of boundary
                    if((code[self.__scanningIndex]in ['o','O'])\
                        and (code[self.__scanningIndex]in ['u','U'])): # checking for comments
                        self.__State=ScanningState.Comment
                        self.__scanningIndex+=2
                    else:
                        while((self.__scanningIndex<len(code)) and \
                            ((code[self.__scanningIndex] in self.__letters )\
                            or(code[self.__scanningIndex] in self.__numbers ))):#within the allowed identifier range

                            tokenvalue+=code[self.__scanningIndex]
                            self.__scanningIndex+=1
                        if tokenvalue.lower() in self.__reserved_keywords:
                            tokentype='reserved_keyword'
                        elif tokenvalue.lower() in self.__logical_operators:
                            tokentype='logical_operator'
                        else:
                            tokentype='identifier'

                        self.__tokens.append(Token(Tokentype=tokentype,value=tokenvalue))

                        self.__State=ScanningState.End

            elif self.__State==ScanningState.Number:
                while((self.__scanningIndex<len(code)) and \
                      (code[self.__scanningIndex] in self.__numbers)):

                        tokenvalue+=code[self.__scanningIndex]
                        self.__scanningIndex+=1
                #decimal numbers
                if (self.__scanningIndex<len(code) and code[self.__scanningIndex] == '.'):

                    tokenvalue+='.'
                    self.__scanningIndex+=1

                    while((self.__scanningIndex<len(code)) and \
                      (code[self.__scanningIndex] in self.__numbers)):

                        tokenvalue+=code[self.__scanningIndex]
                        self.__scanningIndex+=1
                tokentype='number'

                self.__tokens.append(Token(Tokentype=tokentype,value=tokenvalue))

                self.__State=ScanningState.End

            elif self.__State==ScanningState.Assign:
                if(len(code)-self.__scanningIndex>1):
                    if(code[self.__scanningIndex+1]=='='):

                        tokenvalue=':='

                        tokentype='assignmentoperator'

                        self.__scanningIndex+=2

                        self.__tokens.append(Token(Tokentype=tokentype,value=tokenvalue))

                        self.__State=ScanningState.End

                    else:
                        raise('Error at line {} expected = after : but not found'.format(self.__linenumber))
                else:
                    raise('Error at line {} expected = after : but not found'.format(self.__linenumber))

            elif self.__State==ScanningState.String:
                self.__scanningIndex+=1

                tokenvalue='"'

                while((self.__scanningIndex<len(code)) and code[self.__scanningIndex]!='"'):
                    tokenvalue+=code[self.__scanningIndex]
                    self.__scanningIndex+=1

                tokenvalue+='"'

                tokentype='string'

                self.__tokens.append(Token(Tokentype=tokentype,value=tokenvalue))

                self.__State=ScanningState.End

            elif self.__State==ScanningState.Comment:
                commentstart=self.__linenumber
                commentclosed=False
                while((self.__scanningIndex<len(code)-1)):
                    if(code[self.__scanningIndex]=='\n'):

                        self.__linenumber+=1

                    if((code[self.__scanningIndex]in ['u','U'])\
                        and (code[self.__scanningIndex]in ['o','O'])): # checking for comments endings
                        commentclosed=True
                    self.__scanningIndex+=1
                if(not commentclosed):
                    raise ('comment started at {} was not closed and left open till {}'\
                        .format(commentstart,self.__linenumber))
                else:
                    self.__State=ScanningState.End

            elif self.__State==ScanningState.Other:
                positionedcharacter=code[self.__scanningIndex]
                if positionedcharacter in self.__special_characters:
                    if positionedcharacter==';':
                        tokentype='semicolon'
                    elif positionedcharacter=='.':
                        tokentype='dot'
                    elif positionedcharacter=='{':
                        tokentype='leftcurlybracket'
                    elif positionedcharacter=='}':
                        tokentype='rightcurlybracket'
                    elif positionedcharacter=='(':
                        tokentype='leftbracket'
                    elif positionedcharacter==')':
                        tokentype='rightbracket'
                    elif positionedcharacter=='[':
                        tokentype='leftsquarebracket'
                    elif positionedcharacter==']':
                        tokentype='rightsquarebracket'

                    self.__scanningIndex+=1
                    tokenvalue=positionedcharacter
                    self.__tokens.append(Token(Tokentype=tokentype,value=tokenvalue))

                elif positionedcharacter in self.__arithmetic_operators:
                    if positionedcharacter=='+':
                        tokentype='additionoperator'
                    elif positionedcharacter=='-':
                        tokentype='subtractionoperator'
                    elif positionedcharacter=='*':
                        tokentype='multiplicationoperator'
                    elif positionedcharacter=='/':
                        tokentype='divisionoperator'
                    pass
                    self.__scanningIndex+=1
                    tokenvalue=positionedcharacter
                    self.__tokens.append(Token(Tokentype=tokentype,value=positionedcharacter))

                elif positionedcharacter in self.__comparison_operators:
                    if positionedcharacter=='=':
                        tokenvalue='='
                        tokentype='equaloperator'
                    elif positionedcharacter=='!':
                        if(self.__scanningIndex+1<len(code)):
                            if(code[self.__scanningIndex+1]=='='):
                                tokenvalue='!='
                                tokentype='notequaloperator'
                                self.__scanningIndex+=2
                        else:
                            raise('at line {} expected = after !'.format(self.__linenumber))
                    elif positionedcharacter=='<':
                        tokenvalue='<'
                        tokentype='lessthanoperator'
                        if(self.__scanningIndex+1<len(code)):
                            if(code[self.__scanningIndex+1]=='='):
                                tokenvalue+='='
                                tokentype='lessthanorequaloperator'
                                self.__scanningIndex+=2
                            else:
                                self.__scanningIndex+=1
                    elif positionedcharacter=='>':
                        tokenvalue='>'
                        tokentype='greaterthanoperator'
                        if(self.__scanningIndex+1<len(code)):
                            if(code[self.__scanningIndex+1]=='='):
                                tokenvalue+='='
                                tokentype='greaterthanorequaloperator'
                                self.__scanningIndex+=2
                            else:
                                self.__scanningIndex+=1
                    self.__tokens.append(Token(Tokentype=tokentype,value=tokenvalue))
                    self.__State=ScanningState.End

                else:
                    raise('unexpected character {}'.format(code[self.__scanningIndex]))
                self.__State=ScanningState.End


    def resetScanner(self):
        self.__scanningIndex=0
        self.__linenumber=1
        self.__State=ScanningState.Start


class ScanningState(enum.Enum):
    Start=0#done
    End=1#done
    Identifier=2#done
    String=3#done
    Number=4#done
    Assign=5#done
    Comment=6#done
    Other=7
    Error=8


class Token:
    def __init__(self,Tokentype,value):
        self.type=Tokentype
        self.value=value
    def __str__(self):
        return 'Token of type {} and value {}'.format(self.type,self.value)
st='omar12  lala when else familyof 1.2222  panic listen within when do ; and or [ } ( := !='
myscanner=scanner()
myscanner.scan(st)
ls=myscanner.getTokensList()
print(type(ls))

for i in range(len(ls)):
    print(ls[i])





