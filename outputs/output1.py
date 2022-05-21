def drawPyramid(n):
	s=""
	star="*"
	nextline="\n"
	i=0
	while((i<=n)):
		j=1
		while((j<=i)):
			s=s+star
			j=j+1
		s=s+nextline
		i=i+1
	print(s)
drawPyramid(10)