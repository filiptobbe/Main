weight_package = float(input("Hur mycket väger paketet: "))

#Kontrollerar priset per kg, som varierar för de olika vikterna
if weight_package <= 2:
    price_per_kg = 30
elif weight_package <= 6:
    price_per_kg = 28
elif weight_package <= 12:
    price_per_kg = 25
else:
    price_per_kg = 23

cost_package = weight_package*price_per_kg

print("Det kommer att kosta " + str(round(cost_package, 1)) + "kr")


