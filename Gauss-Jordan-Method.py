#
# Por: Andrés Garcia Alves de Borba
#
# Resolución de Ecuaciones Lineales, mediante método de Gauss-Jordan
# Algoritmo de elaboración propia, v1.0: hardcodeado a matrix de 3x3 
#

import numpy as np

#
# Construir una Matriz Aumentada en base a una matriz de Coef. + un array con los Términos Indep.
#
def buildFullMatrix(coefficients: np.matrix, indepTerms: np.array):
    rows = len(coefficients)
    cols = len(coefficients[0]) + 1
    
    matrix = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            if j < cols - 1:
                matrix[i][j] = coefficients[i][j]
            else:
                matrix[i][j] = indepTerms[i]

    return matrix


#
# Mostrar la matriz recibida en forma tabulada
#
def convertFullMatrixToText(matrix: np.matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    textLine = ""
    output = ""

    for i in range(rows):
        
        textLine = "   ["
        for j in range(cols):
            item = matrix[i][j]
            if j != cols - 1:
                textLine += "{0:4.2f}".format(item).rjust(10)
            else:
                textLine += "  =" + "{0:4.2f}".format(item).rjust(10)

        textLine += " ]"
        output += textLine + "\n"

    return output.rstrip()


#
# Orden por el cual poner a cero las celdas de la matriz
# v1.0: hardcodeado a matrix de 3x3
#
def buildProcessingCoords(matrix: np.matrix):
    matrix = np.zeros((6, 2))

    # primero bajo la diagonal principal
    matrix[0] = [3, 1] # fila 3, col 1
    matrix[1] = [2, 1] # fila 2, col 1
    matrix[2] = [3, 2] # fila 3, col 2

    # luego sobre la diagonal principal
    matrix[3] = [1, 3] # fila 1, col 3
    matrix[4] = [2, 3] # fila 2, col 3
    matrix[5] = [1, 2] # fila 1, col 2

    return matrix


#
# Mostrar la matriz recibida como una lista de pares de valores
#
def convertProcessingCoordsToText(matrix: np.matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    textLine = "   "

    for i in range(rows):
        textLine += "("
        
        for j in range(cols):
            textLine += "" if j == 0 else ","
            textLine += "{0:1.0f}".format(matrix[i][j])
        textLine += ") "

    return textLine


#
# Coordenadas de la celda a procesar, según el orden recibido
#
def getCellCoordinates(matrix: np.matrix, order: int):
    return int(matrix[order][0]), int(matrix[order][1])


#
# Procesar una fila contra otra, llevando a cero la "celda" dada
#
def processRows(targetRow: np.array, otherRow: np.array, indexCol: int):

    targetFactor = targetRow[indexCol]
    otherFactor = otherRow[indexCol]

    # debug:
    # print("targetFactor: {0}, otherFactor: {1}".format(targetFactor, otherFactor))
    # print(otherFactor * targetRow)
    # print(targetFactor * otherRow)

    # se realiza una operacion del tipo:
    # X veces la fila_1 menos Y veces la fila_2, aplicando el resultado a la fila_1
    return (otherFactor * targetRow) - (targetFactor * otherRow)


#
# Extraer los valores independientes de la matriz recibida
#
def extractIndepTerms(matrix: np.matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    output = np.ones(rows)

    for i in range(rows):
        output[i] = matrix[i][cols - 1]

    return output


#
# Lógica principal
#
def main():

    print()

    # el sistema de ecuaciones a resolver
    coefficients = np.array([[2, 3, -5], [-3, 2, -1], [1, -3, 2]])
    indepTerms = np.array([2, 3, 1])

    print("Resolver el sistema de ecuaciones lineales:")
    fullMatrix = buildFullMatrix(coefficients, indepTerms)
    print(convertFullMatrixToText(fullMatrix), "\n\n")

    print("Orden de las celdas por el cual llevar a cero la matriz (fila, columna):")
    processingOrder = buildProcessingCoords(fullMatrix)
    print(convertProcessingCoordsToText(processingOrder), "\n\n")

    print("Algoritmo de Gauss-Jordan: \n")
    for order in range(len(processingOrder)):

        # la celda a llevar a cero
        indexRow, indexCol = getCellCoordinates(processingOrder, order)
        print("   - procesando celda ({0},{1}):".format(indexRow, indexCol))
        
        # adaptar indices, ya que en Python estos empiezan desde la posición cero
        indexRow = indexRow - 1
        indexCol = indexCol - 1

        # filas a operar entre sí
        targetRow = fullMatrix[indexRow]
        otherRow = fullMatrix[indexCol]
        
        # procesar la fila
        newRow = processRows(targetRow, otherRow, indexCol)
        fullMatrix[indexRow] = newRow

        # mostrar avances
        fullMatrixText = convertFullMatrixToText(fullMatrix)
        print(fullMatrixText, "\n")

    print()
    print("Resultados:")
    resultDiagonal = np.diagonal(fullMatrix)
    resultIndepTerms = extractIndepTerms(fullMatrix)
    print(resultIndepTerms / resultDiagonal)

# Punto de ingreso
main()
