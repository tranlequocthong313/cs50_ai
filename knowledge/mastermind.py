from logic import *

colors = ["red", "green", "blue", "yellow"]
positions = ["0", "1", "2", "3"]
symbols = []

for color in colors:
    for position in positions:
        symbols.append(Symbol(f"{color}{position}"))

knowledge = And()

for i in range(0, len(symbols), 4):
    knowledge.add(Or(*symbols[i : i + 4]))

# Only one position per color
for color in colors:
    for position in positions:
        antecedent = Symbol(f"{color}{position}")
        for position2 in positions:
            consequent = Symbol(f"{color}{position2}")
            if antecedent == consequent:
                continue
            else:
                knowledge.add(Implication(antecedent, Not(consequent)))


# Only one color per position
for color in colors:
    for position in positions:
        antecedent = Symbol(f"{color}{position}")
        for color2 in colors:
            consequent = Symbol(f"{color2}{position}")
            if antecedent == consequent:
                continue
            else:
                knowledge.add(Implication(antecedent, Not(consequent)))

knowledge.add(
    Or(
        And(
            Symbol("red0"),
            Symbol("blue1"),
            Not(Symbol("green2")),
            Not(Symbol("yellow3")),
        ),
        And(
            Symbol("red0"),
            Symbol("green2"),
            Not(Symbol("blue1")),
            Not(Symbol("yellow3")),
        ),
        And(
            Symbol("red0"),
            Symbol("yellow3"),
            Not(Symbol("blue1")),
            Not(Symbol("green2")),
        ),
        And(
            Symbol("blue1"),
            Symbol("green2"),
            Not(Symbol("red0")),
            Not(Symbol("yellow3")),
        ),
        And(
            Symbol("blue1"),
            Symbol("yellow3"),
            Not(Symbol("red0")),
            Not(Symbol("green2")),
        ),
        And(
            Symbol("green2"),
            Symbol("yellow3"),
            Not(Symbol("red0")),
            Not(Symbol("blue1")),
        ),
    )
)

knowledge.add(
    And(
        Not(Symbol("blue0")),
        Not(Symbol("red1")),
        Not(Symbol("green2")),
        Not(Symbol("yellow3")),
    )
)

for symbol in symbols:
    if model_check(knowledge, symbol):
        print(symbol)
