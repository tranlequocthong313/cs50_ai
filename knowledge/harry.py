from logic import *

rain = Symbol("rain")  # It is raining
hagrid = Symbol("hagrid")  # Harry visited Hagrid
dumbledore = Symbol("dumbledore")  # Harry visited Dumbledore
tuesday = Symbol("tuesday")  # It is a Tuesday
run = Symbol("run")  # Harry will go for a run

# If it didn't rain, Harry visited Hagrid today
# Harry visited Hagrid or Dumbledore today, but not both
# Harry visited Dumbledore today
# knowledge = And(
#     Implication(Not(rain), hagrid),
#     Or(hagrid, dumbledore),
#     Not(And(hagrid, dumbledore)),
#     dumbledore,
# )
# Did it rain?
# Did Harry visit Hagrid?

# print(knowledge.formula())
# result = model_check(knowledge, rain)
# print(result)
# result = model_check(knowledge, hagrid)
# print(result)
# result = model_check(knowledge, dumbledore)
# print(result)


# If it is a Tuesday and it is not raining,
# then Harry will go for a run.
# knowledge = And(Implication(And(tuesday, Not(rain)), run), tuesday, Not(rain))
knowledge = And(Implication(Not(rain), run), Not(rain))
print(knowledge.formula())
print(knowledge.symbols())

print(model_check(knowledge, rain))
print(model_check(knowledge, run))
