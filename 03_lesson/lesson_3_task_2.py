from smartphone import Smartphone

catalog = [
    Smartphone("Apple", "iPhone 14", "+79161234567"),
    Smartphone("Samsung", "Galaxy S23", "+79261234567"),
    Smartphone("Xiaomi", "13 Pro", "+79361234567"),
    Smartphone("Google", "Pixel 7", "+79461234567"),
    Smartphone("OnePlus", "11 Pro", "+79561234567")
]

for phone in catalog:
    print(f"{phone.brand} - {phone.model}. {phone.phone_number}")