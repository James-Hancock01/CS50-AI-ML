from logic import *
import termcolor

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")



symbols = [AKnight, AKnave]
def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge, symbol):
            termcolor.cprint(f"{symbol}:YES", "green")
        elif not model_check(knowledge, Not(symbol)):
            print (f"{symbol}: MAYBE")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    #cannot be both knight and knave
    And(
        Not(And(AKnight, AKnave)), Or(AKnight, AKnave),
    ),
    #logical rule for knights and knaves (knaves lie knights dont)
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(Not(AKnave), Not(And(AKnight,AKnave))),

)
print(knowledge0.formula())
print(check_knowledge(knowledge0))
print("\n\n")

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    #cannot be both knight and knave
    And(
        Not(And(AKnight, AKnave)), Or(AKnight, AKnave),
        Not(And(BKnight, BKnave)), Or(BKnight, BKnave),
    ),
    #logical rule for knights and knaves (knaves lie knights dont)
   Implication(AKnight, And(AKnave, BKnave)),
   Implication(AKnave, Not(And(AKnave, BKnave)))

)

symbols += [BKnight, BKnave]

print(knowledge1.formula())
print(check_knowledge(knowledge1))
print("\n\n")

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    And(
        Not(And(AKnight, AKnave)), Or(AKnight, AKnave),
        Not(And(BKnight, BKnave)), Or(BKnight, BKnave),
    ),
    Implication(AKnight, And(AKnight, BKnight)),
    Implication(AKnave, Not(And(AKnave, BKnave))),
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))
)



print(knowledge2.formula())
print(check_knowledge(knowledge2))
print("\n\n")

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
        And(
        Not(And(AKnight, AKnave)), Or(AKnight, AKnave),
        Not(And(BKnight, BKnave)), Or(BKnight, BKnave),
        Not(And(CKnight, CKnave)), Or(CKnight, CKnave),
    ),
    # C said ... about A
    Implication (CKnight, AKnight),     
    Implication (CKnave, AKnave),
    # B said ... about C
    Implication (BKnight, CKnave),
    Implication (BKnave, CKnight),
    
    # B said ... about A
    Implication (BKnight, 
        # then A is a knave
        And(
            Implication(AKnight, AKnave),
            Implication(AKnave, Not(AKnave))
        )
    ),
    Implication (BKnave, 
        # then A is a Knight
        And(
            Implication (AKnight, AKnight),
            Implication (AKnave, Not(AKnight))
        )
    )
)


symbols += [CKnight, CKnave]
print(check_knowledge(knowledge3))


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
