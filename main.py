from number import Number as n
import argparse
import sys
import pypandoc

vb = [] #Variables basicas
rest = 0 #numero de restricciones
decision = 0 #variables de decision
f = open('.result.md', 'w')

def getInput(input_file, min_flag):#procesa entradas
	global vb, rest, decision
	line_num = 0
	sign = []
	table = [[]]
	res = [0]
	with open(input_file) as f:
		for line in f:
			list = line.split(',')
			if(line_num == 0):
				decision = int(list[0])
				rest = int(list[1])
			if(line_num == 1):
				for x in range(len(list)):
					table[0].append(n(float(list[x]),0))
			if(line_num>1):
				aux = []
				for j in range(decision):
					aux.append(n(float(list[j]),0))
				temp = list[-1].split("\n")
				sign.append(temp[0])
				res.append(float(list[-2]))
				table.append(aux)
			line_num+=1	


	for x in range(len(sign)):
		for i in range(1,len(table)):
			table[i].append(n(0,0))

		if(sign[x] == '≤'):
			table[0].append(n(0,0))
			table[x+1][rest+x-1] = n(1,0)
			vb.append(rest+x-1)

		if (sign[x] == '='):
			table[0].append(n(0,1))
			table[x+1][rest+x-1] = n(1,0)
			vb.append(rest+x-1)

		if (sign[x] == '≥'):
			for i in range(len(table)):
				table[i].append(n(0,0))
			table[0].append(n(0,1))
			table[x+1][rest+x-1] = n(-1,0)
			table[x+1][rest+x] = n(1,0)
			vb.append(rest+x)
			rest+=1
			
	index = 0	
	for x in range(len(res)):
		table[x].append(n(res[index],0))
		index+=1

	if(min_flag == False):
		aux = n(-1,-1)
		for x in range(decision):
			table[0][x] = aux*table[0][x]
	return table


def fixRow(table, row):#auxiliar para generar la tabla
	for x in range(len(table[0])):
		table[0][x] += n(0,-table[row][x].n)
	return table



def fixM(table):#Termina de generar la tabla
	for x in range(len(table[0])):
		if(table[0][x].M == 1):
			for y in range(len(table)):
				if(table[y][x].n == 1):
					table = fixRow(table,y)
	return table

def getMin(table):#Obtiene el menor de la fila U
	min = n(0,0)
	pos = 0
	for x in range(len(table[0])-1):
		if(table[0][x]<min):
			min = table[0][x]
			pos = x
	return [min, pos]

def getPivot(table,pos):#obtiene el elemento pivote
	min = n(999999999,999999999)
	Npos = 0
	for x in range(1,len(table)):
		if(table[x][pos].n != 0 
			and (table[x][-1]/table[x][pos]) < min 
			and (table[x][-1]/table[x][pos])>n(0,0)):
			min = (table[x][-1]/table[x][pos])
			Npos = x
	return [min, Npos]

def getNewMat(table, column, row): #aplica las operaciones para hacer la nueva matriz
	aux = table[column][row]
	for x in range(len(table[column])):
		table[column][x] = table[column][x]/aux
		table[column][x].n = round(table[column][x].n , 3)
		table[column][x].M = round(table[column][x].M , 3)

	for x in range(len(table)):
		if(x != column):
			aux = table[x][row]*n(-1,-1)
			for y in range(len(table[x])):
				table[x][y].n = round(table[column][y].n*aux.n+table[x][y].n,3)
				table[x][y].M = round(table[column][y].n*aux.M+table[x][y].M,3)
				
	return table

def printState(new, out, pivot, table, case):# imprime casos intermedios
	global f
	f.write("## Estado "+str(case)+":\n")
	
	length = len(table[0])

	f.write("|")
	for x in range(1,length):
		f.write("X" + str(x) + "|")

	f.write("LD|\n")
	f.write("|")
	for x in range(1,length+1):
		f.write("--|")

	f.write("\n")

	for row in table:	
		f.write('|'.join(map(str,row)))
		f.write("\n")
	f.write("\n###### VB Entrante: "+str(new)+", VB Saliente: "+str(out)+", Numero Pivot: "+str(pivot))
	f.write("\n\n")


def solve(table): #Metodo Simplex
	global vb
	case = 0
	while(True):
		min = getMin(table)
		if(min[0]>n(-1,0)):
			return table
		pivot = getPivot(table,min[1])	

		printState(min[1]+1,vb[pivot[1]-1]+1,table[pivot[1]][min[1]],table, case)
		
		vb[pivot[1]-1] = min[1]

		table = getNewMat(table,pivot[1],min[1])		
		case += 1

	return table

def finalState(table, vb): #imprime estado final
	f.write("### Estado Final:\n")

	length = len(table[0])

	f.write("|")
	for x in range(1,length):
		f.write("X" + str(x) + "|")

	f.write("LD|\n")
	f.write("|")
	for x in range(1,length+1):
		f.write("--|")

	f.write("\n")

	for row in table:	
		f.write('|'.join(map(str,row)))
		f.write("\n")
	
	res = "Resultado Final: U = "+str(abs(table[0][-1].n))+ ", ("

	for x in range(len(table[0])-1):
		if(x in vb):
			for y in range(len(table)):
				if(table[y][x].n == 1):
					res+=str(table[y][-1])+", "
		else:
			res+= "0, "

	res+=")"
	f.write("\n#### " + res)
	f.write("\n")

def main():
	global vb, decision, f
	parser = argparse.ArgumentParser(description="Programa para calcular metodo Simplex")
	
	parser.add_argument("input", help="Archivo de entrada para el programa")
	parser.add_argument("-min", help="Bandera para minimizar", action="store_true")
	parser.add_argument("-max", help="Bandera para maximizar", action="store_true")
	parser.add_argument("-o","--output", help="Archivo de salida para el programa", default="result.pdf")
	min_flag = False
	args = parser.parse_args()
	min_flag = args.min
	outputfile = args.output

	if(not outputfile.endswith('.pdf')):
		outputfile += '.pdf'

	table = getInput(args.input, min_flag)#Procesa entrada

	table = fixM(table)#Arregla la tabla

	table = solve(table)#resuelve
	
	finalState(table,vb)#imprime el estado final
	
	f.close()

	pypandoc.convert_file('.result.md', 'pdf', outputfile=outputfile)

	
main()
