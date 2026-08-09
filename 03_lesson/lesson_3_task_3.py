from Address import Address
from Mailing import Mailing

# Создаем экземпляры адресов
from_address = Address(index="190000", city="Санкт-Петербург", street="Невский проспект", house="25", apartment="10")
to_address = Address(index="119991", city="Москва", street="Тверская улица", house="30", apartment="5")

# Создаем экземпляр отправления
mailing = Mailing(
    to_address=to_address,
    from_address=from_address,
    track="1234567890",
    cost=500
)

# Распечатываем информацию об отправлении
print(f"Отправление {mailing.track} из {mailing.from_address.index}, {mailing.from_address.city}, {mailing.from_address.street}, {mailing.from_address.house} - {mailing.from_address.apartment} в {mailing.to_address.index}, {mailing.to_address.city}, {mailing.to_address.street}, {mailing.to_address.house} - {mailing.to_address.apartment}. Стоимость {mailing.cost} рублей.")