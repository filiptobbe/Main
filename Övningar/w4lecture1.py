print("test")

#exempel
class Katt: #stor bokstav på klassen
    color = "red"
    def säg_meow(self): #Säg meow är namnet på vår metod - VIKTIG REGEL: Första argumentet i en metod är ALLTID self
        print("Meow meow!")

    def __init__(self): #Konstruktor, __init__ är exempel på en konstruktor, vilket är en typ av konstruktor
        print("Godmorgon! Jag har skapats")

k1 = Katt()
k1.säg_meow()

#Exempel två

class Bil:
    def __init__(self, modell_input, färg_input):
        print("Vi har skapat ett bil-objekt!")
        self.modell = modell_input #Definiera attribut och lägger in ett värde "modell"
        self.färg = färg_input

    def honk(self):
        print("Tut tut!")

bil1 = Bil("Volvo", "Röd")
bil1.honk() #Anropar metoden



#Exempel uppgift

class Katt:
    def __init__(self, färg_input, namn_input):
        self.färg = färg_input
        self.namn = namn_input

    def __str__(self): #använd till labben
        return f"{self.färg}, {self.namn}"

katt1 = Katt("grön", "Peter")
katt2 = Katt("orange", "Potatis")
katt3 = Katt("blå", "Plupp")
print(f"{katt1}\n{katt2}")

print(katt1.namn) #Ta ut attribut för katten

katt1.namn = "Lisa" #Sätter nytt värde för attributen namn

#Filhantering

attribut_data = "Vardagsrums TV, 100, 22, 100,9"
with open("data.txt", "w") as fil:
    fil.write("Vardagsrums TV, 100, 22, 100,9" + "\n" + "NY RAD")
    fil.close() #stänger filen


try:
    min_fil = open("data.txt", "r") #argument: filnamn och integreringstyper. Enklast att ha textfilen och koden i samma mapp
    #Välj mellan "r" read, "a" append, "w" write (skriver över), "x" create
    for line in min_fil:
        clean_line = line.strip()  #Ta bort \n
        attribute_list = clean_line.split(",")
        print(attribute_list)
except:
    #Skapa en ny fil
    open("kalleanka.txt", "x").close()
    print("Filen finns inte")


#Nästa: tvskärm klass, objekt för varje skräm
#Varje rad, en specifik tv

#Gör varje rad till en lista
#Behöver typ inte try exept för om den inte existerar skapas en ny fil


