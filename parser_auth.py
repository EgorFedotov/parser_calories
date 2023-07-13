import json
import requests
import csv
from bs4 import BeautifulSoup

# url = 'https://health-diet.ru/table_calorie/'

headers = {
    'Accept':  '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}
# req = requests.get(url, headers=headers)
# src = req.text

# with open('index.html') as file:
#     src = file.read()

# soup = BeautifulSoup(src, 'lxml')
# all_products_hrefs = soup.find_all(class_='uk-flex mzr-tc-group-item')

# all_categories = {}
# for item in all_products_hrefs:
#     item_text = item.text
#     item_href = 'https://health-diet.ru' + item.find(class_='mzr-tc-group-item-href').get("href")
#     all_categories[item_text] = item_href

with open('all_categories.json') as file:
    all_categories = json.load(file)

iteration_count = int(len(all_categories)) - 1
count = 0
print(f'Всего итерайций: {iteration_count}')
for category_name, categoty_href in all_categories.items():
    rep = [',', ' ', '-', "'"]
    category_name = category_name.replace('\n', '')
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, '_')
    req = requests.get(url=categoty_href, headers=headers)
    src = req.text
    with open(f'data/{count}_{category_name}.html', 'w') as file:
        file.write(src)
    with open(f'data/{count}_{category_name}.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    alert_block = soup.find(class_='uk-alert uk-alert-danger')
    if all_categories is not None:
        continue

    table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')

    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f'data/{count}_{category_name}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )

    products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')
    for item in products_data:
        product_tds = item.find_all('td')
        title = product_tds[0].text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text

        with open(f'data/{count}_{category_name}.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )
    count += 1
