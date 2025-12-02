import random

number_of_dice = int(input("Hur många tärningar behövs i spelet? "))
dice_rolls = int(input("Hur många kast får en spelare? "))
dice_list = []
keep_playing = True

#Loop fortsätter tills spelaren vill avbryta
while keep_playing == True:

    user_input = input("Genom att trycka på enter kan du börja kasta, om du vill avsluta spelet skriv A:")

    #Avsluta
    if user_input.upper() == "A":
        keep_playing = False

    #Starta en tärningsserie
    if user_input == "":
        rolls_left = dice_rolls

        while (rolls_left) > 0:
            dice_list = []

            #Slumpa antalet tärningar som spelaren har valt
            for i in range(number_of_dice):
                dice_list.append(random.randint(1, 6))
                print("Tärning " + str(i + 1) + ": " + str(dice_list[-1]))

            rolls_left -= 1

            #Om spelaren har fler försök, ge alternativet att slå igen
            if rolls_left > 0:
                user_input = input("Är du inte nöjd kan du kasta igen, vill du kasta igen?(j/n) ")

                if user_input.lower() == "j":
                    keep_playing = True
            else:
                rolls_left = 0
    

            #Resultatet:
            if rolls_left == 0:
                print("Du fick", end = " ")
                
                for j in range(number_of_dice):
                    print(dice_list[-j-1], end = " ")

                    if j == (number_of_dice - 1):
                        print("\n")

print("Tack och hej!")
