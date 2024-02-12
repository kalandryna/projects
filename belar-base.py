from cs50 import SQL
import csv


with open("zyvioly-csv.csv") as file:
    reader = csv.DictReader(file, delimiter=';')
    data = []
    for row in reader:
        data.append(row)

db = SQL("sqlite:///mybase.db")

for row in data:
    db.execute("INSERT INTO zyvioly (назва, катэгорыя, падказка) VALUES (?,?,?)", row['назва'], row['катэгорыя'], row['падказка'])
