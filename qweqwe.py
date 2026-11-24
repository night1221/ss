import requests
import datetime 

response = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json")
data = response.json()

for item in data:
    if item['cc'] == 'USD':
        usd = item['rate']
        print("USD: ", usd, "  in:", datetime.datetime.now())

for item in data:
    if item['cc'] == 'EUR':
        eur = item['rate']
        print("EUR: ", eur, "  in:", datetime.datetime.now())

trt = float(input("Введіть суму в гривнях: "))
print(f"Сума в доларах: {trt / usd:.2f}")
print(f"Сума в євро: {trt / eur:.2f}")
