print("Välkommen till Chomp-spelet")

rows = int(input("Hur många rader ska chokladbaren bestå av (mellan 2-9): "))  
columns = int(input("Hur många kolumner ska chokladbaren bestå av (mellan 2-9): "))

matrix = []

def create_chocolate_bar(rows, columns):
    row_number = 1

    #Skapa matrisen för chokladkakan
    while row_number <= rows:
        row_list = []
        for column_number in range(columns):
            row_list.append(str(row_number)+ str(column_number+1))
        
        #Lägg till radlistan i matrisen och nollställ radlistan
        matrix.append(row_list)
    
        row_number += 1

    return matrix

def print_chocolate_bar(matrix):

    #Skriv ut alla element i aktuell rad "row" ggr
    for row in matrix:
        print(" ".join(row))

def chomp(chomp_matrix, chomp_row_number, chomp_column_number):
    
    #Kontroll: negativa index
    if chomp_row_number < 0 or chomp_column_number < 0:
        return None

    #Om radindex är utanför matrisen
    if chomp_row_number >= len(chomp_matrix):
        return None

    #Skapa en kopia av matrisen
    new_matrix = []
    for row in chomp_matrix:
        new_matrix.append(row[:])

    #Ta bort från den angivna raden
    new_matrix[chomp_row_number] = new_matrix[chomp_row_number][:chomp_column_number]

    #Ta bort från alla rader efter
    for r in range(chomp_row_number + 1, len(new_matrix)):
        new_matrix[r] = new_matrix[r][:chomp_column_number]

    # Om det blev tomt i första raden -> hela matrisen ska vara tom
    if chomp_row_number == 0 and chomp_column_number == 0:
        return []

    return new_matrix


create_chocolate_bar(rows, columns)
print_chocolate_bar(matrix)

#Testar
print(chomp([["11", "12", "13", "14"], ["21", "22", "23", "24"], ["31", "32", "33", "34"]], 1, 2))

print(chomp([["11", "12", "13", "14", "15", "16"], ["21", "22", "23", "24", "25", "26"]], 1, 2))

print(chomp([["11", "12", "13", "14", "15", "16"], ["21", "22", "23", "24", "25", "26"]], 0, 0))

print(chomp([["11", "12", "13", "14", "15", "16"], ["21", "22", "23", "24", "25", "26"]], -1, 3))

