import csv

with open('csv/trans.asc', encoding='utf-8') as file:
    plik_csv = list(csv.reader(file, delimiter=';'))  # Wczytujemy całość do listy

    if plik_csv:  # Sprawdzamy, czy plik nie jest pusty
        x = max(map(len, [row[3] for row in plik_csv[1:]]))  # Pomijamy nagłówek
        y = max(map(len, [row[4] for row in plik_csv[1:]]))
        print(f'Max długość transaction_type: {x}, operation: {y}')
    else:
        print("Plik CSV jest pusty")
