
quantity_packages = int(input("Hur många paket vill du skicka?"))
packages_weight_list = []
price_per_kg = [30,28,25,23]
cost_packages = 0

i = 0

#Körs en gång per paket. För varje kontrolleras priset och läggs ihop i det totala priset. 
while i < (quantity_packages):
    weight = float(input("Ange vikt för paket" + str(i+1) + ":"))
    packages_weight_list.append(weight)

    #Kontrollerar vilket pris vikten har och adderar det till den totala kostnaden av paketen
    if packages_weight_list[i] <= 2:
        cost_packages += price_per_kg[0] * packages_weight_list[i]
    elif packages_weight_list[i] <= 6:
        cost_packages += price_per_kg[1] * packages_weight_list[i]
    elif packages_weight_list[i] <= 12:
        cost_packages += price_per_kg[2] * packages_weight_list[i]
    else:
        cost_packages += price_per_kg[3] * packages_weight_list[i]   

    i += 1

cost_packages = int(cost_packages)

print("Det kommer att kosta " + str(cost_packages) + " kr")