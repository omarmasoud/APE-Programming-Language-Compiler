class Dog:
	def __init__(self,name,breed,age,color):
		self.name=name
		self.breed=breed
		self.age=age
		self.color=color
	def getName(self,):
		return self.name
	def getBreed(self,):
		return self.breed
	def getColor(self,):
		return self.color
	def getAge(self,):
		return self.age
	def setName(self,Name):
		self.name=Name
	def setBreed(self,Breed):
		self.breed=Breed
	def setColor(self,Color):
		self.color=Color
	def setAge(self,Age):
		self.age=Age
dog1=Dog("Kovu","German Shepherd",2,"Brown")
print(dog1.name)
print(dog1.breed)
dog1.setName("Kovo")
print(dog1.name)
