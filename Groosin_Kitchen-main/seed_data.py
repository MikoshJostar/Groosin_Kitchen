import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "georgian_restaurant.settings")
django.setup()

from restaurant.models import Category, FoodItem

khinkali, _ = Category.objects.get_or_create(name="Хінкалі", defaults={"order": 1})
khachapuri, _ = Category.objects.get_or_create(name="Хачапурі", defaults={"order": 2})
salads, _ = Category.objects.get_or_create(name="Салати та закуски", defaults={"order": 3})
drinks, _ = Category.objects.get_or_create(name="Напої", defaults={"order": 4})

items = [
    dict(category=khinkali, name="Хінкалі з телятиною",
         description="Соковиті хінкалі ручної роботи з ароматним бульйоном усередині.",
         price=180, is_available=True, is_spicy=False),
    dict(category=khinkali, name="Хінкалі з грибами",
         description="Вегетаріанська версія улюбленої страви з лісовими грибами.",
         price=160, is_available=True, is_vegetarian=True),
    dict(category=khachapuri, name="Хачапурі по-аджарськи",
         description="Човник з розплавленим сиром і яйцем зверху — класика Батумі.",
         price=220, is_available=True, is_vegetarian=True),
    dict(category=khachapuri, name="Хачапурі по-мегрельськи",
         description="Кругла хачапурі з подвійним шаром сиру.",
         price=210, is_available=False, is_vegetarian=True),
    dict(category=salads, name="Салат Пхалі",
         description="Шпинат, волоський горіх, гранат і грузинські спеції.",
         price=140, is_available=True, is_vegetarian=True),
    dict(category=salads, name="Аджапсандалі",
         description="Тушковані баклажани, перець і томати з часником.",
         price=150, is_available=True, is_spicy=True, is_vegetarian=True),
    dict(category=drinks, name="Тархун домашній",
         description="Освіжаючий трав'яний лимонад зі смаком тархуну.",
         price=70, is_available=True),
    dict(category=drinks, name="Грузинське вино Сапераві",
         description="Насичене червоне сухе вино з виноградників Кахетії.",
         price=250, is_available=True),
]

for data in items:
    FoodItem.objects.get_or_create(name=data["name"], defaults=data)

print("Categories:", Category.objects.count())
print("Items:", FoodItem.objects.count())
