from TV import TV

def read_file(tv_file_input):
    try:
        #Öppnar textfilen
        with open(tv_file_input, "r") as tv_file:
            all_tv_list = []

            #Konverterar attributen till en lista
            for line in tv_file:
                # Hoppa över tomma rader
                if line.strip() == "":
                    continue

                #Dela raden vid kommatecken
                parts = line.split(",")

                #Ny lista, utan mellanslag
                cleaned_line = []
                for part in parts:
                    cleaned_line.append(part.strip())

                #Kontrollerar att formatet är korrekt (5 delar)
                if len(cleaned_line) != 5:
                    continue

                #Tar ut varje objekt
                name = cleaned_line[0]
                try:
                    max_channel = int(cleaned_line[1])
                    current_channel = int(cleaned_line[2])
                    max_volume = int(cleaned_line[3])
                    current_volume = int(cleaned_line[4])

                except ValueError:
                    #Felhantering - någon siffra gick inte att tolka
                    print("Ogiltiga tal")
                    continue

                all_tv_list.append(
                    TV(name, max_channel, current_channel, max_volume, current_volume)
                )

    except FileNotFoundError:
        #Felhantering - filen existerar inte
        print("Filen finns inte")
        all_tv_list = []

    return all_tv_list


def write_file(all_tv_list, file_name = "allatv.txt"):
    try:
        with open(file_name, "w") as file:
            #Gör om TV-objekten till strängar och lägger till de i filen
            for tv in all_tv_list:
                file.write(tv.str_for_file() + "\n")
    except FileNotFoundError:
        #Felhantering
        print("Filen finns inte")


#Byter kanal
def change_channel(selected_tv):
    try:
        #Användaren matar in
        new_channel = int(input("Ange kanalnummer: "))

        #Försöker att byta kanal
        success = selected_tv.change_channel(new_channel)

        #Låter användaren skriva in ett nytt värde och testa igen
        while success == False:
            new_channel = int(input(f"Kanal för den här TV:n ska vara mellan 1 till {selected_tv.max_channel}, försök igen: "))
            success = selected_tv.change_channel(new_channel)

    except ValueError:
        print("Fel inmatning, du måste skriva ett heltal")


#Ökar volymen
def increase_volume(selected_tv):
    #Försöker att öka volymen
    success = selected_tv.increase_volume()

    if success == False:
        print(f"Maxvolymen för den här TV:n är {selected_tv.max_volume}")


#Sänker volymen
def decrease_volume(selected_tv):
    #Försöker att sänka volymen
    success = selected_tv.decrease_volume()

    if success == False:
        print(f"Den minsta volymen för den här TV:n är 0")


def adjust_TV_menu():
    print("1. Byt kanal")
    print("2. Höj volym")
    print("3. Sänk volym")
    print("4. Återgå till huvudmenyn")

    #Användaren väljer
    while True:
        try:
            choice = int(input("Välj: "))
            #Kollar om talet är mellan 1 och 4
            if 1 <= choice <= 4:
                return choice
            else:
                print("Fel val, försök igen: ")
        except ValueError:
            print("Fel inmatning, du måste skriva ett heltal.")


def select_TV_menu(all_tv_list):
    #Skriver ut huvudmenyn (lista alla TV + Avsluta)
    i = 1
    for tv in all_tv_list:
        print(f"{i}. {tv.tv_name}")
        i += 1

    #Sista valet i menyn - avsluta
    print(f"{i}. Avsluta")

    #Användaren väljer
    while True:
        try:
            choice = int(input("Välj: "))

            #Kollar om talet är inom menyn
            if 1 <= choice < i:
                #Retunerar tv-objektet
                return all_tv_list[choice - 1]
            
            #Avsluta
            elif choice == i:
                return None                    
            else:
                print("Fel val, försök igen: ")

        except ValueError:
            print("Fel inmatning, du måste skriva ett heltal.")


def main():
    print("***Välkommen till TV-simulatorn****")

    tv_obj_list = read_file("allatv.txt")

    #Huvudloop: välj TV eller avsluta
    while True:
        selected_tv = select_TV_menu(tv_obj_list)

        if selected_tv is None:
            #Alla tv sparas ner när användaren avslutar
            write_file(tv_obj_list, "allatv.txt")
            print("Programmet avslutas")
            break

        #Visa aktuell status
        print()
        print(selected_tv.tv_name)
        print(f"Kanal: {selected_tv.current_channel}")
        print(f"Ljudnivå: {selected_tv.current_volume}")
        print()

        #Undermeny för vald TV tills användaren går tillbaka
        while True:
            choice = adjust_TV_menu()

            if choice == 1:
                change_channel(selected_tv)
            elif choice == 2:
                increase_volume(selected_tv)
            elif choice == 3:
                decrease_volume(selected_tv)
            elif choice == 4:
                #Tillbaka till huvudmenyn
                print()
                break

            #Visa status efter varje ändring
            print()
            print(selected_tv.tv_name)
            print(f"Kanal: {selected_tv.current_channel}")
            print(f"Ljudnivå: {selected_tv.current_volume}")
            print()

main()