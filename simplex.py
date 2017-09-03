import argparse
import numpy as np
import sys
total_var = 0
des_num = 0
res_num = 0
u_coef = []														#u_coef son los valores de la funcion U
res_coef = []													#res_coef son los valores de las restricciones
signed = []														#signed es el tipo de cada restriccion
min_flag = False

def getInput(input_file):										#Lee archivo de entrada, lo parsea y almacena
	global des_num, res_num, u_coef, res_coef, signed, total_var
	line_num = 0
	with open(input_file) as f:
		for line in f:
			list = line.split(',')
			if(line_num==0):
				des_num = int(list[0])
				res_num = int(list[1])
				total_var += des_num + res_num
				line_num+=1
			else :
				if(line_num==1):
					for i in range(des_num):
						u_coef.append(int(list[i]))
						line_num+=1
				else:
					aux = []
					for i in range((res_num)):
						aux.append(int(list[i]))
					res_coef.append(aux)
					listAux = list[-1].split('\n')
					if(listAux[0] == '≥'):
						total_var+=1
					signed.append(listAux[0])

def printAux():													#Imprime valores despues de leerlos y procesarlos		
	global des_num, res_num, u_coef, res_coef
	print(u_coef)
	print(res_coef)
	print(signed)
	
def makeFirstMat():												#Con los valores de entrada, crea la primera matriz para el proceso
	global des_num, res_num, u_coef, res_coef,max
	matrix = []
	aux = []
	for i in range(des_num+res_num+1):							#Primera fila
		if(i<des_num):
			if(max):
				aux.append(-u_coef[i])
			else:
				aux.append(u_coef[i])
		else:
			aux.append(0)
	matrix.append(aux)
	
	for i in range(res_num):									#resto de la matriz
		aux = []
		for j in range((des_num+res_num)):
			if(j<des_num):
				aux.append(res_coef[i][j])
			else:
				if((j-des_num)==i):
					aux.append(1)
				else:	
					aux.append(0)
		aux.append(res_coef[i][-1])								#valores limites de la restriccion
		matrix.append(aux)
	return matrix

def getMinRow(mat, new_column):									#revisa con la columna pivot, el valor menor para que sea el elemento pivot
	min = sys.maxsize
	minPos = 0
	for i in range(1,len(mat)):
		for j in range(len(mat[0])):
			if(j == new_column):				
				if(mat[i][j]>0):
					minAux = mat[i][-1]/mat[i][j]
					if(minAux<min and minAux>0):
						min = minAux
						minPos = i
	return minPos

def getNewMat(mat, pivot, row, column):							#realiza ecuaciones para generar la nueva matriz
	for i in range(len(mat[0])):								#fila entrante(posicion/pivot)
		print("pos = " +str(mat[row][i])+" pivot = "+str(pivot)+" resultado = "+str(round(mat[row][i]/pivot,2)))
		aux = mat[row][i]/pivot
		mat[row][i] = round(aux,2)
	for i in range(len(mat)):									#el resto de la matriz
		if(i != row):
			aux = -mat[i][column]
			print(aux)
			for j in range(len(mat[0])):
				print(str(aux)+" * "+str(mat[row][j])+" + "+str(mat[i][j])+" = "+str(round(aux*mat[row][j]+mat[i][j],2)))
				aux2 = aux*mat[row][j]+mat[i][j]

				mat[i][j] = round(aux2,2)

	return mat

def solve(mat):													#saca columna entrante, fila saliente y nueva matriz
	while(True):
		new_column = mat[0].argmin()
		if(mat[0][new_column]>=0):								#para el proceso

			sys.exit()
		print("Columna pivote "+str(new_column))
		last_row = getMinRow(mat,new_column)
		print("Fila pivote "+str(last_row))
		print("Pivote "+str(mat[last_row][new_column]))
		mat = getNewMat(mat, mat[last_row][new_column], last_row,new_column)
		printMat(mat)

def printMat(mat):
	for i in range(len(mat)):
		print(mat[i])

def fillMat(mat):
	global total_var

	len_u_coef = len(u_coef)
	len_res_coef = len(res_coef)
	un_assign_var = des_num

	for i in range(0, len_u_coef): 			#Llenar los coeficientes de U en la tabla
		mat[0][i] = u_coef[i] * -1
	
	for i in range(0, len_res_coef): 		#Llenar los coeficientes de las restricciones junto con 
		for j in range(0, len_u_coef + 1): 	#las variables de holgura, M y de exceso

			if(j == len_u_coef):
				mat[i+1][total_var] = res_coef[i][j]
			else:
				mat[i+1][j] = res_coef[i][j]

		if(signed[i] == '≥'): 				#Agrega la variable de exceso
			mat[i+1][un_assign_var] = -1
			un_assign_var += 1
			mat[0][un_assign_var] = -1j

		if(signed[i] == '='):
			mat[0][un_assign_var] = -1j			
		
		mat[i+1][un_assign_var] = 1
		un_assign_var += 1

	if(min_flag):
		for i in range(0, total_var + 1):
			mat[0][i] *= -1

	#modificar U si existen Ms


def main():
	'''
	global des_num, res_num, u_coef, res_coef, max
	parser = argparse.ArgumentParser(description="Programa para calcular metodo Simplex")
	parser.add_argument("input", help="Archivo de entrada para el programa")
	parser.add_argument("-o","--output", help="Archivo de salida para el programa")
	parser.add_argument("-min", help="Bandera para minimizar", action="store_true")
	parser.add_argument("-max", help="Bandera para maximizar", action="store_true")
	args = parser.parse_args()
	max = args.max
	getInput(args.input)
	printAux()
	mat = makeFirstMat()
	print(np.array(mat))
	solve(np.array(mat,dtype=float))
	'''
	global des_num, res_num, u_coef, res_coef, total_var, min_flag, mat
	parser = argparse.ArgumentParser(description="Programa para calcular metodo Simplex")
	
	parser.add_argument("input", help="Archivo de entrada para el programa")
	parser.add_argument("-min", help="Bandera para minimizar", action="store_true")
	parser.add_argument("-max", help="Bandera para maximizar", action="store_true")
	parser.add_argument("-o","--output", help="Archivo de salida para el programa")

	args = parser.parse_args()
	min_flag = args.min
	getInput(args.input)
	printAux()

	mat = np.zeros([res_num + 1, total_var + 1], dtype=np.complex)

	fillMat(mat)

	print()
	print(mat)
	#print(args.accumulate(args.integers))

main()