class math:
	def __init__(self,number1,number2):
		self.number1=number1
		self.number2=number2
	def setNum1(self,num1):
		self.number1=num1
	def setNum2(self,num2):
		self.number2=num2
	def getnum1(self,num1):
		return self.number1
	def exec(self,x):
		if ((x>10)):
			print("x is greater then 10")
		while((x<10)):
			x=x+1
			y = input() 
			print(y)
mat=math(1,2)
mat.exec(12)
