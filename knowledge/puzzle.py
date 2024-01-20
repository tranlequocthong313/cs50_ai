import termcolor
from logic import *


students = ["Glideroy", "Minerva", "Pomona", "Horace"]
houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
symbols = []

for student in students:
    for house in houses:
        symbols.append(Symbol(f"{student}{house}"))

knowledge = And()

for i in range(0, len(symbols), min(len(students), len(houses))):
    knowledge.add(Or(*symbols[i : i + min(len(students), len(houses))]))

# Only one house per student
for student in students:
    for house in houses:
        antecedent = f"{student}{house}"
        for house2 in houses:
            consequent = f"{student}{house2}"
            if antecedent == consequent:
                continue
            else:
                knowledge.add(Implication(Symbol(antecedent), Not(Symbol(consequent))))

# Only one student per house
for student in students:
    for house in houses:
        antecedent = f"{student}{house}"
        for student2 in students:
            consequent = f"{student2}{house}"
            if antecedent == consequent:
                continue
            else:
                knowledge.add(Implication(Symbol(antecedent), Not(Symbol(consequent))))

knowledge.add(Symbol("MinervaGryffindor"))
knowledge.add(Not(Symbol("PomonaSlytherin")))
knowledge.add(Or(Symbol("GlideroyGryffindor"), Symbol("GlideroyRavenclaw")))

for symbol in symbols:
    if model_check(knowledge, symbol):
        print(symbol)
