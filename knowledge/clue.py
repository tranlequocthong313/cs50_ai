import termcolor

from logic import *

mustard = Symbol("ColMustard")
plum = Symbol("ProfPlum")
scarlet = Symbol("MsScarlet")
characters = [mustard, plum, scarlet]

ballroom = Symbol("ballroom")
kitchen = Symbol("kitchen")
library = Symbol("library")
rooms = [ballroom, kitchen, library]

knife = Symbol("knife")
revolver = Symbol("revolver")
wrench = Symbol("wrench")
weapons = [knife, revolver, wrench]

symbols = characters + rooms + weapons


def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge, symbol):
            termcolor.cprint(f"{symbol}: YES", "green")
        elif not model_check(knowledge, Not(symbol)):
            print(f"{symbol}: MAYBE")


# knowledge = And(
#     Or(mustard, plum, scarlet),
#     Or(ballroom, kitchen, library),
#     Or(knife, revolver, wrench),
# )
# print(knowledge.formula())
# knowledge.add(Not(mustard))
# knowledge.add(Not(kitchen))
# knowledge.add(Not(revolver))
# print(knowledge.formula())
# knowledge.add(
#     Or(
#         Not(scarlet),
#         Not(library),
#         Not(wrench),
#     )
# )
# print(knowledge.formula())
# knowledge.add(Not(plum))
# print(knowledge.formula())
# knowledge.add(Not(ballroom))
# print(knowledge.formula())

# check_knowledge(knowledge)

knowledge = And(
    Or(mustard, scarlet, plum),
    Or(kitchen, ballroom, library),
    Or(knife, revolver, wrench),
    Not(mustard),
    Not(wrench),
    Or(Not(plum), Not(revolver), Not(ballroom)),
    Not(scarlet),
    Not(kitchen),
    Not(knife),
)
check_knowledge(knowledge)
