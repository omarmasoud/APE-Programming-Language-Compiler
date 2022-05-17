from email import parser
from APEScanner import *
from APE_parser import Parser
from APE_Compiler import Compiler
from APEScanner import scanner
from anytree import RenderTree,Node





testcase1 = "familyof Dog {name := 2; breed := 1;age := 0; color := 3; routine dog(Name, Breed, Age, Color){name := Name; breed := Breed; age := Age; color := Color;}; OU GETTERS UO routine getName(){return name;};routine getBreed(){return breed;};routine getColor(){return color;}; routine getAge() {return age;}; OU SETTERS UO routine setName(Name){name := Name;};routine setBreed(Breed){breed := Breed;};routine setColor(Color){color := Color;};routine setAge(Age){age := Age;}; };dog1 := new Dog();panic(dog1.name);panic(dog1.breed);dog1.setName(4);panic(dog1.name);"
code2 = "square.length := square.getwidth()"

whenloop = "when( x > 3)  do{ x := 3;  };"
withinloop = "within (i:=1; i = 10 ; i := i + 1 ; ) { x := x + i ; within (j:=1; j = 10 ; j := j + 1 ; ) { y := y + i ;  }; };"
var = "listen(x); x:=x+2;"

c = Compiler(withinloop)







