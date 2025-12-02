mileage = float(input("Ange körsträcka i km: "))
fuel = float(input("Ange förbrukat bränsle i liter: "))

#Beräkna bränsleförbrukningen
consumed_fuel = (fuel*100)/mileage

print("Bränsleförbrukningen för bilen är: " + str(round(consumed_fuel, 3)) + "l/100 km")
