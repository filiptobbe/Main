farenheit_list = []

for i in range(0,20):
    celsius_to_farenheit = round((((i * 9) + 160)/5), 1)
    farenheit_list.append(celsius_to_farenheit)

    if i == 0:
        print("C F")
    
    print(str(i), str(farenheit_list[i]))

