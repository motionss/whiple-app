import pandas as pd
from bs4 import BeautifulSoup
import json
import re
import cloudscraper
import time
import random


cars = ['https://www.ultimatespecs.com/car-specs/Alfa-Romeo',
        'https://www.ultimatespecs.com/car-specs/Aston-Martin',
        'https://www.ultimatespecs.com/car-specs/Audi',
        'https://www.ultimatespecs.com/car-specs/BMW',
        'https://www.ultimatespecs.com/car-specs/BMW-Isetta',
        'https://www.ultimatespecs.com/car-specs/Bugatti',
        'https://www.ultimatespecs.com/car-specs/Chevrolet',
        'https://www.ultimatespecs.com/car-specs/Citroen',
        'https://www.ultimatespecs.com/car-specs/Dodge',
        'https://www.ultimatespecs.com/car-specs/Ferrari',
        'https://www.ultimatespecs.com/car-specs/Fiat',
        'https://www.ultimatespecs.com/car-specs/Ford',
        'https://www.ultimatespecs.com/car-specs/Honda',
        'https://www.ultimatespecs.com/car-specs/Hyundai',
        'https://www.ultimatespecs.com/car-specs/Koenigsegg',
        'https://www.ultimatespecs.com/car-specs/Lamborghini',
        'https://www.ultimatespecs.com/car-specs/Mazda',
        'https://www.ultimatespecs.com/car-specs/McLaren',
        'https://www.ultimatespecs.com/car-specs/Mercedes-Benz',
        'https://www.ultimatespecs.com/car-specs/Mitsubishi',
        'https://www.ultimatespecs.com/car-specs/Nissan',
        'https://www.ultimatespecs.com/car-specs/Peugeot',
        'https://www.ultimatespecs.com/car-specs/Porsche',
        'https://www.ultimatespecs.com/car-specs/Renault',
        'https://www.ultimatespecs.com/car-specs/Toyota',
        'https://www.ultimatespecs.com/car-specs/Volkswagen',
        'https://www.ultimatespecs.com/car-specs/Volvo']

car_of_the_day = random.choice(cars)

manufacturer = car_of_the_day.split("/")[-1]
link = "https://www.ultimatespecs.com"
scraper = cloudscraper.create_scraper(delay=10)
info = scraper.get(car_of_the_day).text
soup = BeautifulSoup(info, "html.parser")
models = soup.find("div", {"class": "col-md-8 col-md-pull-4"})
models = models.find_all("a", {"class": "col-md-3 col-sm-4 col-xs-4 col-6"})
models = [model.get("href") for model in models]
models = [link + model for model in models]

car_of_the_day = random.choice(models)

info = scraper.get(car_of_the_day).text
soup = BeautifulSoup(info, "html.parser")
body = soup.find("div", {"class": "right_column"})
if body.text == '\n':
    print("No versions available")
    info = scraper.get(car_of_the_day).text
    soup = BeautifulSoup(info, "html.parser")
    body = soup.find("div", {"id": "verions"})
    car_name = soup.find("div", {"class": "page_title_text"}).text
    car_name = car_name.replace('Specs', '').strip()
    car_name = car_name.replace(manufacturer, '').strip()
    production_years = re.findall('Production years:(.*?)<i', info)[0]
    production_years = production_years.replace('</b>', '')
    production_years = production_years.replace('<br />', '').strip()
    print(car_of_the_day)
    table_cars = body.find("table", {"class": "table_versions"})
    table_cars = table_cars.find_all("a")
    next_car = [car.get("href") for car in table_cars]
    next_car = [car for car in next_car if car != '#']
    shorter_car = next_car[0]
    for i in next_car:
        if len(shorter_car) > len(i):
            shorter_car = i
    next_car = shorter_car
    info = scraper.get(link + next_car).text
    soup = BeautifulSoup(info, "html.parser")
    next_car_name = soup.find("span", {"itemprop": "name"}).text
    table1 = pd.read_html(info)[0]
    table2 = pd.read_html(info)[3]
    if 'Top Speed :' not in table2[0].keys():
        table2 = pd.read_html(info)[3]
    engine = table1.loc[table1[0] == 'Engine type - Number of cylinders :', 1]
    engine = engine.values[0]
    traction = table1.loc[table1[0] ==
                          'Drive wheels - Traction - Drivetrain :', 1]
    traction = traction.values[0]
    top_speed = table2.loc[table2[0] == 'Top Speed :', 1]
    top_speed = top_speed.values[0]
    gallery = soup.find("div", {"id": "car_image"})
    gallery = gallery.find("a")['href']
    info = scraper.get(link + gallery).text
    soup = BeautifulSoup(info, "html.parser")
    car_image_link = soup.find("a", {"class": "tol"}).get("href")
    info = scraper.get(car_image_link)
    soup = BeautifulSoup(info.text, "html.parser")
    car_image = soup.find("div", {"class": "swiper-slide"})
    car_image = car_image.find("img").get("src")
    car_image = car_image.replace('/', '')
    print('termine en el if')
else:
    versions = body.find_all(
        "a", {"class": "col-md-3 col-sm-4 col-xs-4 col-4"})
    versions = [version.get("href") for version in versions]
    versions = [link + version for version in versions]
    car_of_the_day = random.choice(versions)

info = scraper.get(car_of_the_day).text
soup = BeautifulSoup(info, "html.parser")
body = soup.find("div", {"id": "verions"})
car_name = soup.find("div", {"class": "page_title_text"}).text
car_name = car_name.replace('Specs', '').strip()
car_name = car_name.replace(manufacturer, '').strip()
production_years = re.findall('Production years:(.*?)<i', info)[0]
production_years = production_years.replace('</b>', '')
production_years = production_years.replace('<br />', '').strip()
print(car_of_the_day)
table_cars = body.find("table", {"class": "table_versions"})
table_cars = table_cars.find_all("a")
next_car = [car.get("href") for car in table_cars]
next_car = [car for car in next_car if car != '#']
shorter_car = next_car[0]
for i in next_car:
    if len(shorter_car) > len(i):
        shorter_car = i
next_car = shorter_car
info = scraper.get(link + next_car).text
soup = BeautifulSoup(info, "html.parser")
next_car_name = soup.find("span", {"itemprop": "name"}).text
table1 = pd.read_html(info)[0]
table2 = pd.read_html(info)[3]
if 'Top Speed :' not in table2[0].keys():
    table2 = pd.read_html(info)[3]
engine = table1.loc[table1[0] == 'Engine type - Number of cylinders :', 1]
engine = engine.values[0]
traction = table1.loc[table1[0] == 'Drive wheels - Traction - Drivetrain :', 1]
traction = traction.values[0]
top_speed = table2.loc[table2[0] == 'Top Speed :', 1]
top_speed = top_speed.values[0]
gallery = soup.find("div", {"id": "car_image"})
gallery = gallery.find("a")['href']
info = scraper.get(link + gallery).text
soup = BeautifulSoup(info, "html.parser")
car_image_link = soup.find("a", {"class": "tol"}).get("href")
info = scraper.get(car_image_link)
soup = BeautifulSoup(info.text, "html.parser")
car_image = soup.find("div", {"class": "swiper-slide"})
car_image = car_image.find("img").get("src")
car_image = car_image.replace('/', '')

car = {'manufacturer': manufacturer,
       'model': car_name,
       'production_years': production_years,
       'car_image': car_image,
       'next_guess': {
           'name': next_car_name,
           'engine': engine,
           'traction': traction,
           'top_speed': top_speed
       }}

response = {
    "statusCode": 200,
    "headers": {},
    "body": json.dumps(car)
}

print(car)
