rows = int(input("Ange antal rader: "))
columns = int(input("Ange antal kolumner: "))

column_number = 0
row_number = 0

while row_number < rows:

    #Nollställer kolumnen
    column_number = 0
    while column_number < columns:

        #Skriver ut X eller O beroende på modulus
        if (column_number + row_number) % 2 == 0:
            print("X", end = " ")

        if (column_number + row_number) % 2 == 1:
            print("O", end = " ")

        if column_number == (columns - 1):
            print()

        column_number += 1

    row_number += 1
