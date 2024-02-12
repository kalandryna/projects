from cs50 import SQL
import csv


with open("new.csv") as file:
    reader = csv.DictReader(file, delimiter=';')
    data = []
    for row in reader:
        data.append(row)

db = SQL("sqlite:///mybase.db")

for row in data:
    db.execute("INSERT INTO animals_rus (animal, category, hint) VALUES (?,?,?)", row['animal'], row['category'], row['hint'])

