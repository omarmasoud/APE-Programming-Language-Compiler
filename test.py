from email import parser
from unittest import TestCase
from APE.APEScanner import *
from APE.APE_parser import Parser
from APE.APE_Compiler import Compiler
from APE.APEScanner import scanner


import subprocess


testcase1 = "familyof Dog { routine init() {name := 2; breed := 1;age := 0; color := 3;}; routine dog(Name, Breed, Age, Color){name := Name; breed := Breed; age := Age; color := Color;}; OU GETTERS UO routine getName(){return name;};routine getBreed(){return breed;};routine getColor(){return color;}; routine getAge() {return age;}; OU SETTERS UO routine setName(Name){name := Name;};routine setBreed(Breed){breed := Breed;};routine setColor(Color){color := Color;};routine setAge(Age){age := Age;}; };dog1 := new Dog();panic(dog1.name);panic(dog1.breed);dog1.setName(4);panic(dog1.name);"
code2 = "square.length := square.getwidth()"

whenloop = "when( x > 3)  do{ x := 3;  };"
withinloop = "within (i:=1; i = 10 ; i := i + 1 ; ) { x := x + i ; within (j:=1; j = 10 ; j := j + 1 ; ) { y := y + i ;  }; };"
var = "listen(x); panic(x);"

testcase2 = "x:=1; when(x<10) do {x:=x+1; panic(\"hello ya shabab\");}; "
testcae4 = "hello.length.width"
testcase3 = "familyof math{routine init(number1,number2) {number1 := number1; number2 := number2;}; routine setNum1(num1){number1 := num1;};routine setNum2(num2){number2 := num2;}; routine getnum1(num1){return number1;}; routine exec(x){if(x>10){panic(\"x is greater then 10\");}; when(x<10)do{x:=x+1; listen(y); panic(y);}; };}; mat:= new math(1,2); mat.exec(12)"
c = Compiler()
c.compile(testcase2)








