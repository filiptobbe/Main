
#Kalle-Theodors e-handel

class Produkt:
    def __init__(self, kategori_input, namn_input, pris_input):
        self.kategori = kategori_input
        self.namn = namn_input
        self.pris = pris_input
    
    def __str__(self):
        return f"Kategori: {self.kategori}\n Produktnamn: {self.namn} \n Pris: {str(self.pris)}kr"

produkt1 = Produkt("Mat", "Gammal Kaviar", 20)
produkt2 = Produkt("Kläder och Skor", "Gamla Keezys", 3000)
produkt3 = Produkt("Fordon", "Gammal bil", 200000)

print(produkt2)

#Labb 5

#Varje rad representerar ett objekt, 5 attribut per

#Skriv över filen och listan till sträng (behöver inte close för W)

with open("allatv.txt", "w") as fil:
    fil.write("Whoops I have deleted content")
    tv_apparat = ",".join(["Tvnamn", 200, 22, 10, 9])
    tv_apparat2 = ",".join(["Tvnamn", 200, 22, 10, 9])
    #fil.write(tv_apparat + \n + tv_apparat2)